from django.db import models
from django.contrib.auth.models import AbstractUser
from users.validators import validate_password, validate_username

class User(AbstractUser):
    
    username = models.CharField(
        unique=True, max_length= 50,
        validators=[validate_username],
        )
    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=150,
        validators=[validate_password],
    )
    is_staff = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        """Normalize email and ensure validations before saving."""
        self.email = self.email.lower().strip()
        self.username = self.username.lower().strip()
        if self.password:
            self.set_password(self.password) 
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username

class Role(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

