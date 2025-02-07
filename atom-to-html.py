#!/usr/bin/env python3

import os
import sys
import atoma
import argparse
from airium import Airium
from datetime import datetime, timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def make_html(feed):
    air = Airium()
    air('<!DOCTYPE html>')
    lang = "en"
    if feed.lang:
        lang = feed.lang
    with air.html(lang=lang):
        with air.head():
            air.meta(charset="utf-8")
            air.title(_t=feed.title)
            if feed.link:
                air.link(href=feed.link, type="application/atom+xml", rel="alternate", title=feed.title)
        with air.body():
            if feed.link:
                with air.p(klass="link"):
                    air.a(href=feed.link, _t=feed.title)
            with air.div(klass="main"):
                with air.p(klass="description", style="background-color: rgb(220,220,220); margin: 1em;"):
                    air.strong(_t="Description: ")
                    air(feed.description)
                air.h1(_t="Items")
                for item in feed.items:
                    with air.div(klass="item", style="border: 1px solid white; margin: 1em; background-color: rgb(231,254,255);"):
                        with air.p():
                            air.strong(_t=item.title)
                            air(': ')
                            date = utc_to_local(item.published)
                            air(date.strftime("%A, %B %d, %Y %T %z"))
                            if item.updated:
                                date = utc_to_local(item.updated)
                                air(" Updated: {0}".format(date.strftime("%A, %B %d, %Y %T %z")))
                        with air.ol():
                            for author in item.authors:
                                with air.li():
                                    air("Author: {0}".format(author.name))
                                    if author.email:
                                        air.a(href="mailto:{0}".format(author.email), _t=" Email")
                                    if author.url:
                                        air.a(href=author.uri, _t=" Link")
                        with air.ol():
                            for contributor in item.contributors:
                                with air.li():
                                    air("Contributor: {0}".format(contributor.name))
                                    if contributor.email:
                                        air.a(href="mailto:{0}".format(contributor.email), _t=" Email")
                                    if contributor.uri:
                                        air.a(href=contributor.uri, _t=" Link")
                        with air.div(klass="itemdesc"):
                            air(item.content)
                        with air.div(klass="links", style="background-color: rgba(0,128,64,.25);"):
                            with air.ol():
                                for link in item.links:
                                    with air.li():
                                        title = "Link"
                                        if link.title:
                                            title = link.title
                                        air.a(href=link.href, _t=title)
    return str(air)

def atom2html(inf, outf):
    outf.write(make_html(atoma.parse_atom_bytes(inf.read())))
    outf.write("\n")

parser = argparse.ArgumentParser(description='Convert Atom to HTML')

parser.add_argument('-i', '--input', metavar='INFILE', type=str, nargs=1, default='', help='Specify INFILE as Atom input file, defaults to stdin')
parser.add_argument('-o', '--output', metavar='OUTFILE', type=str, nargs=1, default='', help='Specify OUTFILE as HTML output file, defaults to stdout')

args = parser.parse_args()

if (len(args.input) > 0) and (len(args.output) > 0):
    with open(args.input[0], 'rb') as inf:
        with open(args.output[0], 'w') as outf:
            atom2html(inf, outf)
    sys.exit(0)
elif len(args.input) > 0:
    with open(args.input[0], 'rb') as inf:
        atom2html(inf, sys.stdout)
    sys.exit(0)
elif len(args.output) > 0:
    with open(args.output[0], 'w') as outf:
        atom2html(sys.stdin.buffer, outf)
    sys.exit(0)
else:
    atom2html(sys.stdin.buffer, sys.stdout)
    sys.exit(0)
