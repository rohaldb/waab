#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import argparse
import re
import feedparser
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
import urllib3

def parse_listing():
    """

    Function to process yellowpage listing page
    : param keyword: search query
    : param place : place name
    """

    url_base = "https://www.handbook.unsw.edu.au/undergraduate/specialisations/2019/COMPA1"

    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'www.yellowpages.com.au',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    req = Request(url_base, headers=headers)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    response = requests.get(url_base, verify=False, headers = headers )
    seenFinal = False
    scraped_results = []

    # f = open("soup.txt", "a")
    # f.write(str(soup))
    # {"code" :"COMP1511", "name": "programming Fundamentals"},

    x = soup.find('li', class_="crumb truncate").text

    courseCodeList = []
    for course in soup.find_all("span", class_="align-left"):
        item = course.text
        courseCodeList.append(item)

    courseNameList = []
    for course in soup.find_all("p", class_="a-card-text m-toggle-text has-focus"):
        item = course.text
        courseNameList.append(item)

    courses = []

    if (len(courseCodeList) < len(courseNameList)):
        for index, item in enumerate(courseCodeList):
            object = {"code": item, "name": courseNameList[index] }
            courses.append(object)
    else:
        for index, item in enumerate(courseNameList):
            object = {"code": courseCodeList[index], "name": item }
            courses.append(object)

    courseMetaDataList = []

    for item in courseCodeList:
        print(item)
        courseURL = "https://www.handbook.unsw.edu.au/undergraduate/courses/2019/" + item + "/"
        response = requests.get(courseURL, verify=False, headers = headers )

        if (response.status_code == 200):
            req = Request(courseURL, headers=headers)
            newPage = urlopen(req)
            newSoup = BeautifulSoup(newPage, 'html.parser')
            prereq = []
            for course in newSoup.find_all("div", class_="a-card-text m-toggle-text has-focus"):
                val = course.text

                x = val.split("Prerequisite: ",1)
                if (len(x) == 2):
                    prereq2 = x[1]
                    pres = re.findall(r'\b\w{8}\b',prereq2)
                    prereq = pres

            terms = []
            for course in newSoup.find_all("div", class_="o-attributes-table-item "):
                foundTerms = course.text
                if "Offering Term" in foundTerms:
                    getTerms = foundTerms[16:].split(',')
                    str = getTerms[-1][0:len(getTerms[-1]) - 1]
                    getTerms[-1] = str
                    terms = getTerms

            courseMetaDataList.append({ "course": item, "prereqs": prereq, "sems": terms, "des": val })

    print(courseMetaDataList)

    # print(courseMetaDataList)

if __name__=='__main__':

	parse_listing()
