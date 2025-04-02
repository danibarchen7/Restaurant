from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits= 6, decimal_places=2)
    image_url = models.ImageField(blank=True, null=True)
    def __str__(self):
        return self.name