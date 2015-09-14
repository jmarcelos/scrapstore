# -*- coding: utf-8 -*-

from crawl import Crawler
from lxml import html as lhtml
from datetime import datetime
import json

class Archive:
	archive_host = "http://web.archive.org"
	archive_save = archive_host+"/save/"
	archive_search = "http://archive.org/wayback/available?"
	timestamp_mask = '%Y%m%d%H%M%S'

	url = None
	url_archive = None
	date = None
	timestamp = None

	def __init__(self, url, url_archive=None, date=None):
		self.url = url
		self.url_archive = url_archive
		self.date = date

	def to_dict(self):
		return self.__dict__

	def save(self):
		html,headers = Crawler().get(self.archive_save+self.url)
		for header in headers.split("\r\n"):
			dados = header.split(": ")
			if dados[0] == "Content-Location":
				self.url_archive=self.archive_host+dados[1]
				self.timestamp = dados[1].split("/")[2]
				self.date = datetime.strptime(self.timestamp, self.timestamp_mask)
				self.date = self.timestamp
	
	def findOne(self):
		search = "url=%s&timestamp=%s" % (self.url,self.date.strftime(self.timestamp))
		html,headers = Crawler().get(self.archive_search+search)
		data = json.loads(html)
		self.url_archive = data['archived_snapshots']['closest']['url']
