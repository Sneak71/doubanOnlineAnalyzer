#!/usr/bin/python
#-*- coding:utf-8 -*-

import subprocess
import sys
import time
import json
import jieba
import codecs
import os

def runSpider(spiderName, online1st, jsonName):
	'''using scrapy to get infomation
	'''
	rc = subprocess.call([
				'scrapy', 'crawl', spiderName,
				'-a', 'online1st=%s'%online1st, 
				'-o', jsonName
			])
	return rc

def runAnalyze(jsonName):
	'''calculate the frequency of words
	'''
	print "begin to calculate the frequency of words~~"
	wc = sorted(_genWordCount(jsonName).iteritems(), key=lambda item:item[1],reverse=True) 
	json.dump(
		{item[0]:item[1] for item in wc},
		codecs.open("%s.wc.tmp"%jsonName, "w", 'utf-8'), 
		ensure_ascii=False
	)
	os.rename("%s.wc.tmp"%jsonName, "%s.wc"%jsonName)
	print "analyse finished~"

def _genWordCount(filename, nonsense=[]):
	''' this method is used to abstract the words from the text
		and calculate the count of text
	'''
	wc = {}  # words' count
	with open(filename,"r") as f:
		resps = json.load(f)
		for resp in resps:
			linewc = jieba.cut(resp["content"].strip(), cut_all=True)
			for item in linewc:
				if item in nonsense:
					continue
				if item.strip():
					wc.setdefault(item,0)
					wc[item] +=1
	return wc

if __name__ == '__main__':
	print sys.argv
	if len(sys.argv) > 3:
		spiderName, online1st, jsonName = sys.argv[1], sys.argv[2],sys.argv[3]
		#rc = runSpider(spiderName, online1st, jsonName)
		#if rc == 0:
			#runAnalyze(jsonName)
		#else:
			#print "Opssssss.... the returnCode is %d, maybe there is something wrong~~" % rc
		runAnalyze(jsonName)
		