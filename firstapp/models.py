from django.db import models

# Create your models here.
#Task-Book show in table format
#data fill in the form thats why create the form in client side
# show edit&delete option 
class Book(models.Model):   #define models
    name = models.CharField(max_length=100)
    qty = models.IntegerField()
    price = models.FloatField()
    author = models.CharField(max_length=100)
    is_published = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

def __str__(self):
    return self.name

class Meta:
    db_table = "book"