#! /usr/bin/env python
# coding: utf8
'''
Created on 29.12.2010

@author: cyberone
'''
import urllib2
import base64
from urllib2 import URLError
from xml.dom.minidom import parse
import json

class UTorrentRPC:
    '''
    Клиент для utorrent.
    Создание: 
    UTorrentRPC(url='http://192.168.1.3:8080/gui', user='admin', password='secret')
    '''


    def __init__(self, *args, **kwargs):
        '''
        Создаёт подключенного клиента.
        Параметры:
        user — имя пользователя
        password — пароль пользователя
        url — адрес клиента 
        '''
        # DONE: Переписать себе адрес, пользователя и пороля
        self._url = kwargs['url']
        try:
            self._username = kwargs['username']
            self._password = kwargs['password']
        except KeyError:
            pass
        u = self._connect()
        doc = parse(u)
        u.close()
        # DONE: вытащить auth token
        token_node = doc.getElementsByTagName('div')[0]
        self._token = token_node.childNodes[0].data
        pass
    
    def _connect(self, get_string = None):
        url = self._url
        if get_string != None:
            url += '?' + get_string
        req = urllib2.Request(url)
        try:
            base64string = base64.encodestring('%s:%s' % (self._username, self._password))[:-1]
            authheader =  "Basic %s" % base64string
            req.add_header("Authorization", authheader)
        except AttributeError:
            pass
        u = urllib2.urlopen(req, None, 3)
        return u
    
    def get_settings(self):
        # DONE: Подключаемся
        u = self._connect('action=getsettings&token=' + self._token)
        # DONE: Получаем настройки
        settings = json.loads(u.read())
        u.close()
        return settings
    
    def set_settings(self, settings):
        '''
        Изменяет настройки
        @param settings: массив кортежей [(имя1, значение1), …]
        '''
        arr = ['token=' + self._token, 'action=setsetting']
        for i in settings:
            arr.append('s=' + i[0])
            arr.append('v=' + i[1])
        u = self._connect('&'.join(arr))
        u.read()
        u.close()
        

def discover(urls, username = None, password = None):
    '''
    Ищет и возвращает список наёденных utorrent ресурсов
    @param urls: список урлов
    @param username:
    @param pasword:
    '''
    result = []
    # DONE: Обнаружить в списке урлов utorrent
    for i in urls:
        req = urllib2.Request(i)
        if username != None:
            base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
            authheader =  "Basic %s" % base64string
            req.add_header("Authorization", authheader)
        try:
            u = urllib2.urlopen(req, None, 3)
            result.append(UTorrentRPC(url = i, username = username, password = password))
        except URLError:
            pass
    return result
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()