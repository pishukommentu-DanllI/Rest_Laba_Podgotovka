from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User
from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name='Товары')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name='Товары')
    price = models.IntegerField(verbose_name='Цена', null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            self.price = sum(product.price for product in self.products.all())
        except ValueError:
            self.price = 0
        super(Order, self).save()


# переопределенная модель user для входа по mail, а не по name
class UserCustom(AbstractUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    fio = models.CharField(blank=False, max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio', 'username']

    def __str__(self):
        return f'{self.fio}'
