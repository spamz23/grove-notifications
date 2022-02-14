from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.template.loader import render_to_string


from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    """
    The custom User Django model.
    The default `username` field is disabled.
    Instead the `email` field is used.
    """

    # Disable 'username' field
    username = None

    # The user email
    email = models.EmailField(_("Email"), unique=True)

    # The user first name
    first_name = models.CharField(
        _("First name"),
        max_length=60,
        blank=False,
        null=False,
    )

    # The user last name
    last_name = models.CharField(
        _("Last name"),
        max_length=60,
        blank=False,
        null=False,
    )

    # Make the 'email' the 'username' field
    USERNAME_FIELD = "email"

    # The required fields
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    # The custom objects manager
    objects = UserManager()

    def __str__(self):
        """
        String representation of this model. The user fullname.
        """
        return self.get_full_name()

    class Meta:  # noqa
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def notify(
        self,
        subject: str,
        message: str,
    ):
        """
        Notifies the user
        """
        args = {"message": message}
        msg_plain = render_to_string("templates/email_notification.txt", args)
        msg_html = render_to_string("templates/email_notification.html", args)
        send_mail(
            subject,
            msg_plain,
            recipient_list=[self.email],
            fail_silently=False,
            html_message=msg_html,
        )
