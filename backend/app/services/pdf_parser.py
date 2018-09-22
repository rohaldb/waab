import requests
from difflib import SequenceMatcher
import re, json
import PyPDF2
import pprint
import requests
from io import StringIO, BytesIO
from lxml import html
import argparse
import feedparser
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
import urllib3

class CourseMatcher:

    def get_programs_hash():
        req = '{"track_scores":true,"_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","*.active","urlmap","contenttype"],"excludes":["",null,null]},"query":{"filtered":{"query":{"bool":{"must":[{"query_string":{"fields":["*study_level_value*"],"query":"*ugrd*"}}]}},"filter":{"bool":{"should":[{"term":{"contenttype":"course"}}],"must_not":[{"missing":{"field":"*.name"}}]}}}},"from":0,"size":229,"sort":[{"course.code":"asc"}]}'
        res = requests.post("https://www.handbook.unsw.edu.au/api/es/search", req)
        programs = res.json()["esresponse"][0]["hits"]["hits"]
        program_hash = {}
        for program in programs:
            try:
                cource_code = program["_source"]["course.code"]
                out = program["_source"]["course.name"].title()
                program_hash[out] = {
                    "code":cource_code,
                    "urlmap": program["_source"]["urlmap"]
                }
            except:
                print("Error extracting")
        return program_hash

    def get_course(program_name):
        hash_c = CourseMatcher.get_programs_hash()
        program_keys = hash_c.keys()
        for key in program_keys:
            if CourseMatcher.similar("Commerce", key) > 0.92:
                course_obj = hash_c[key]
                return course_obj
        return {}

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()



class PdfParser:
    def filter_output(matches):
        done_or_doing = []
        for match in matches:
            if re.match(r"[A-Z]{4} [0-9]{4}", match) != None:
                done_or_doing.append(re.sub(' ', '', match))

        return done_or_doing

    def get_match(match_array):
        match = match_array[len(match_array)-1]
        #print("Match {}".format(match))
        comparison = re.sub(r'[0-9]{4}', '', match)
        course_obj = CourseMatcher.get_course(comparison)
        #print("C {}".format(course_obj))
        print(json.dumps(course_obj, indent=4))
        return course_obj

    def open_and_extract(bytestream):
        import pdb
        pdb.set_trace()
        
        matchArray = []
        match = ""
        try:
            #print("Attempting to read file {}".format(filename))
            pdf_file = BytesIO((file.read()))
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            num_pages = read_pdf.getNumPages()
            array_of_courses = []
            #print("Num Pages {}".format(num_pages))
            for num in range(num_pages):
                print("Parsing page {}".format(num))
                page = read_pdf.getPage(num)
                page_content = page.extractText()
                matches = re.findall(r'[A-Z]{4} *[0-9]{4}', page_content)
                matches = re.findall(r'Program:(.*?)Plan:', page_content)
                matchArray.extend(matches)
                array_of_courses.extend(PdfParser.filter_output(matches))

            match = PdfParser.get_match(matchArray)
            print(match)
            course_meta_data = PdfParser.parse_listing("https://www.handbook.unsw.edu.au" + match["urlmap"])
            return array_of_courses, course_meta_data, match["code"]
        except:
            print("Error reading file")

    def parse_listing(url):
        """

        Function to process yellowpage listing page
        : param keyword: search query
        : param place : place name
        """

        url_base = url

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

        return courseMetaDataList
