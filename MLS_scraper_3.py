from urllib.request import urlopen
from bs4 import BeautifulSoup

# commented out the file writing parts and just saved the URLs into
# a Python list instead. This will run faster than reading a file. 
# Writing to a file was good for checking the URLs.
# Here I read the first data item I wanted to scrape -- the 
# player's name. See screen capture: I saw it working for multiple pages 
# and then exited with Control-C. 

html = urlopen("http://www.mlssoccer.com/players")
bsObj = BeautifulSoup(html, "html.parser")
# f = open("mls_urls.txt", 'a')
p = open("mls_players.txt", 'a')
player_list = []

# looking at this tag to get the next page URL --
# <a title="Go to next page" href="/players?page=1">next ›</a>
def get_next_page(html, bsObj):
    next_page = bsObj.find( "a", {"title":"Go to next page"} )
    if next_page and ('href' in next_page.attrs):
        partial = str(next_page.attrs['href'])
        new_url = "http://www.mlssoccer.com" + partial
        html = urlopen(new_url)
        bsObj = BeautifulSoup(html, "html.parser")
        get_player_pages(html, bsObj)
    else:
        print("Done!")

# run this on each page to get player detail page links
def get_player_pages(html, bsObj):
    global player_list
    tag_list = bsObj.findAll( "a", {"class":"row_link"} )
    for tag in tag_list:
        if 'href' in tag.attrs: 
            # f.write(str(tag.attrs['href']) + "\n")
            player_list.append(str(tag.attrs['href']))
        # else:
            # f.write("no href\n")
    get_next_page(html, bsObj)

def get_player_details(player_list):
    for player in player_list:
        new_url = "http://www.mlssoccer.com" + player
        html = urlopen(new_url)
        bsObj = BeautifulSoup(html, "html.parser")
        print(bsObj.find( "div", {"class":"title"} ))
        # need to get_text
        # need to add delay 

get_player_pages(html, bsObj)
get_player_details(player_list)
# f.close()
p.close()
