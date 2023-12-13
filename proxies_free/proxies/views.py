import json

from django.http import HttpResponse
from .__init__ import *
import requests as r
from proxy_checking import ProxyChecker
import random

HEADERS = {"Content-Type": "application/json; charset=utf-8"}


# Create your views here.

def index(request):
    bad_request = json.dumps({'Label': 'Bad Request'})
    if request.method == 'POST':
        result = post_method(request)
    elif request.method == 'GET':
        result = get_method(request)
    else:
        return HttpResponse(bad_request, content_type='application/json', status=400)

    if len(result) != 0:
        return HttpResponse(json.dumps(result), content_type='application/json', status=400)
    else:
        return HttpResponse(json.dumps({'Status': 'Not Active'}), content_type='application/json', status=400)

def post_method(request):
    t_proxy = request.POST['type_proxies']
    l_proxy = get_proxies_active(t_proxy)
    for proxy in l_proxy:
        try:
            rs = r.post(request.POST['endpoint'], headers=HEADERS, proxies={t_proxy: proxy},
                              data=json.dumps(request.POST['payload'][0]),verify=False)
            if rs.status_code == 200:
                return [proxy]
        except:
            print(proxy)
    return None


def get_method(request):
    t_proxy = request.GET['type_proxies']
    l_proxy = get_proxies_active(t_proxy)
    return l_proxy


def get_proxies_active(type_proxies, limit=50):
    source_proxies = r.get(source[type_proxies]).text.replace('\r', '')
    list_proxies = random.choices(source_proxies.split('\n'), k=limit)
    result_ = []
    for proxy in list_proxies:
        if check_active({type_proxies: f'{type_proxies}://{proxy}'}, proxy):
            result_.append(f'{type_proxies}://{proxy}')
    return result_


def print_proxy(proxy):
    checker = ProxyChecker()
    return checker.check_proxy(proxy)


def check_active(dict_proxy, proxy):
    try:
        url = 'http://ipinfo.io/ip'
        res = r.get(url=url, headers={"Content-Type": "application/json; charset=utf-8"}, proxies=dict_proxy,
                    timeout=5).text
        ip = proxy.split(':')[0]
        return res == ip
    except:
        return False
