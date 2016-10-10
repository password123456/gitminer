# -*- coding: utf-8 -*-
__author__ = 'https://github.com/password123456/'

import requests
from lxml import html
import os
import codecs
import datetime
import urllib
import httplib
import time
import mechanize

codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
LOG_FILE_NAME = datetime.datetime.now().strftime("%Y%m%d") + '_git_miner.txt'

class bcolors:
    HELP = '\033[1;36m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GitMiner():

    def __init__(self, session):

        self.logo = bcolors.OKGREEN+"""
 ██████╗ ██╗████████╗███╗   ███╗██╗███╗   ██╗███████╗██████╗
██╔════╝ ██║╚══██╔══╝████╗ ████║██║████╗  ██║██╔════╝██╔══██╗
██║  ███╗██║   ██║   ██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝
██║   ██║██║   ██║   ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗
╚██████╔╝██║   ██║   ██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║
 ╚═════╝ ╚═╝   ╚═╝   ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ v1.0.1

 Automatic search for GitHub.

 """+bcolors.ENDC+bcolors.FAIL+"""+ Original Author:"""+bcolors.ENDC+""" Danilo Vaz a.k.a. UNK
 """+bcolors.FAIL+"""+ Modified by:"""+bcolors.ENDC+""" password123456
 """+bcolors.FAIL+"""+ Github:"""+bcolors.ENDC+""" https://github.com/password123456
""" + bcolors.WARNING + \
"\n +[" + bcolors.FAIL + "WARNING" + bcolors.WARNING \
+ "]------------------------------------------+" \
"\n | DEVELOPERS ASSUME NO LIABILITY AND ARE NOT        |" \
"\n | RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY    |" \
"\n | THIS PROGRAM                                      |" \
"\n +---------------------------------------------------+\n\n" + bcolors.ENDC

        self.session = session
        self.url = "https://github.com"
        self.user_agent = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"}
        self.keyword = []
        self.number_page = None

    def get_keyword(self, filename):

        f = open(filename, 'r')
        for i in f.readlines():
            #print(i)
            self.keyword.append(i.strip())

    def save_output(self, text):
        save_log = open(LOG_FILE_NAME, 'a')
        save_log.write(text)
        save_log.close()

    def next_page(self,prox_page, key):
        print(bcolors.HELP + "\n+[PAGE %s/%s]-----------------------------------------+" % (prox_page.split("&")[1].split("=")[1], self.number_page) + bcolors.ENDC)
        HTML = self.access_web(prox_page)
        self.parse_search(HTML.content, key)

    def parse_search(self, response, key):
        tree = html.fromstring(response)
        url_file = tree.xpath('//div[contains(@class, "code-list-item-public")]/p[contains(@class, "title")]/a[2]/@href')
        last_indexed = tree.xpath('//div[contains(@class, "code-list-item-public")]/p[contains(@class, "title")]\
                                  /span[contains(@class, "updated-at")]/time/text()')
        user = tree.xpath('//div[contains(@class, "code-list-item-public")]/a/img[contains(@class, "avatar")]/@alt')
        prox_page = tree.xpath('//a[contains(@class, "next_page")]/@href')

        for number_link in range(len(url_file)):
            link = self.url + url_file[number_link].replace("blob","raw")
            HTML = self.access_web(link)
            code_boladao = HTML.text
            print("| [" + bcolors.OKBLUE + "USER" + bcolors.ENDC + "]: %s" % user[number_link])
            self.save_output("| [USER]: %s\n" % user[number_link])
            print("| [" + bcolors.OKBLUE + "LINK" + bcolors.ENDC + "]: %s" % link)
            self.save_output("| [LINK]: %s\n" % link)
            try:
                print("| [" + bcolors.OKBLUE + "LAST INDEXED" + bcolors.ENDC + "]: %s" % last_indexed[number_link])
                self.save_output("| [LAST INDEXED]: %s\n" % last_indexed[number_link])
            except:
                pass

        if not prox_page:
            return
        prox_page = prox_page[0]
        prox_page = self.url + prox_page
        self.next_page(prox_page, key)

    def access_web(self, url_access):

        try:
            acc = requests.get(url_access, cookies=self.session, headers=self.user_agent)
            time.sleep(1)
        except Exception as e:
            print(e)
            return None
        if " find any code matching" in acc.text:
            print("[-] We couldn't find any code matching\n")
            self.save_output("[-] We couldn't find any code matching\n")
            return None
        return acc

    def parser_pages(self, response):
        tree = html.fromstring(response)
        number_page = tree.xpath('//div[contains(@class, "pagination")]/a/text()')
        #print number_page
        if number_page:
            return number_page[len(number_page)-2]
        else:
            return "1"

    def start(self):
        print(self.logo)
        self.get_keyword('keyword.txt')
        if len(self.keyword) > 0:
            for key in self.keyword:
                print('\n+[Keyword: %s]' % key)
                self.save_output('+[Keyword: %s]\n' % key)
                search_term = "/search?o=desc&q=%s&s=indexed&type=Code&utf8=✓" % key
                #print(search_term)
                url_access = self.url + search_term
                #print(url_accesss)
                HTML = self.access_web(url_access)
                if HTML is None:
                    #print('HTML is None')
                    continue
                self.number_page = self.parser_pages(HTML.content)
                print(bcolors.HELP + "+[PAGE: 1/%s]-----------------------------------------+" % self.number_page + bcolors.ENDC)
                self.save_output("+[PAGE: 1/%s]-----------------------------------------+\n" % self.number_page)
                self.parse_search(HTML.content, key)


def github_login():
    username = 'your github id'
    password = 'your github password'

    browser = mechanize.Browser()
    cj = mechanize.CookieJar()
    browser.set_cookiejar(cj)
    browser.set_handle_robots(False)
    response = browser.open('https://github.com/login')

    browser.select_form(nr = 0)
    browser.form['login'] = username
    browser.form['password'] = password
    browser.submit()

    cookies = browser._ua_handlers['_cookies'].cookiejar
    cookie_dict = {}
    for c in cookies:
        cookie_dict[c.name] = c.value
    return cookie_dict

def main():
    session = github_login()
    gitminer = GitMiner(session)
    gitminer.start()

if __name__ == '__main__':
    main()
