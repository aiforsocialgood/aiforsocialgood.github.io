import os
import re
import json

from mako.template import Template
from mako.lookup import TemplateLookup

reg = "\$\{[^$]*\}"


def getAcceptedPapers(papers_dir, papers_pdf_link, posters_pdf_link):
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
        #print(lines)
        # all files need to have the same number of elements

        toks = [l.strip().split(':') for l in lines]
        
        infos = dict([(t[0], ':'.join(t[1:])) for t in toks])
        
        # information not in the file
        if "pdf" not in infos.keys():
            infos["pdf"] = '{}/{}.pdf'.format(papers_pdf_link, name)

        if "poster" not in infos.keys():
            infos["poster"] = '{}/{}.pdf'.format(posters_pdf_link, name)

        infos["id"] = id
        infos["name"] = name

        # Check that pdf and poster exists
        rootdir = os.path.dirname(os.getcwd())
        infos["pdf"] = insertIfExists(rootdir, infos["pdf"])
        infos["poster"] = insertIfExists(rootdir, infos["poster"])

        papers.append(infos)

    papers =  sorted(papers, key=lambda k: int(k['id']))
    papers =  sorted(papers, key=lambda k: k.get('category', ''))
    return papers


def insertIfExists(rootdir, basename, default=''):
    path = os.path.join(rootdir, basename)
    result = default
    if os.path.exists(path):
        result = basename
    return result


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
        if page_name in ['acceptedpapers', 'proposals']:
            attributes["papers"] = getAcceptedPapers(
                attributes["papers_dir"],
                attributes["papers_pdf_link"],
                attributes["posters_pdf_link"],
            )

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
        print('Error')
        print(page_name, e)

        ctc = re.findall(reg, open(page_name).read())
        atr = attributes.keys()
        #for c in ctc:
        #    c = c.strip("${}")
        #    if c not in atr:
        #        print(page_name, " : ", c,  " is missing")
        # print("footer", re.findall(reg, open("footer").read()))
        # print("header", re.findall(reg, open("header").read()))
