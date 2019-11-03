from django.shortcuts import render
from scrappers import settings as myapp_settings
from .lib.FacebookWebBot import *
import datetime


# Create your views here.
def collect_data(request):
    bot = FacebookBot()
    bot.set_page_load_timeout(10)
    fb_login = getattr(myapp_settings, 'FACEBOOK_LOGIN')
    fb_pass = getattr(myapp_settings, 'FACEBOOK_PASSWORD')
    bot.login(fb_login, fb_pass)
    allpost = bot.getPostInProfile("https://mbasic.facebook.com/DmitryYunusov.TutaevDistrict", moreText="Еще новости",
                                   deep=10)
    return render(request, 'posts/fb/index.html', {
        'posts': allpost,
    })

