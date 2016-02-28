from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

# Here I disabled the function that gets all URLs - for testing purposes
# Added .get_text() for all 6 details I want to capture
# Ran it and found an error: If a tag is missing, e.g. player has no position 
# or player has no Twitter - script throws an AttributeError and stops.
# So I wanted to add a try/except but I didn't want to add it 6 times.
# I wrote my 6 details into a list. Then looped over the list with 
# a new try/except. If there is an AttributeError, I write "None" --
# this is all inside get_player_details() function 
# This works (see MLS_scraper_5.png), but I need to get rid of Age: and 
# Birthplace: text.

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
    # disable for testing - use only first page URLs 
    # get_next_page(html, bsObj)

def get_player_details(player_list):
    for player in player_list:
        new_url = "http://www.mlssoccer.com" + player
        html = urlopen(new_url)
        bsObj = BeautifulSoup(html, "html.parser")
        player_details = []
        title = bsObj.find( "div", {"class":"title"} )
        # div class title (text) player's full name
        team = bsObj.find( "div", {"class":"club"} )
        # div class club (text) team
        position = bsObj.find( "div", {"class":"position"} )
        # div class position (text) position
        birthday = bsObj.find( "div", {"class":"age"} )
        # <div class="age"><span class="category">Age:</span>
        # 23 (10/21/1992)</div>
        birthplace = bsObj.find( "div", {"class":"hometown"} )
        # <div class="hometown"><span class="category">Birthplace:</span>
        # Barranquilla, Colombia</div>
        twitter = bsObj.find( "div", {"class":"twitter_handle"} )
        # <div class="twitter_handle"><a 
        # href="https://twitter.com/Olmesgarcia13" 
        # class="twitter_link">@Olmesgarcia13</a></div>

        player_details = [title, team, position, birthday, birthplace,
        twitter]
        for detail in player_details:
            try:
                print( detail.get_text() )
            except AttributeError:
                print( "None" )

        # delay program for 2 seconds
        time.sleep(2)

get_player_pages(html, bsObj)
get_player_details(player_list)
p.close()
