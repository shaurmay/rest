from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категорія")

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва страви")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    is_available = models.BooleanField(default=True, verbose_name="В наявності")

    def __str__(self):
        return self.name