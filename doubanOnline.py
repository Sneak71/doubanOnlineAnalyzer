#!/usr/bin/python
#-*- coding:utf-8 -*-

import web
from web import form
from web.contrib.template import render_jinja
import urllib2
from lxml import etree
import subprocess
import os
import json

urls = (
	"/douban/online", "doubanOnline",
	"/douban/online/query", "doubanOnlineWC"
)

render = render_jinja("templates", encoding="utf-8")

search = form.Form(
	form.Textbox(name="onlineIndex",value="你想查看的线上活动的主页是什么呢？"),
)

class doubanOnline(object):
	def GET(self):
		f = search()
		return render.doubanOnline(form=f)

	def POST(self):
		f = search()
		if not f.validates():
			return render.doubanOnline(form=f)
		else:
			first, name, topic = self._getFirstPage(f["onlineIndex"].value)
			temp = f["onlineIndex"].value.split("/")
			jsonName = temp[-1] if temp[-1] else temp[-2]
			# call run.py to scrapy and analyze
			scrapy = subprocess.Popen([
				'python', 'run.py', 'doubanOnline', 
				first, '%s.json'%jsonName,
			])
			# return word's frequency - asyn
			return render.doubanOnline(form=f,  name=name, topic=topic, index=jsonName)
	
	def _getFirstPage(self, index):
		resp = urllib2.urlopen(index)
		html = resp.read()
		if not html: return ("", "Opssss......I don't know why the page is {0}, maybe something bad happens".format(resp.getcode()))
		tree = etree.HTML(html)
		first = tree.xpath("//div[@class='pic']/a/@href")[0]
		topic = tree.xpath("//div[@id='edesc_f']/text()")
		name = tree.xpath("head/title/text()")[0].strip()
		return (first, name, "<br />".join(topic))

class doubanOnlineWC(object):
	def GET(self):
		data = web.input()
		return open("%s.json.wc"%data["name"]).read() if os.path.exists("%s.json.wc"%data["name"]) else ""

if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()