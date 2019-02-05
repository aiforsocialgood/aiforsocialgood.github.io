## -*- coding: utf-8 -*-
import re
import os
import sys
import json

from mako.template import Template
from mako.lookup import TemplateLookup

reg = "\$\{[^$]*\}"

mylookup = TemplateLookup(directories=['.', '../bio', '../abstract'], strict_undefined=False, input_encoding='utf-8')

# Load custom attributes from json file
custom = json.loads(open('custom.json').read())


# Get all sections
sections = ['proposals', 'home', 'schedule', 'acceptedpapers', 'cfp', 'organizers']

for section_name in sections :
	attributes = custom['default'].copy()
	attributes.update(custom.get(section_name, {}))
	
	html = """<%include file="header"/> <%include file="{}"/>  <%include file="footer"/>""".format(section_name)
	
	section = Template(html, lookup=mylookup, strict_undefined=False)
	
	try : 
		s = section.render(**attributes)
		outfile = open('../%s.htm' % section_name, "w")
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
		#print("footer", re.findall(reg, open("footer").read()))
		#print("header", re.findall(reg, open("header").read()))




