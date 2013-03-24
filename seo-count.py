from bs4 import BeautifulSoup
import urllib2, re, csv, time

def get_baidu_records_count(host):
	url = 'http://www.baidu.com/s?wd=site%3A' + host
	try:
		data  = urllib2.urlopen(url)
		html = data.read()
		soup = BeautifulSoup(html)
		sitetip = soup.find('p',{'class':'site_tip'})
		if sitetip.is_empty_element == False:
			strong = sitetip.find('strong')
			text = strong.string
			text = text.replace(',','')
			numPattern = re.compile(r'\d+')
			m = numPattern.search(text)
			strCn = m.group(0)
			return int(strCn)
		else:
			return 0
	except:
		return 'error'


# read website from a txt file and save them to a csv file.

filename1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
filename2 = str(filename1) + '.csv'
writer=csv.writer(open(filename2, 'wb'))
writer.writerow(['site', 'count'])
for site in open("site.txt"):
	site =  site.rstrip()
	count = get_baidu_records_count(site)
	writer.writerow([site, count])
	print site + ' Done!'
print 'Finished!'
	