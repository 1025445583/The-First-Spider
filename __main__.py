import requests
from bs4 import BeautifulSoup  
import time
import re
def get_muen(url):
	response = requests.get(url)
	soup =  BeautifulSoup(response.text,'html.parser')
	urls = soup.select('.clearfix')
	
	urls = soup.find_all('a',href=re.compile('/Novel'))[1:-6]
	#print(urls)

	index = []
	for i in urls:
		index.append('http://book.sfacg.com'+i['href'])
	#urlss = urls.find_all()

	return index


def get_content(url):
	response = requests.get(url)

	soup = BeautifulSoup(response.text, 'html.parser') 

	title = soup.select('.article-title')[0].text
	
	content = '\n'
	for i in soup.select('.article-content p'):

		content = content + i.text +'\n'
	return title + content + '\n\n\n\n   '





def get_index(url='http://book.sfacg.com/List/default.aspx?PageIndex=1'):
	
	novel = []

	actor = []

	content = []

	urls = []

	response = requests.get(url)

	soup =  BeautifulSoup(response.text,'html.parser')

	name = soup.find_all('a',target = '_blank',style = 'font-size: 14px; color: #FF6600;')
	for i in name:
		novel.append(i.text)
		urls.append(i.get('href'))

	for j in soup.find_all('a',id = re.compile('ContentMain_rnlv___NovelList_AuthorLink_')):
		actor.append(j.text)

	for l in soup.find_all('ul',class_='Comic_Pic_List'):
		content.append(l.find_all('li')[1].text.split(' ')[-1])

	for k in range(20):
		print(str(k) + ' ' + novel[k] + '\n   作者：' + actor[k] + '\n   简介：' + content[k] + '\n\n\n')
	return urls

info = []
urls = []

url_muen = []
num = 1
urls = get_index()
print('上一页请输入up，下一页请输入dn\n')
bookname = input('请输入需下载的小说序号（如需下载特定小说请输入21）:')
url='http://book.sfacg.com/List/default.aspx?PageIndex=1'
#while info == []:
while (bookname == 'dn' or bookname == 'up'):
	if bookname == 'dn':
		num += 1
		url = 'http://book.sfacg.com/List/default.aspx?PageIndex=%d'%num
		urls = get_index(url)
		
	elif bookname == 'up':
		num -= 1
		url = 'http://book.sfacg.com/List/default.aspx?PageIndex=%d'%num
		urls = get_index(url)
		
	
	print('上一页请输入up，下一页请输入dn\n')
	bookname = input('请输入需下载的小说序号（如需下载特定小说请输入21）:')
	


if (1<=int(bookname)<=20):
	bookname = int(bookname)
	print('ok')
	url_index = 'http://book.sfacg.com'+urls[bookname]+'MainIndex/'
elif (int(bookname)>20):
	url_index = input('请输入需下载的小说目录网址：')

url_muen = get_muen(url_index)
n = 1
length = len(url_muen)
for j in url_muen:
	print('正在下载：' + '%.2f'%(n/length*100) + '%')
	n+=1
	content = get_content(j) 
	f = open('F:/novel.txt', 'a',encoding = 'utf-8')
	f.write(content)
	f.close()
	time.sleep(1)




