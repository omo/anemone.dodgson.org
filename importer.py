
import sys
import os
import os.path
import re
import json
import xml.etree.ElementTree
import zipfile
from collections import namedtuple
from bs4 import BeautifulSoup
import requests
from optparse import OptionParser

wp_domain = None

ns = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/'
}

Post = namedtuple('Post', ['title', 'body', 'date', 'slug', 'tags'])

def image_url_prefix():
    return 'https://{}.files.wordpress.com/'.format(wp_domain)

def site_url():
    return 'https://{}.wordpress.com/'.format(wp_domain)

def is_visible(elm: xml.etree.ElementTree):
    """"""
    post = elm.find('wp:post_type', ns).text == 'post'
    valid = elm.find('wp:status', ns).text not in ['draft', 'private', 'trash']
    categs = [e.get('nicename') for e in elm.findall('category')]
    to_publish = any([c for c in categs if c in ['letters', 'fragments']])
    return post and valid and to_publish

def make_post_from(elm):
    title = elm.find('title').text
    body = elm.find('content:encoded', ns).text
    slug = elm.find('wp:post_name', ns).text
    date = elm.find('wp:post_date', ns).text
    categs = [e.get('nicename') for e in elm.findall('category')
              if e.get('nicename') not in ['uncategorized']]
    return Post(title=title, body=body, slug=slug, date=date, tags=categs)

def extract_posts(file):
    """Get list of post object from the XML."""
    elm = xml.etree.ElementTree.parse(file).getroot()
    items = [i for i in elm.findall('channel/item') if is_visible(i)]
    return [make_post_from(i) for i in items]

def format_body(text):
    text = re.sub("""\[gallery.*\]""", "", text)
    text = text.replace(image_url_prefix(), '/images/')
    text = text.replace(site_url(), '/')
    text = "".join(["<p>" + p + "</p>" for p in text.split("\n\n") if p ])
    return text

def to_path(post):
    m = re.match(r"(\d+)-(\d+)", post.date)
    yyyy, mm = m.group(1), m.group(2)
    return os.path.join("content/post/%s/%s" % (yyyy, mm), post.slug + ".html")

def write_post(post, dry):
    path = to_path(post)
    tempalte = """+++
tags  = {}
title = {}
date  = "{}"
+++
{}
"""
    tags = "[" + ",".join(['"' + t + '"' for t in post.tags]) + "]"
    text = tempalte.format(tags, json.dumps(post.title), post.date, format_body(post.body))
    if dry:
        print("To Write: %s" % path)
    else:
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        open(path, "w").write(text)


def extract_links(file):
    posts = extract_posts(file)
    links = []
    for p in posts:
        soup = BeautifulSoup(p.body, "html.parser")
        links = links + [i['src'] for i in soup.find_all('img')]
    print(links)
    return links

def fetch_image_link(url):
    file_path = url.replace(image_url_prefix(), './static/images/')
    dir_path = os.path.dirname(file_path)
    if os.path.exists(file_path):
        return
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    print(file_path)
    r = requests.get(url)
    open(file_path, "wb").write(r.content)


def list_xml(zip: zipfile.ZipFile):
    return [ zip.open(n) for n in zip.namelist() if n.endswith(".xml") ]

parser = OptionParser()
parser.add_option("-w", "--wp", dest="wp_domain",  metavar="DOMAIN")
parser.add_option("-f", "--file", dest="file",  metavar="FILE")
parser.add_option("-c", "--command", dest="command",  metavar="COMMAND")
parser.add_option("-D", "--dry", dest="dry",  action="store_true")
(options, args) = parser.parse_args()

wp_domain = options.wp_domain

if "convert" in options.command:
    z = zipfile.ZipFile(options.file)
    for f in list_xml(z):
        for p in extract_posts(f):
            write_post(p, options.dry)
elif "fetch" in options.command:
    z = zipfile.ZipFile(options.file)
    for f in list_xml(z):
        for l in extract_links(z.open(f)):
            fetch_image_link(l)
else:
    print("specify command with --command")