from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=32)
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    publish=models.ForeignKey("Publish",related_name="bookList")
    authorlist=models.ManyToManyField("Author",related_name="bookList") # 多对多的关系，自动创建关系表

    def __str__(self):

        return self.title

class Publish(models.Model):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Author(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()

    def __str__(self):
        return self.name