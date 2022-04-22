from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Blog(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=250)
    publish = models.DateTimeField(auto_now_add=True)


class Comment(MPTTModel):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    text = models.CharField(max_length=100)
    publish = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)


    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return f'Комментарий от {self.author}'