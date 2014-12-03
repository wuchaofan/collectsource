#coding: utf-8
from django.shortcuts import render
import os
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
import urllib2
# Create your views here.
@cache_page(60*30)		
def index(request):
	meituan_url='http://sh.meituan.com/dianying/zuixindianying'
	meituan=requests.get(meituan_url)

	meituanhtml=BeautifulSoup(meituan.text)
	div=meituanhtml.find('div',{'class':'movies-container'})
	if div:
		print '----start----'
		divcells=div.findAll('div',{'class':'movie-cell'})
		titles=[]
		for index,cell in enumerate(divcells):
			h3=cell.find('h3',{'class':'movie-cell__title'})
			rate = cell.find('strong',{'class':'rates'})
			img = cell.find('img')
			imgurl=''
			if img.get('data-src'):
				imgurl=img['data-src']
			else:
				imgurl=img['src']
			titles.append({'name':h3.text,'rate':u'美团 '+rate.text+u'分','img': imgurl,'id':index})
		return render_to_response('mobile.html',{'titles':titles,'header':u'热映电影','activetab':'filmtab1'})

@cache_page(60*30)		
def hotfilm(request):
	meituan_url='http://sh.meituan.com/dianying/zuixindianying/coming'
	meituan=requests.get(meituan_url)

	meituanhtml=BeautifulSoup(meituan.text)
	div=meituanhtml.find('div',{'class':'movies-container'})
	if div:
		print '----start----'
		divcells=div.findAll('div',{'class':'movie-cell'})
		titles=[]
		for index,cell in enumerate(divcells):
			h3=cell.find('h3',{'class':'movie-cell__title'})
			
			p=cell.find('p',{'class':'release'})
			img = cell.find('img')
			imgurl=''
			if img.get('data-src'):
				imgurl=img['data-src']
			else:
				imgurl=img['src']
			titles.append({'name':h3.text,'rate':p.text,'img': imgurl,'id':index})
		return render_to_response('mobile.html',{'titles':titles,'header':u'即将上映','activetab':'filmtab2'})

@cache_page(60*30)		
def comingfilmbyname(request):
	name=request.GET.get('name',None)
	if name:
		douban_se='http://movie.douban.com/subject_search?search_text={0}&cat=1002'.format(urllib2.quote(name.encode("utf-8")))
		douban_rx=requests.get(douban_se)
		douban_html = BeautifulSoup(douban_rx.text)
		trs = douban_html.findAll('tr',{'class':'item'})
		if trs:
			# for item in tables[0:1]:
			div_pl2=trs[0].find('div',{'class':'pl2'})
			a = div_pl2.find('a')
			attrs= ''
			introdetail=''
			if a:
				reul =a['href']
				print reul
				detail = requests.get(reul)
				detail_html = BeautifulSoup(detail.text)
				div_info = detail_html.find('div',{'id':'info'})
				if div_info:
					attrs = div_info.text.split('\n')
				intro = detail_html.find('span',{'class':'all'})
				if not intro:
					div_intro = detail_html.find('div',{'id':'link-report'})
					introdetail = div_intro.text
				else:
					introdetail=intro.text
			return render_to_response('comingfilmbyname.html',{'attrs':attrs,'intro':introdetail})


