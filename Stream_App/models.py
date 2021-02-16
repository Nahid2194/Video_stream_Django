from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Video(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post_user')
    video_title = models.CharField(max_length=250, verbose_name='Put a Title')
    slug = models.SlugField(max_length=5, unique=True)
    video_content = models.FileField(
        verbose_name='Upload Video', upload_to='videos')
    thumbnail = models.ImageField(
        verbose_name='Add to Thumbnail', upload_to='thumbnails', blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.video_title

    def save(self):
        self.slug = slugify(self.video_title + '-' + str(uuid.uuid4()))
        super(Video, self).save()


class Comment(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='video_comment')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment_user')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return self.comment
