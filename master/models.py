from django.db import models

class Company(models.Model):
    s_no = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=254, null=True)
    title = models.CharField(max_length=250, null=True)
    company = models.CharField(max_length=250, null=True)
    
    def __str__(self):
        return self.company


