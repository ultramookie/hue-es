#!/usr/bin/env python

import json
import datetime
import urllib
import urllib2
from pprint import pprint
from dateutil.tz import tzlocal
from elasticsearch import Elasticsearch

indexname = "hue"
doc_type = "hue"
config = "config.json"
elastichost='localhost:9200'

huelightdata = {}
huesensordata = {}

es = Elasticsearch(elastichost)

now = datetime.datetime.now(tzlocal())

month = now.strftime("%m")
year = now.strftime("%Y")
index = indexname + "-" + year + "-" + month

with open(config) as json_data:
    configjson = json.load(json_data)
    hubip = configjson['hubip']
    user = configjson['user']

baseurl = 'http://%s/api/%s' % (hubip,user)

lightsurl = '%s/lights' % baseurl
sensorsurl = '%s/sensors' % baseurl

req = urllib2.Request(lightsurl, None)
r = urllib2.urlopen(req)
lightsjson = json.loads(r.read())
r.close()

req = urllib2.Request(sensorsurl, None)
r = urllib2.urlopen(req)
sensorsjson = json.loads(r.read())
r.close()

for light in lightsjson:
  doc_type = "huelight"
  huelightdata['timestamp'] = now
  huelightdata['type'] = lightsjson[light]['type']
  huelightdata['name'] = lightsjson[light]['name']
  huelightdata['modelid'] = lightsjson[light]['modelid']
  huelightdata['manufacturername'] = lightsjson[light]['manufacturername']
  huelightdata['uniqueid'] = lightsjson[light]['uniqueid']
  huelightdata['swversion'] = lightsjson[light]['swversion']
  huelightdata['on'] = lightsjson[light]['state']['on']
  huelightdata['brightness'] = lightsjson[light]['state']['bri']
  if 'hue' in lightsjson[light]['state']:
    huelightdata['hue'] = lightsjson[light]['state']['hue']
  if 'sat' in lightsjson[light]['state']:
    huelightdata['saturation'] = lightsjson[light]['state']['sat']
  if 'effect' in lightsjson[light]['state']:
    huelightdata['effect'] = lightsjson[light]['state']['effect']
  if 'ct' in lightsjson[light]['state']:
    huelightdata['colortemp'] = lightsjson[light]['state']['ct']
  huelightdata['reachable'] = lightsjson[light]['state']['reachable']
  huelightdata['alert'] = lightsjson[light]['state']['alert']
  if 'colormode' in lightsjson[light]['state']:
    huelightdata['colormode'] = lightsjson[light]['state']['colormode']
  id="%s-%s" % (now,huelightdata['uniqueid'])
  es.index(index=index,doc_type=doc_type,id=id,body=huelightdata) 
