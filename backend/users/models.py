from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    username = models.CharField(max_length=150,
                         unique=True,
                         error_messages={
                             'unique': _("A user with that username already exists."),
                                         })

    email = models.EmailField(_('email address'), blank=True, unique=True)

    def __str__(self):
      return self.username + ' -- ' + self.email