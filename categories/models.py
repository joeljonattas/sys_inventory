from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, max_length=300)
    equipament_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    