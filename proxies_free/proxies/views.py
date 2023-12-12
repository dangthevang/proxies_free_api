import json

from django.http import HttpResponse
from .__init__ import *
import requests as r
from proxy_checking import ProxyChecker

# Create your views here.

def index(request):
    bad_request = json.dumps({'Label':'Bad Request'})
    if 'TYPE_PROXIES' in request.GET:
        type_proxies = request.GET['TYPE_PROXIES']
        proxies = request.GET['PROXIES']
        result = get_proxies_active(type_proxies,proxies)
    else:
        return HttpResponse(bad_request,content_type='application/json',status=400)

    if result is None:
        return HttpResponse(bad_request,content_type='application/json',status=400)
    else:
        res = json.dumps(result, ensure_ascii=False).encode('utf8')
        return HttpResponse(res,content_type='application/json',status=200)

def get_proxies_active(type_proxies, proxies_deny=None):
    source_proxies = r.get(source[type_proxies]).text.replace('\r','')
    list_proxies = source_proxies.split('\n')
    try:
        idx = list_proxies.index(proxies_deny)
    except ValueError:
        idx = 0
    for proxy in list_proxies[idx+1:]:
            if check_active({type_proxies:f'{type_proxies}://{proxy}'},proxy):
                return f'{type_proxies}://{proxy}'
    return None

def print_proxy(proxy):
    checker = ProxyChecker()
    return checker.check_proxy(proxy)

def check_active(dict_proxy,proxy):
    try:
        url = 'http://ipinfo.io/ip'
        res = r.get(url=url,headers={"Content-Type": "application/json; charset=utf-8"},proxies=dict_proxy,timeout=5).text
        ip = proxy.split(':')[0]
        return res == ip
    except:
        return False

