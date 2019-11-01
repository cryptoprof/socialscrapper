from django.shortcuts import render
import vk
from scrappers import settings as myapp_settings

# Create your views here.
def hello(request):
    #get token from scrappers/settings.py. Just add a string VK_TOKEN='YOUR_TOKEN' in settings.py
    session = vk.Session(access_token=getattr(myapp_settings, 'VK_TOKEN'))
    api = vk.API(session, v='5.103', lang='ru', timeout=10)
    posts = api.wall.get(domain='beregaonline_tutaev',count=100,offset=100)
    return render(request, 'posts/index.html', {
        'posts': posts,
        'token': getattr(myapp_settings, 'VK_TOKEN'),
    })
