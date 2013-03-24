#-*- coding: UTF-8 -*-  

from bs4 import BeautifulSoup
import urllib2, re, csv, time, sys
reload(sys) 
sys.setdefaultencoding( "utf-8" ) 

# 读取百度搜索结果页面，查询符合域名的span
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

# 根据查询到的span，查询所属的table，并将关键词、排名和收录域名储存到列表中
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

# 查询十页，将翻页检索到的内容存储到列表中
def get_linklist(host, keyword):
	list = []
	pn = 0
	while pn < 100:
		links = get_links(host, keyword, pn)
		ranklist = get_linkrank(links, keyword, pn)
		list.extend(ranklist)
		pn += 10
	return list

# 主程序，写到csv中的keyword是乱码，怎么解决？

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
			writer.writerow(i)
			print '%s at No %s' % (i[0], i[1])
			result_count += 1
print 'Finished'
