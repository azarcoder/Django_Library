from django.db import models

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    contact = models.CharField(max_length = 10)
    email = models.EmailField()
    photo = models.ImageField(upload_to='photos/')
    password = models.CharField(max_length = 8)
    flag = models.BooleanField(default=False)    
    class Meta:
        db_table = 'students'

class Books(models.Model):
    bookId = models.IntegerField()
    bookName = models.CharField(max_length = 100)
    authorName = models.CharField(max_length = 100)
    bookCount = models.IntegerField(default=3)
    bookTaken = models.BooleanField(default=False)
    images = models.ImageField(upload_to ='books/')
    lending_info = models.JSONField(null=True, blank=True)
    class Meta:
        db_table = 'books'

    


