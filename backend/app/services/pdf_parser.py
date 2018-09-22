import PyPDF2
import re
import json
import pprint
from io import StringIO, BytesIO
import pdb

class PdfParser:
    def filter_output(matches):
        done_or_doing = []
        for match in matches:
            if re.match(r"[A-Z]{4} [0-9]{4}", match) != None:
                done_or_doing.append(re.sub(' ', '', match))

        return done_or_doing

    def open_and_extract(file):
        try:
            #print("Attempting to read file {}".format(filename))
            pdf_file = BytesIO((file.read()))
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            num_pages = read_pdf.getNumPages()
            array_of_courses = []
            print("Num Pages {}".format(num_pages))
            # pdb.set_trace()
            for num in range(num_pages):
                print("Parsing page {}".format(num))
                page = read_pdf.getPage(num)
                page_content = page.extractText()
                matches = re.findall(r'[A-Z]{4} *[0-9]{4}', page_content)
                array_of_courses.extend(PdfParser.filter_output(matches))
            return { "Courses":  array_of_courses }
        except:
            return { "Courses":  [] }
