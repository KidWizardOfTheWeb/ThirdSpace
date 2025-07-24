from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db.models import TextField
from django.template.defaultfilters import default
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField

# Create your models here.
class User(AbstractUser):
    # objects = models.Manager()
    objects = UserManager()
    USER_TYPES = (
        (1, "Basic"),
        (2, "Moderator"),
        (3, "Admin"),
    )

    aws_token = models.TextField()
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default=1)
    phone_number = PhoneNumberField(blank=True)
    activated = models.BooleanField(default=True)

    dark_mode = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    picture = models.ImageField(upload_to='profile_pics', default='default.jpg')

    website_code = HTMLField(default="")
    website_as_string = models.TextField(default="")

    # add birthday?

    # don't enforce real names probably, make this username instead
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def name(self):
        return str(self)
    pass

class Account(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # sponsor = models.ManyToManyField(Sponsor, through='DriverSponsorship', related_name = "drivers", db_index=True)
    # current_sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True, blank=True, related_name="current_sponsor")
    #point_balance = models.IntegerField(default=0) # need to migrate to being between driver and sponsor

    # @property
    # def point_balance(self):
    #     if self.current_sponsor:
    #         sponsorship = self.sponsorships.filter(sponsor=self.current_sponsor).first()
    #         if sponsorship:
    #             return sponsorship.point_balance
    #
    #     return 0
    #
    # @point_balance.setter
    # def point_balance(self, value):
    #     # sponsorship = self.sponsorships.filter(sponsor=self.current_sponsor).first()
    #     if self.current_sponsor:
    #         sponsorship = self.sponsorships.filter(sponsor=self.current_sponsor).first()
    #         if sponsorship:
    #             suspension_level = sponsorship.suspension_level
    #             if suspension_level == 0:
    #                 sponsorship.point_balance = value
    #                 sponsorship.save()
    #             elif suspension_level == 1:
    #                 print("Suspended account! Cannot gain points at this time, contact an admin.")
    #             elif suspension_level == 2:
    #                 print("Suspicious user! Admins will review your account.")
    #             else:
    #                 print("Suspension type unknown. Contact an admin.")
    #         else:
    #             print("No account here! Cannot gain points at this time, contact an admin.")
    #     else:
    #         print("NO SPONSOR ASSIGNED")

    # def __str__(self):
    #     return f'Driver {self.user.username}'

class NotificationSettings(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')

    # Notification preferences
    # Need to only show certain notifications on the form for each user type
    delivery_notification = models.BooleanField(default=False)
    shipped_notification = models.BooleanField(default=False)
    point_change_notification = models.BooleanField(default=False)
    rate_change_notification = models.BooleanField(default=False)
    purchase_notification = models.BooleanField(default=False)
    approvals_notification = models.BooleanField(default=True)
    sponsor_notification = models.BooleanField(default=False)
    sponsor_removal_notification = models.BooleanField(default=True)
    catalog_notification = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification Settings for {self.user.name}"

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    job_title = models.CharField(max_length=100, default="Admin")

    def __str__(self):
        return f'{self.user.username}'

class AuditLog(models.Model):
    class CATEGORY_CHOICES(models.TextChoices):
        # SPONSOR_APP = "application"
        PASS_CHANGE = "pwdchange"
        LOGIN_ATTEMPT =  "login"
        OTHER = "other"

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=20, choices = CATEGORY_CHOICES.choices, default=CATEGORY_CHOICES.OTHER)
    log_message = models.TextField()
    timestamp = models.DateTimeField()
    audits = models.Manager()

    def __str__(self):
        return f'[{self.category}] {self.timestamp} - {self.log_message}'

class UserPageData(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default="")
    content = HTMLField()
    content_as_string = TextField(default="")

    def __str__(self):
        return f'{self.content}'