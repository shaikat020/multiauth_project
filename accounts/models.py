from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, name, id_number, contact_information, password=None, role='student', level=None, term=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        if not all([name, id_number, contact_information]):
            raise ValueError('All required fields must be provided')

        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            name=name,
            role=role,
            id_number=id_number,
            contact_information=contact_information,
            level=level if role == 'student' else None,
            term=term if role == 'student' else None,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=email,
            name=name,
            id_number="000000",
            contact_information="Admin User",
            password=password,
            role="admin"
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    id_number = models.CharField(max_length=20, unique=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    term = models.CharField(max_length=50, null=True, blank=True)
    contact_information = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'id_number', 'contact_information']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin