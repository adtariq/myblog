
# Create your models here.
# blog/models.py
from django.db import models
from accounts.models import CustomUser
from django.urls import reverse
from django.utils import timezone



class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, \
                                            related_name='blog_posts')
    objects = models.Manager()


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}"

class Rating(models.Model):
    CHOICES=[
        (1, '1'), 
        (2, '2'),
        (3, '3'), 
        (4, '4'),
        (5, '5'), 
        ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField( choices=CHOICES)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-post']

    def __str__(self):
        return f'{self.author.username} - {self.value}'