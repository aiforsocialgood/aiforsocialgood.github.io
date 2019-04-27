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

mylookup = TemplateLookup(directories=['.', '../bio', '..'],
                          strict_undefined=False,
                          input_encoding='utf-8')

# Load custom attributes from json file
custom = json.loads(open('custom.json').read())

# Get all pages
pages = ['proposals', 'home', 'schedule',
            'acceptedpapers', 'cfp', 'organizers',
            'guidelines_areachairs', 'guidelines_reviewers',
            'pastworkshops', 'futureworkshops',
            'faq_general', 'faq_reviewers', 'faq_fundings',
            'faq_submission'
            ]

for page_name in pages:

    attributes = custom['default'].copy()
   
    attributes.update(custom.get(page_name, {}))

    html = """<%include file="header"/>
              <%include file="{}"/>
              <%include file="footer"/>""".format(page_name)

    page = Template(html, lookup=mylookup, strict_undefined=False)

    try:

        # Retrieve accepted papers from directory
        if page_name == 'acceptedpapers':
            papers_dir = attributes['papers_dir']
            papers_pdf_link = attributes['papers_pdf_link']
            papers = getAcceptedPapers(papers_dir, papers_pdf_link)
            attributes['papers'] = papers

        if page_name == 'proposals':
            papers_dir = attributes['papers_dir']
            papers_pdf_link = attributes['papers_pdf_link']
            papers = getAcceptedPapers(papers_dir, papers_pdf_link)
            attributes['papers'] = papers

        # Generating the different .htm files
        s = page.render(**attributes)
        outfile = open('../%s.htm' % page_name, "w")
        outfile.write(str(s))
        outfile.close()

        # Copy home as index
        if page_name == 'home':
            outfile = open('../index.htm', "w")
            outfile.write(str(s))
            outfile.close()

    except Exception as e:
        print(page_name, e)

        ctc = re.findall(reg, open(page_name).read())
        atr = attributes.keys()
        #for c in ctc:
        #    c = c.strip("${}")
        #    if c not in atr:
        #        print(page_name, " : ", c,  " is missing")
        # print("footer", re.findall(reg, open("footer").read()))
        # print("header", re.findall(reg, open("header").read()))
