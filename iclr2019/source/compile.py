import os
import re
import json

from mako.template import Template
from mako.lookup import TemplateLookup

reg = "\$\{[^$]*\}"


def getAcceptedPapers(papers_dir, papers_pdf_link):
    '''
    Retrieve the list of accepted papers from 
    directory defined in the .json file

    Name of the .txt file should contain the id
    '''
    papers = [] 
    filenames = os.listdir(papers_dir)
    filenames = [f for f in filenames if '.txt' in f]
    
    for filename in filenames:
        id = filename.split('_')[0]
        name = filename.split('.')[0]

        finput = open('{}/{}'.format(papers_dir, filename))
        lines = finput.readlines()
        infos = dict([tuple(l.strip().split(':')) for l in lines])
        
        # information not in the file
        if "pdf" not in infos.keys():
            infos["pdf"] = '{}/{}.pdf'.format(papers_pdf_link, name)

        infos["id"] = id
        infos["name"] = name

        # Check that pdf exists
        rootdir = os.path.dirname(os.getcwd())
        pdffile = os.path.join(rootdir, infos['pdf'])
        if not os.path.exists(pdffile):
            infos["pdf"] = ""
        papers.append(infos)
    return papers

def getScheduleItems():
    # see schedule template
    pass

mylookup = TemplateLookup(directories=['.', '../bio'],
                          strict_undefined=False,
                          input_encoding='utf-8')

# Load custom attributes from json file
custom = json.loads(open('custom.json').read())

# Get all sections
sections = ['proposals', 'home', 'schedule', 'faq',
            'acceptedpapers', 'cfp', 'organizers',
            'guidelines', 'pastworkshops']

for section_name in sections:

    attributes = custom['default'].copy()
    attributes.update(custom.get(section_name, {}))

    html = """<%include file="header"/>
              <%include file="{}"/>
              <%include file="footer"/>""".format(section_name)

    section = Template(html, lookup=mylookup, strict_undefined=False)

    try:

        # Retrieve accepted papers from directory
        if section_name == 'acceptedpapers':
            papers_dir = attributes['papers_dir']
            papers_pdf_link = attributes['papers_pdf_link']
            papers = getAcceptedPapers(papers_dir, papers_pdf_link)
            attributes['papers'] = papers

        # Generating the different .htm files
        s = section.render(**attributes)
        outfile = open('../%s.htm' % section_name, "w")
        outfile.write(str(s))
        outfile.close()

        # Copy home as index
        if section_name == 'home':
            outfile = open('../index.htm', "w")
            outfile.write(str(s))
            outfile.close()


    except Exception as e:
        print(section_name, e)

        ctc = re.findall(reg, open(section_name).read())
        atr = attributes.keys()
        for c in ctc:
            c = c.strip("${}")
            if c not in atr:
                print(section_name, " : ", c,  " is missing")
        # print("footer", re.findall(reg, open("footer").read()))
        # print("header", re.findall(reg, open("header").read()))
