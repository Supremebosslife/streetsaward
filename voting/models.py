from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None  # Remove the username field

    # Add any additional fields as needed

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # Set email as a required field

class Category(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=50, default='fa-question')  # Default icon is 'fa-question' (question mark)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Nominee(models.Model):
    nominee_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/nominee_images/', default='static/nominee_images/blank.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nominee_name

class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nominee = models.ForeignKey(Nominee, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'nominee', 'category')

    def __str__(self):
        return f"{self.user} voted for {self.nominee.nominee_name} in {self.category}"