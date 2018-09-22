import PyPDF2
import textract
import re
import json
import pprint
import requests
from io import StringIO, BytesIO

class PdfParser:
    def filter_output(matches):
        done_or_doing = []
        for match in matches:
            if re.match(r"[A-Z]{4} [0-9]{4}", match) != None:
                done_or_doing.append(re.sub(' ', '', match))

        return done_or_doing

    def open_and_extract(bytestream):
        try:
            #print("Attempting to read file {}".format(filename))
            pdf_file = StringIO(bytestream)
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            num_pages = read_pdf.getNumPages()
            array_of_courses = []
            print("Num Pages {}".format(num_pages))
            for num in range(num_pages):
                print("Parsing page {}".format(num))
                page = read_pdf.getPage(num)
                page_content = page.extractText()
                matches = re.findall(r'[A-Z]{4} *[0-9]{4}', page_content)
                array_of_courses.extend(filter_output(matches))

            return { "data": { "Courses":  array_of_courses } }
        except:
            print("Error reading file")
