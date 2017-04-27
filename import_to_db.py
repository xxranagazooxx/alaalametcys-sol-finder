#!/usr/bin/env python
import sys
import json
import time
import ConfigParser
import googleapiclient.discovery as gapid

from pprint import pprint
import models as db

config = ConfigParser.ConfigParser()
config.read("config.cfg")
apikey = config.get("customsearch-main", "apikey")
cx = config.get("customsearch-main", "cx")

DEBUG = True

def get_hits(q_dict, preview=False):
    """
    get data from custom search and select items to return 

    # q_dict = {"module" : "section bank", "section": "c/P", "num": 17}
    # example: query = "section bank c/p #17"
    """

    ret = []
    q_str = ""

    # if query is dict, transform
    if not isinstance(q_dict, dict):
        raise Exception("Query must be a dict")

    tmp = "aamc %(module)s %(section)s %(num)s" % q_dict
    q_str = tmp.lower()

    if DEBUG:
        print ">>> querying: ", q_str

    # build service
    service = gapid.build("customsearch", "v1", developerKey=apikey)
    res = service.cse().list(
        q=q_str,
        cx=cx).execute()

    if preview:
        for r in res.get('items'):
            print r.get('title')
            print r.get('link')

    # rustle up important bits
    for r in res.get('items'):
        tmp = {}
        tmp.update({'title': r.get('title')})
        tmp.update({'link': r.get('link')})
        tmp.update({'snippet': r.get('snippet')})
        # add filtering
        tmp.update(parse_hits(q_dict, r))
        ret.append(tmp)
    return ret

def parse_hits(query, hit):
    """
    helper to parse and filter given hits 
    """

    suspect = str(query.get('num')) not in hit.get('title')
    return {'suspect': suspect}

def populate_db():

    section = "CARS"
    module = "FL2"

    for num in range(1, 53+1):
        hits = get_hits({
                "section": section,
                "module": module,
                "num" : num})
        for hit in hits:
            db.add_solution(section, module, num, hit)
        time.sleep(2)

