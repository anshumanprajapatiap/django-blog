from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categorie(models.Model):
    All_Cat = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.All_Cat

class Post(models.Model):
    Cat = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Title = models.CharField(max_length=40, null=True)
    Post_date = models.DateTimeField(null=True)
    Short_dis = models.TextField(null=True)
    Long_dis = models.TextField(null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.Title+'--'+self.Cat.All_Cat+'--'+self.usr.username

class LikeComment(models.Model):
    post_data = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    usr = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    like = models.BooleanField(default=False)
    comment = models.TextField(null=True)
    date = models.DateField(null=True)

    def __str__(self):
        return self.post_data.Title

class UserDetail(models.Model):
    usr = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.usr.username