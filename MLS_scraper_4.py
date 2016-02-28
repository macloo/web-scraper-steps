from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
# time will allow a delay in program execution

# added 2 time delays: One for each page while scraping the URLs, 
# and one for each page while scraping the text about each player 
# also added get_text() in the get_player_details() function 

html = urlopen("http://www.mlssoccer.com/players")
bsObj = BeautifulSoup(html, "html.parser")
p = open("mls_players.txt", 'a')
player_list = []

# player links are on multiple pages -- get the next page URL
def get_next_page(html, bsObj):
    next_page = bsObj.find( "a", {"title":"Go to next page"} )
    if next_page and ('href' in next_page.attrs):
        partial = str(next_page.attrs['href'])
        new_url = "http://www.mlssoccer.com" + partial
        html = urlopen(new_url)
        bsObj = BeautifulSoup(html, "html.parser")
        get_player_pages(html, bsObj)
    else:
        print("Done collecting URLs ...")

# run this on each page to get player detail page links
def get_player_pages(html, bsObj):
    global player_list
    tag_list = bsObj.findAll( "a", {"class":"row_link"} )
    for tag in tag_list:
        if 'href' in tag.attrs: 
            player_list.append(str(tag.attrs['href']))
        # else:
            # f.write("no href\n")
    # delay program for 1 second
    time.sleep(1)
    get_next_page(html, bsObj)

def get_player_details(player_list):
    for player in player_list:
        new_url = "http://www.mlssoccer.com" + player
        html = urlopen(new_url)
        bsObj = BeautifulSoup(html, "html.parser")
        title = (bsObj.find( "div", {"class":"title"} ))
        print(title.get_text())
        # # delay program for 2 seconds
        time.sleep(2)

# collect all the URLs
get_player_pages(html, bsObj)
# collect text from each player detail page
get_player_details(player_list)
p.close()
