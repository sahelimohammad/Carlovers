from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):

    Priority = [
        ("L", "Low"),
        ("M", "Medium"),
        ("H", "High"),
    ]
    
    Status = [
        ("I", "In Progress"),
        ("D", "Done"),
    ]
    

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main')
    image1 = models.ImageField(null=True , blank=True , upload_to='home/%Y/%m/%d/')
    image2 = models.ImageField(null=True , blank=True , upload_to='home/%Y/%m/%d/')
    image3 = models.ImageField(null=True , blank=True , upload_to='home/%Y/%m/%d/')
    image4 = models.ImageField(null=True , blank=True , upload_to='home/%Y/%m/%d/')

    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=10, choices=Priority)
    status = models.CharField(max_length=20, choices=Status)

    class Meta:
        ordering = ['-created' , 'body']
 
    def __str__(self):
        return f'{self.user.username} , {self.created}'

    def get_absolute_url (self):
        return reverse('home:post_detail' , args=(self.id , self.slug))

    def likes_count (self):
        return self.pvote.count()

    def dislikes_count (self):
        return self.pdislike.count()

    def can_like (self , user):
        like = user.uvote.filter(post=self)
        if like.exists():
            return True
        return False

    def can_dislike(self , user):
        dislike = user.udislike.filter(post=self)
        if dislike.exists():
            return True
        return False



#Comment
class Comment (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='ucomments') #which user
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='pcomments') #which post
    reply = models.ForeignKey('Comment' , on_delete=models.CASCADE , related_name='rcomments' ,blank=True , null=True)
    is_reply = models.BooleanField(default=False)
    comment = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -- {self.comment[:30]}'


class Vote (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='uvote')
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='pvote')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'

class DisLike (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='udislike')
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='pdislike')

    def __str__(self):
        return f'{self.user} disliked {self.post.slug}'