#!/usr/bin/env python

import os, sys
import argparse

from markuploader import load
from rapydcompiler import Parser, __file__ as rapydml_compiler_path

parser = argparse.ArgumentParser(description='Pre-Compiler for XML/HTML-like markup. \
Simplifies writing new web pages and XML by making format more human-readable as well \
as reducing redundant syntax.')

parser.add_argument('input', metavar='INPUT', type=argparse.FileType('r'), 
					help='The RapydML file to compile')
parser.add_argument('--no-acknowledgement', dest='no_ack', action='store_true', default=False,
					help="Avoid the string stating that page was generated using RapydML")

# add all available markup languages to the help menu
rapydml_dir = os.path.abspath(os.path.dirname(rapydml_compiler_path))
available_markup = os.listdir(os.path.join(rapydml_dir, 'markup'))
group = parser.add_mutually_exclusive_group()
for lang in available_markup:
	group.add_argument('--%s' % lang, action='store_true', default=False,
						help='Parse the file using %s markup syntax' % lang.upper())

args = parser.parse_args()

# figure out which markup the user selected, default to HTML if none specified
markup = None
for lang in available_markup:
	if getattr(args, lang):
		markup = lang
if markup is None:
	markup = 'html'

# load correct markup template
markup_lang = load(markup, rapydml_dir)

# begin markup
html = Parser(markup_lang)
filename = args.input.name.rsplit('.', 1)[0]
with open(filename + '.html', 'w') as output:
	if not args.no_ack:
		output.write('<!DOCTYPE html>\n')
	output.write(html.parse(args.input.name))
