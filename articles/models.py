from django.db import models
from django.conf import settings
import re

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
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