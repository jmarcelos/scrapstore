# -*- coding: utf-8 -*-
import StringIO
import pycurl
import logging


class Crawler:
    def __init__(self,timeout=1):
        self.timeout = timeout

    def get(self,url, post=None):
        body = StringIO.StringIO()
        headers = StringIO.StringIO()

        curl = pycurl.Curl() 
        curl.setopt( pycurl.URL, str(url) ) 
        if post:            
            curl.setopt(pycurl.POST,1) 
            curl.setopt(pycurl.POSTFIELDS,post)
        curl.setopt( pycurl.WRITEFUNCTION, body.write ) 
        curl.setopt( pycurl.HEADERFUNCTION, headers.write )
        curl.setopt( pycurl.FOLLOWLOCATION, self.timeout ) 
        # curl.setopt( pycurl.TIMEOUT, self.timeout )
        try:
            curl.perform()
        except Exception, msg:
            print "erro!!!", url, msg
            logging.error("Nao foi possivel buscar [%s] - [%s]" % (url, msg))
            return None
        content = body.getvalue()
        headers = headers.getvalue()

        body.close()
        return content,headers

