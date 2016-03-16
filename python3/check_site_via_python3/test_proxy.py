#! /usr/bin/env python3

import urllib3
import re
import sys
import os
#from influxdb import InfluxDBClient
import requests
import json
#<Check your real ip>
conn = urllib3.PoolManager()
t = conn.request('GET', 'ifconfig.io/all')
q = str(t.data)
ip = q.split('ip:')[1].split(' ')[0]
#</Check your real ip>
#<Definition variables>
prefix = "http://"
robots = "robots.txt"
mon_url="http://statreceiver.hrenbet.com/write?db=fbps"
http = urllib3.PoolManager()
#</Definition variables>
proxy_list = open("proxy_urls").readlines()
for proxy_list_string in proxy_list:
	proxy_port = proxy_list_string.split(':')[1]
	proxy_list_string = proxy_list_string.rstrip('\n')
	proxy_address = proxy_list_string.split(':')[0]
	proxy_string = prefix+proxy_address+':'+proxy_port
	proxy_hostname = proxy_list_string.split(':')[2]
	proxy = urllib3.ProxyManager(proxy_string)
	urls_list = open("domain_urls", 'r').readlines()
	for urls_list_string in urls_list:
		urls_list_string = urls_list_string.rstrip('\n')
		url_string = prefix+urls_list_string+'/'+robots
		site_via_proxy = proxy.request('GET', url_string)
		site_via_proxy_data = str(site_via_proxy.data)
		find_data_from_site = re.search('fon', site_via_proxy_data)
		if not find_data_from_site:
			find_fon = 0
		else:
			if str(find_data_from_site.group(0)) == 'fon':
				find_fon = 1

		data = "get,host_dmn=%(urls_list_string)s,host_proxy=%(proxy_hostname)s,src_ip=%(ip)s value=%(find_fon)s" %vars()
		requests.post(mon_url, data=data)
#
