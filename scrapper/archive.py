# -*- coding: utf-8 -*-

from crawl import Crawler
from lxml import html as lhtml

def archive(url):
	archive_host = "http://web.archive.org"
	archive_save = archive_host+"/save/"
	html,headers = Crawler().get(archive_save+url)
	for header in headers.split("\r\n"):
		dados = header.split(": ")
		if dados[0] == "Content-Location":
			return archive_host+dados[1]
	return ""
	