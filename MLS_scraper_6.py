from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import csv

# Now we add ability to write out a CSV file
# import the csv library

# open new file for writing
csvfile = open("mls_players.csv", 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
# write the header row in the CSV
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
    time.sleep(1)
    # disable for testing - use only first page URLs 
    # get_next_page(html, bsObj)

def get_player_details(player_list):
    for player in player_list:
        new_url = "http://www.mlssoccer.com" + player
        html = urlopen(new_url)
        bsObj = BeautifulSoup(html, "html.parser")
        bsObj.span.decompose()
        player_details = []
        title = bsObj.find( "div", {"class":"title"} )
        team = bsObj.find( "div", {"class":"club"} )
        position = bsObj.find( "span", {"class":"position"} )
        birthday = bsObj.find( "div", {"class":"age"} )
        # <div class="age"><span class="category">Age:</span>
        # 23 (10/21/1992)</div>
        birthplace = bsObj.find( "div", {"class":"hometown"} )
        # <div class="hometown"><span class="category">Birthplace:</span>
        # Barranquilla, Colombia</div>
        twitter = bsObj.find( "div", {"class":"twitter_handle"} )

        player_details = [title, team, position, birthday, birthplace,
        twitter]
        # new empty list for CSV rows
        row = []
        for detail in player_details:
            try:
                # write a new item into the list, row
                row.append( detail.get_text() )
            except AttributeError:
                # write a new item into the list, row
                row.append( "None" )

        # write a new row in the CSV, by writing the list
        c.writerow( row )

        # delay program for 1 second
        time.sleep(1)

get_player_pages(html, bsObj)
get_player_details(player_list)
# close CSV file
csvfile.close()
