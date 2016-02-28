from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.mlssoccer.com/players")
bsObj = BeautifulSoup(html, "html.parser")
f = open("mls_urls.txt", 'a')

tag_list = bsObj.findAll( "a", {"class":"row_link"} )

# first get the URLS from one page and write them to a file
for tag in tag_list:
    if 'href' in tag.attrs: 
        f.write(str(tag.attrs['href']) + "\n")
    else:
        f.write("no href\n")

f.close()
