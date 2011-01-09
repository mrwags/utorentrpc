#! /usr/bin/env python
# coding: utf8
'''
Created on 29.12.2010

@author: cyberone
'''
import unittest
from utorrentrpc import discover


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testTest(self):
        pass
    
    def testDiscover(self):
        '''
        Выполнять только дома
        '''
        # DONE: Unit-test
        clients = discover([
                            'http://192.168.1.2:8080/gui',
                            'http://192.168.1.3:8080/gui',
                            'http://192.168.1.4:8080/gui',
                            'http://192.168.1.5:8080/gui',
                            ],
                            'admin',
                            '1')
        self.assertTrue(len(clients) > 0)
        
    def testGetSettings(self):
        # DONE: Подключаемся
        client = discover([
                            'http://192.168.1.2:8080/gui/',
                            'http://192.168.1.3:8080/gui/',
                            'http://192.168.1.4:8080/gui/',
                            'http://192.168.1.5:8080/gui/',
                            ],
                            'admin',
                            '1')[0]
        # DONE: Получаем словарь настроек
        settings = client.get_settings()
        # DONE: Ищем в словаре bandwidth
        self.assertTrue(settings.has_key('settings'))
        
    def testSetSettings(self):
        client = discover([
                            'http://192.168.1.2:8080/gui/',
                            'http://192.168.1.3:8080/gui/',
                            'http://192.168.1.4:8080/gui/',
                            'http://192.168.1.5:8080/gui/',
                            ],
                            'admin',
                            '1')[0]
        client.set_settings([('max_dl_rate', '5')])
        settings = client.get_settings()
        for i in settings['settings']:
            if i[0] == 'max_dl_rate':
                self.assertEquals('5', i[2])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()