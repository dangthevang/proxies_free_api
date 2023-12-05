import json

from django.shortcuts import render
from django.http import HttpResponse
from .__init__ import *
import requests as rq
from proxy_checking import ProxyChecker

import urllib
# Create your views here.

def index(request):
    bad_request = json.dumps({'Label':'Bad Request'})

    if 'TYPE_PROXIES' in request.GET:
        type_proxies = request.GET['TYPE_PROXIES']
        link_test = request.GET['LINK_TEST']
        result = get_proxies_active(type_proxies,link_test)
    else:
        return HttpResponse(bad_request,content_type='application/json',status=400)

    if result is None:
        return HttpResponse(bad_request,content_type='application/json',status=400)
    else:
        res = json.dumps(result, ensure_ascii=False).encode('utf8')
        return HttpResponse(res,content_type='application/json',status=200)

def get_proxies_active(type_proxies, link_test):
    source_proxies = rq.get(source[type_proxies]).text.replace('\r','')
    list_proxies = source_proxies.split('\n')
    for proxy in list_proxies:
        try:
            dict_proxies = print_proxy(proxy)
            if dict_proxies['status'] and type_proxies in dict_proxies['type']:
                    # and get_status(proxy, type_proxies):
                return f'{type_proxies}://{proxy}'
        except:
            continue
    return None

def get_status(proxies,link_test):
    try:
        headers = {"Content-Type": "application/json; charset=utf-8"}
        rs = rq.get(link_test,proxies=proxies,headers=headers)
        if rs.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def print_proxy(proxy):
    checker = ProxyChecker()
    return checker.check_proxy(proxy)

def is_proxy(proxy, link_test, type_proxy):
    print(proxy)
    try:
        proxy_handler = urllib.request.ProxyHandler({f'{type_proxy}': f'{type_proxy}://{proxy}'})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        sock=urllib.request.urlopen(link_test)
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return False
    except Exception as detail:
        print( "ERROR:", detail)
        return False
    return True