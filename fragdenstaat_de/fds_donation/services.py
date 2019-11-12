from django.db import models
from django.utils import timezone
from django.contrib import auth

from froide.account.models import User
from froide.account.services import AccountService
from froide.helper.email_sending import mail_registry

from fragdenstaat_de.fds_newsletter.utils import subscribe_to_default_newsletter

from .models import Donor, Donation
from .utils import subscribe_donor_newsletter


def get_or_create_donor(data, user=None, subscription=None):
    if user is not None:
        try:
            return Donor.objects.get(user=user)
        except Donor.DoesNotExist:
            return create_donor(data, user=user, subscription=subscription)
    # TODO: find donor in another way?
    return create_donor(data, user=user, subscription=subscription)


def create_donor(data, user=None, subscription=None):
    email_confirmed = None
    if user is not None and user.email.lower() == data['email'].lower():
        email_confirmed = user.date_joined
    donor = Donor.objects.create(
        salutation=data.get('salutation', ''),
        first_name=data['first_name'],
        last_name=data['last_name'],
        company_name=data.get('company', ''),
        address=data.get('address', ''),
        postcode=data.get('postcode', ''),
        city=data.get('city', ''),
        country=data.get('country', ''),
        email=data['email'].lower(),
        user=user,
        email_confirmed=email_confirmed,
        subscription=subscription,
        contact_allowed=data.get('contact', False),
        become_user=data.get('account', False),
        receipt=data.get('receipt', False),
    )
    if donor.email_confirmed and donor.contact_allowed:
        subscribe_to_default_newsletter(donor.email, user=user)
        subscribe_donor_newsletter(donor)

    return donor


new_donor_thanks_email = mail_registry.register(
    'fds_donation/email/donor_new_thanks',
    (
        'name', 'first_name', 'last_name', 'salutation',
        'payment',
    )
)

donor_thanks_email = mail_registry.register(
    'fds_donation/email/donor_thanks',
    (
        'name', 'first_name', 'last_name', 'salutation',
        'payment',
    )
)

donor_optin_email = mail_registry.register(
    'fds_donation/email/donor_thanks_optin',
    (
        'name', 'first_name', 'last_name', 'salutation',
        'payment',
    )
)


def send_donation_email(donation):
    if donation.email_sent:
        return
    donor = donation.donor

    extra_context = {}
    if donor.email_confirmed:
        # No opt-in needed
        if donor.email_confirmation_sent:
            # not a new donor
            mail_intent = donor_thanks_email
        else:
            mail_intent = new_donor_thanks_email
    else:
        mail_intent = donor_optin_email
        extra_context = {
            'action_url': donor.get_url()
        }

    context = {
        'name': donor.get_full_name(),
        'first_name': donor.first_name,
        'last_name': donor.last_name,
        'salutation': donor.get_salutation(),
        'payment': donation.payment,
    }
    context.update(extra_context)

    mail_intent.send(
        user=donor.user,
        email=donor.email,
        context=context,
        ignore_active=True, priority=True
    )
    donation.email_sent = timezone.now()
    donation.save()
    donor.email_confirmation_sent = donation.email_sent
    donor.save()


def create_donation_from_payment(payment, ):
    order = payment.order
    try:
        return Donation.objects.get(
            models.Q(payment=payment) | models.Q(order=order)
        )
    except Donation.DoesNotExist:
        pass
    # No donation, so no donor, let's create one
    donor = get_or_create_donor({
        'first_name': order.first_name,
        'last_name': order.last_name,
        'address': order.street_address_1,
        'city': order.city,
        'postcode': order.postcode,
        'country': order.country,
    }, user=order.user, subscription=order.subscription)
    donation = Donation.objects.create(
        donor=donor,
        timestamp=order.created,
        amount=order.total_gross,
        order=order,
        payment=payment
    )
    return donation


def confirm_donor_email(donor, request=None):
    if request and request.user.is_staff:
        # Don't trigger things as staff
        return
    is_auth = request and request.user.is_authenticated

    donor.email_confirmed = timezone.now()
    donor.save()

    # Try finding existing user via email
    user = None
    if not donor.user:
        try:
            user = User.objects.get(
                email__iexact=donor.email,
                is_active=True
            )
        except User.DoesNotExist:
            user = None
        if user is not None:
            donor.user = user
            donor.save()
            if request:
                auth.login(request, user)

        elif donor.become_user and not is_auth:
            # Create user
            user, created = AccountService.create_user(
                user_email=donor.email,
                first_name=donor.first_name,
                last_name=donor.last_name,
                address=donor.get_full_address(),
                private=True
            )
            AccountService(user)._confirm_account()
            donor.user = user
            donor.save()
            # Login new user
            if request:
                auth.login(request, user)
    else:
        user = donor.user

    if donor.contact_allowed:
        # Subscribe to normal and donor newsletter
        # TODO: subscribe email address / if different from user?
        subscribe_to_default_newsletter(
            donor.email, user=user,
            name=donor.get_full_name(),
            email_confirmed=True
        )
        subscribe_donor_newsletter(donor, email_confirmed=True)
