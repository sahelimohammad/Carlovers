from django.db import models
from django.contrib.auth.models import User





class Relation(models.Model):

    from_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='followers')
    to_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True , blank=True , upload_to='account/%Y/%m/%d/')
    job = models.CharField(max_length=80 , null=True , blank=True)
    country = models.CharField(max_length=30 , null=True , blank=True)
    city = models.CharField(max_length=30 , null=True , blank=True)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null=True , blank=True)


    



