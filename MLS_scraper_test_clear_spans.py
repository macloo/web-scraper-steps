from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import csv

# this version is able to get rid of the spans inside age/birthday 
# and birthplace -- see lines 63-67 

csvfile = open("mls_players_test.csv", 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
# write the header row for CSV file
c.writerow(['title', 'team', 'position', 'birthday', 'birthplace', 'twitter'])

html = urlopen("http://www.mlssoccer.com/players")
bsObj = BeautifulSoup(html, "html.parser")
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
    # time.sleep(1) # decided I don't need this delay
    # get_next_page(html, bsObj)

def get_player_details(player_list):
    counter = 0
    for player in player_list:
        new_url = "http://www.mlssoccer.com" + player
        html = urlopen(new_url)
        bsObj = BeautifulSoup(html, "html.parser")
        bsObj.span.decompose()
        player_details = []
        title = bsObj.find( "div", {"class":"title"} )
        team = bsObj.find( "div", {"class":"club"} )
        position = bsObj.find( "span", {"class":"position"} )
        # had div for position - should be span - oops 
        birthday = bsObj.find( "div", {"class":"age"} )
        # <div class="age"><span class="category">Age:</span>
        # 23 (10/21/1992)</div>
        birthplace = bsObj.find( "div", {"class":"hometown"} )
        # <div class="hometown"><span class="category">Birthplace:</span>
        # Barranquilla, Colombia</div>
        twitter = bsObj.find( "div", {"class":"twitter_handle"} )

        player_details = [title, team, position, birthday, birthplace,
        twitter]
        row = []
        for detail in player_details:
            # this is how to get rid of the spans --
            if detail is not None:
                if detail.span:
                    detail.span.clear()
            try:
                row.append( detail.get_text() )
            except AttributeError:
                row.append( "None" )
        
        c.writerow( row )

get_player_pages(html, bsObj)
get_player_details(player_list)
csvfile.close()
print("Finished!")
