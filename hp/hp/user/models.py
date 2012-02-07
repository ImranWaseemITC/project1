from django.db import models
import uuidfield

class user(models.Model):
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    nickname = models.CharField(max_length=20) #validate
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=100) #validate
    pw_salt = models.CharField(max_length=100)
    email = models.EmailField() #validate
    join_date_time = models.DateTimeField()
    address = models.TextField(blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    fax_number = models.BigIntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
    class Meta:
        ordering = ["first_name"]