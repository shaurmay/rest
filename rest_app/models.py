from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='dishes/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return self.name
    
class Client(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=500)
    comment = models.TextField(blank=True)
    items = models.TextField(help_text='Serialized list of items (snapshot)')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Order {self.id} — {self.full_name} ({self.total_price} грн)"