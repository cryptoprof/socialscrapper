from django.shortcuts import render
import vk, json
from scrappers import settings as myapp_settings
from .models import VkPosts
import datetime


# Create your views here.
def collect_data(request):
    # get token from scrappers/settings.py. Just add a string VK_TOKEN='YOUR_TOKEN' in settings.py
    session = vk.Session(access_token=getattr(myapp_settings, 'VK_TOKEN'))
    api = vk.API(session, v='5.103', lang='ru', timeout=10)
    posts = api.wall.get(domain='beregaonline_tutaev', count=100, offset=0)
    for post in posts['items']:
        base_post = VkPosts()
        base_post.post_id = int(post['from_id'])
        base_post.post_date = datetime.datetime.fromtimestamp(post['date'])
        #Если это репост, возьмем текст из него
        if('copy_history' in post):
            post['text'] = 'REPOST:'+post['copy_history'][0]['text']
        base_post.text = (str(post['text']))
        try:
            base_post.attachments = post['attachments']
        except KeyError:
            print("well, it WASN'T defined after all!")
        base_post.likes = post['likes']['count']
        base_post.reposts = post['reposts']['count']
        base_post.comments = post['comments']['count']
        base_post.json_dump_full = post
        if (post['views']):
            base_post.views = post['views']['count']
        base_post.save()
    return render(request, 'posts/index.html', {
        'posts': posts,
        'token': getattr(myapp_settings, 'VK_TOKEN'),
    })
