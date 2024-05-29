from django.db import models
from django.core.exceptions import ValidationError
from account.models import User
from catalog.models import Product


class Order(models.Model):
    customer = models.ForeignKey(User, related_name='customer',
                                 on_delete=models.CASCADE, verbose_name='Покупатель')
    products = models.ManyToManyField(Product, verbose_name='Товары', blank=True, through='ProductsInOrder')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    all_total_price = models.PositiveIntegerField(default=0, verbose_name='Общая итоговая цена')  # Новое поле


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.customer} - {self.created}'


class ProductsInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар', related_name='count_in_order',)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество товара в заказе')
    total_price = models.PositiveSmallIntegerField(verbose_name='Итоговая цена в заказе') # Добавление нового поля


class ServiceExecution(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    execution_date = models.DateField(verbose_name='Дата выполнения')
    note = models.TextField(blank=True, null=True, verbose_name='Примечание')
    employee = models.CharField(max_length=255, verbose_name='Сотрудник')

    class Meta:
        verbose_name = 'Выполнение услуги'
        verbose_name_plural = 'Выполнениe услуг'

    def clean(self):
        if ServiceExecution.objects.filter(order=self.order).exists() and not self.pk:
            raise ValidationError(f"Выполнение услуги для заказа {self.order} уже существует.")

    def __str__(self):
        return f"Услуга: {self.order.customer}\nКлиент: {self.order.customer}\nДата: {self.execution_date}"

    def order_without_date(self):
        return f"{self.order.customer}"
