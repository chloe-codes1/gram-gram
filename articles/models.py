from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail
import re

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True)
    # DB 저장 x, 호출하게 되면 잘라서 표현
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFit(700, 700)],
                                      format='JPEG',
                                      options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 주로 목적어가 되는 model에 정의를 함
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles')
    # 해쉬태그 M:N
    tags = models.ManyToManyField('Hashtag', blank=True)

    class Meta:
        ordering = ['-created_at']

    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.content)

        if not tags:
            return

        for t in tags:
            tag, tag_created = Hashtag.objects.get_or_create(name=t)
            self.tags.add(tag)  
    
class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)