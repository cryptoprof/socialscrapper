from django.db import models


class VkPosts(models.Model):
    id = models.IntegerField(verbose_name="ID", name="ID", primary_key=True)
    post_id = models.IntegerField(verbose_name="id Поста", name="post_id")
    post_date = models.DateField(verbose_name='дата поста', name='post_date')
    text = models.TextField(verbose_name='Текст', name='text')
    attachments = models.TextField(verbose_name='Приложения к посту', name='attachments', null=True)
    likes = models.IntegerField(verbose_name='лайков', name='likes', null=True)
    comments = models.IntegerField(verbose_name='комментов', name='comments', null=True)
    reposts = models.IntegerField(verbose_name='репостов', name='reposts', null=True)
    views = models.IntegerField(verbose_name='просмотров', name='views', null=True)
    json_dump_full = models.TextField(verbose_name='дамп ответа от vk', name='json_dump_full', null=True)
