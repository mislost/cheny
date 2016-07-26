#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import threading
import sys

global DATA
global COUNT
COUNT = 0
DATA = []

def get_url(page):
    global DATA
    global COUNT
    url = 'http://www.mtl999.gq/forum-54-%s.html' % page
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    headers = { 'User-Agent' : user_agent }
    request = urllib2.Request(url,headers = headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        print e
        return False
    content = response.read()
    pattern = re.compile('<li .*?>.*?<a href="(thread.*?)".*?',re.S)
    result = pattern.findall(content)
    DATA = DATA + result
    COUNT = COUNT + 1
    return DATA


def run():
    global COUNT
    global DATA
    for i in range(43):
        t = threading.Thread(target=get_url,args=(str(i),))
        t.start()
    


def get_image_url(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    headers = { 'User-Agent' : user_agent }
    request = urllib2.Request(url,headers = headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        return False
    content = response.read()
    pattern = re.compile('<img.*?file="(.*?\.gif)".*?')
    result = pattern.findall(content)
    #print url + ":"
    #for i in result:
    #    print i
    #print "-" * 90
    with open('image.txt','a+') as f:
        for i in result:
            f.write(i + '\n')

def main():
    global DATA, COUNT
    run()
    while True:
        if COUNT > 42:
            DATA = ['http://www.mtl999.gq/%s' % i for i in DATA ]
            for url in DATA:
                k = threading.Thread(target=get_image_url,args=(url,)) 
                k.start()
            return     

if __name__ == '__main__':
    main()
