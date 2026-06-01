from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [('student','Хонанда'),('admin','Администратор')]
    role   = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    score  = models.IntegerField(default=0)
    bio    = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        verbose_name = 'Корбар'
        verbose_name_plural = 'Корбарон'

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_admin_role(self):
        return self.role == 'admin' or self.is_staff
