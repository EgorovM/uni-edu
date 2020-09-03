from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, name, password=None, type='PR'):
        """
            Creates and saves a User with the given username and password.
        """
        if username is None:
            raise ValueError('User must have an username.')

        user = self.model(username=username, name=name, type=type)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):
        if password is None:
            raise ValueError('Superusers must have a password.')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    ACCOUNTS_TYPES = (
        ('SH', 'Образовательная организация'),
        ('TH', 'Учитель'),
        ('PR', 'Ученик'),
    )

    username = models.CharField(max_length=127, unique=True)

    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    name = models.CharField(max_length=127)
    type = models.CharField(max_length=2, choices=ACCOUNTS_TYPES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    def send_notification(self, title, content):
        notification = Notification.objects.create(
            user=self,
            title=title,
            content=content
        ).save()

    def send_access_notification(self, course):
        self.send_notification(
            f'{course.name}',
            f'Успешно прошли отбор в курс "{course.name}"! Ждем вас на следующем занятии.'
        )

    def send_reject_notification(self, course):
        self.send_notification(
            f'{course.name}',
            f'Вам была отказана заявка на курс "{course.name}". Попробуйте еще раз.'
        )

    @property
    def full_type(self):
        return dict(self.ACCOUNTS_TYPES)[self.type]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=127)
    content = models.TextField(max_length=1023)
    is_readed = models.BooleanField(default=False)

    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.title}"
