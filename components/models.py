from django.db import models

# Create your models here.
class Bloggers(models.Model):
    ename = models.CharField(max_length=100)
    eemail = models.EmailField()
    password = models.CharField(max_length=100)
    uid_name = models.CharField(max_length=800)
    img = models.CharField(max_length=100)
    class Meta:
        db_table = "blog"
