#-*- coding: UTF-8 -*-  
# 还差两个问题，第一如何解决csv输入中文的问题，第二如何解决翻页查询的问题  
from bs4 import BeautifulSoup
import urllib2, re, csv, time, sys
reload(sys) 
sys.setdefaultencoding( "utf-8" ) 


def get_links(host, keyword, pn):
	url = 'http://www.baidu.com/s?wd=' + keyword + '&pn=' + str(pn)
	try:
		data  = urllib2.urlopen(url, timeout = 20)
		html = data.read()
		soup = BeautifulSoup(html)
		links = soup.find_all('span',text=re.compile(host))
		return links
	except:
		print "connection error"

def get_linkrank(links, keyword, pn):
	linklist = []
	for link in links:
		link_table = link.find_parents("table")
		table_id = link_table[0]
		try:
			rank = table_id['id']
			linkcontent = link.string
			linkrow = [keyword, rank, linkcontent]
			linklist.append(linkrow)
		except:
			pass	
	return linklist

def get_linklist(host, keyword):
	list = []
	pn = 0
	while pn < 100:
		links = get_links(host, keyword, pn)
		ranklist = get_linkrank(links, keyword, pn)
		list.extend(ranklist)
		pn += 10
	return list

# read website from a txt file and save them as a list

filename1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
filename2 = str(filename1) + '-rank.csv'
writer=csv.writer(open(filename2, 'wb',))
writer.writerow(['keyword', 'rank','url&date'])
keyword_count ,result_count = 1, 1
host = 'lietou.com'
with open("keyword.txt") as file:
	for keyword in file:
		keyword =  keyword.rstrip()
		print 'Print No %s keyword: %s' % (keyword_count, keyword)
		keyword_count += 1
		rank = get_linklist(host, keyword)
		for i in rank:
			i[0] = i[0].decode('utf8')
			writer.writerow(i)
			print '%s at No %s' % (i[0], i[1])
			result_count += 1
print 'Finished'
