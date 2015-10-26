# coding=utf-8

from helper.crawler import Crawler
from datetime import datetime
import json
from re import sub


class Archive(Crawler):
    archive_host = "http://web.archive.org"
    archive_save = archive_host+"/save/"
    archive_search = "http://archive.org/wayback/available?"
    timestamp_mask = '%Y%m%d%H%M%S'


    def get_archived_url(self, url):
        search_archive_url = None
        doc, headers = self.crawl_HTML_with_headers(self.archive_save+url)

        for header in headers.split("\r\n"):
            dados = header.split(": ")
            if dados[0] == "Content-Location":
                timestamp = dados[1].split("/")[2]
                date = datetime.strptime(timestamp, self.timestamp_mask)
                search = "url=%s&timestamp=%s" % (url,date.strftime(timestamp))
                search_archive_url = self.archive_search+search
                break

        return self.get_url_from_archive_content(search_archive_url)


    def get_url_from_archive_content(self,url):
        json_data = self.crawl_json(url)
        return json_data['archived_snapshots']['closest']['url']
