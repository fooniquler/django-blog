from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize


class Post(models.Model):
    class Meta:
        ordering = ['-post_date']

    STATUS_CHOICES = (('published', 'Successfully published'), ('moderation', 'Submitted for moderation'))

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='moderation')

    def get_date(self):
        return humanize.naturaltime(self.post_date)

    def __str__(self):
        return f"{self.author} - {self.title}"
