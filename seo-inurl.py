from bs4 import BeautifulSoup
import urllib2, re, csv, time

def get_baidu_records_count(inurl):
	host = 'lietou.com'
	url = 'http://www.baidu.com/s?wd=site%3A' + host + '+' +'inurl%3A' + inurl
	try:
		data  = urllib2.urlopen(url)
		html = data.read()
		soup = BeautifulSoup(html)
		sitetip = soup.find('span',{'class':'nums'})
		if sitetip.is_empty_element == False:
			text = sitetip.string
			text = text.replace(',','')
			numPattern = re.compile(r'\d+')
			m = numPattern.search(text)
			strCn = m.group(0)
			return int(strCn)			
		else:
			return 0
	except:
		return 'error'


# read website from a txt file and save them as a list

filename1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
filename2 = str(filename1) + '-inurl.csv'
writer=csv.writer(open(filename2, 'wb'))
writer.writerow(['inurl', 'count'])
for inurl in open("inurl.txt"):
	inurl =  inurl.rstrip()
	count = get_baidu_records_count(inurl)
	writer.writerow([inurl, count])
