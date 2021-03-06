########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                 Updater - Bui The Hien               #
#                                                      #
#                  dated- 26 June 2016                 #
#                 Update - 20 May 2018                 #
########################################################

import os
import getpass
import bs4
import re
import requests
import time
import urllib
import math

os.makedirs('Wallhaven', exist_ok=True)

def build_params():
    params = ''
    print('''****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallapapers only.
    ga      - For 'General' and 'Anime' wallapapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ')
    ALL = '111'
    ANIME = '010'
    GENERAL = '100'
    PEOPLE = '001'
    GENERAL_ANIME = '110'
    GENERAL_PEOPLE = '101'
    if ccode.lower() == "all":
        ctag = ALL
    elif ccode.lower() == "anime":
        ctag = ANIME
    elif ccode.lower() == "general":
        ctag = GENERAL
    elif ccode.lower() == "people":
        ctag = PEOPLE
    elif ccode.lower() == "ga":
        ctag = GENERAL_ANIME
    elif ccode.lower() == "gp":
        ctag = GENERAL_PEOPLE

    params += "&categories=" + ctag

    print('''
    ****************************************************************
                            Purity Codes

    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - For 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    pcode = input('Enter Purity: ')
    ptags = {'sfw':'100', 'sketchy':'010', 'nsfw':'001', 'ws':'110', 'wn':'101', 'sn':'011', 'all':'111'}
    ptag = ptags[pcode]

    params += "&purity=" + ptag

    rtag = input('Enter at least resolution (ex: 1280x720): ')
    if rtag:
        params += "&atleast=" + rtag

    ratio = input("Enter ratio (16x9): ")
    if ratio:
        params += "&ratios=" + ratio

    stag = input('Enter sort type: relevance, random, date_added, views, favorites, toplist: ')
    if stag:
        params += "&sorting=" + stag

    otag = input('Enter order of sort: desc, asc: ')
    if otag:
        params += "&order=" + otag

    return params

def login():
    print('NSFW images require login')
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    req = requests.post('https://alpha.wallhaven.cc/auth/login', data={'username':username, 'password':password})
    return req.cookies

def category():
    print('''****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallapapers only.
    ga      - For 'General' and 'Anime' wallapapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ')
    ALL = '111'
    ANIME = '010'
    GENERAL = '100'
    PEOPLE = '001'
    GENERAL_ANIME = '110'
    GENERAL_PEOPLE = '101'
    if ccode.lower() == "all":
        ctag = ALL
    elif ccode.lower() == "anime":
        ctag = ANIME
    elif ccode.lower() == "general":
        ctag = GENERAL
    elif ccode.lower() == "people":
        ctag = PEOPLE
    elif ccode.lower() == "ga":
        ctag = GENERAL_ANIME
    elif ccode.lower() == "gp":
        ctag = GENERAL_PEOPLE

    print('''
    ****************************************************************
                            Purity Codes

    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - For 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    pcode = input('Enter Purity: ')
    ptags = {'sfw':'100', 'sketchy':'010', 'nsfw':'001', 'ws':'110', 'wn':'101', 'sn':'011', 'all':'111'}
    ptag = ptags[pcode]

    if pcode in ['nsfw', 'wn', 'sn', 'all']:
        cookies = login()
    else:
        cookies = dict()

    CATURL = 'https://alpha.wallhaven.cc/search?categories=' + \
        ctag + '&purity=' + ptag + '&page='
    return (CATURL, cookies)


def latest():
    print('Downloading latest')
    latesturl = 'https://alpha.wallhaven.cc/latest?page='
    return (latesturl, dict())

def search():
    query = input('Enter search query: ')
    searchurl = 'https://alpha.wallhaven.cc/search?q=' + \
        urllib.parse.quote_plus(query) + build_params() + '&page='
    return (searchurl, dict())

from tqdm import tqdm
from math import *

def main():
    Choice = input('''Choose how you want to download the image:

    Enter "category" for downloading wallpapers from specified categories
    Enter "latest" for downloading latest wallpapers
    Enter "search" for downloading wallpapers from search

    Enter choice: ''').lower()
    while Choice not in ['category', 'latest', 'search']:
        if Choice != None:
            print('You entered an incorrect value.')
        choice = input('Enter choice: ')

    if Choice == 'category':
        BASEURL, cookies = category()
    elif Choice == 'latest':
        BASEURL, cookies = latest()
    elif Choice == 'search':
        BASEURL, cookies = search()

    pgid = int(input('How Many pages you want to Download: '))
    startpg = int(input('Start page to begin download: '))
    if startpg > pgid:
        print("Can download when number of pages less than start page ")
        return

    print('Number of Wallpapers to Download: ' + str(24 * (pgid-startpg+1)))
    for j in range(startpg, pgid + 1):
        totalImage = str(24 * pgid)
        url = BASEURL + str(j)
        print('Starting download page: ' + str(j) + ', url: ' + url);
        urlreq = requests.get(url, cookies=cookies)
        soup = bs4.BeautifulSoup(urlreq.text, 'lxml')
        soupid = soup.findAll('a', {'class': 'preview'})
        res = re.compile(r'\d+')
        imgid = res.findall(str(soupid))
        imgext = ['jpg', 'png', 'bmp']
        for i in range(len(imgid)):
            currentImage = (((j - 1) * 24) + (i + 1))
            url = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.' % imgid[i]
            for ext in imgext:
                iurl = url + ext
                osPath = os.path.join('Wallhaven', os.path.basename(iurl))
                if not os.path.exists(osPath):
                    imgreq = requests.get(iurl, cookies=cookies, stream=True)
                    if imgreq.status_code == 200:
                        print("Downloading : %s - %s / %s" % ((os.path.basename(iurl)), currentImage , totalImage))
                        total_size = int(imgreq.headers.get('content-length', 0))
                        with open(osPath, 'ab') as imageFile:
                            for chunk in tqdm(imgreq.iter_content(1024), total=math.ceil(total_size/1024), unit='KB', unit_scale=True):
                                imageFile.write(chunk)
                        break
                else:
                    print("%s already exist - %s / %s" % (os.path.basename(iurl), currentImage , totalImage))

if __name__ == '__main__':
    main()
