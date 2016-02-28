from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.mlssoccer.com/players")
bsObj = BeautifulSoup(html, "html.parser")
f = open("mls_urls.txt", 'a')

# Added: After getting all player URLs from a list page, get the 
# URL of the NEXT list page, open it, run the player function again.
# The two functions call each other.

# looking at this tag to get the next page URL --
# <a title="Go to next page" href="/players?page=1">next ›</a>
def get_next_page(html, bsObj):
    next_page = bsObj.find( "a", {"title":"Go to next page"} )
    if next_page and ('href' in next_page.attrs):
        partial = str(next_page.attrs['href'])
        new_url = "http://www.mlssoccer.com" + partial
        html = urlopen(new_url)
        bsObj = BeautifulSoup(html, "html.parser")
        # scrape the new page for URLs --
        get_player_pages(html, bsObj)
    else:
        # the last page doesn't have title="Go to next page"
        # so we stop when that is not found
        print("Done!")

# run this on each page to get player detail page links
def get_player_pages(html, bsObj):
    tag_list = bsObj.findAll( "a", {"class":"row_link"} )
    for tag in tag_list:
        if 'href' in tag.attrs: 
            f.write(str(tag.attrs['href']) + "\n")
        else:
            f.write("no href\n")
    # when a page is done, get the next page --
    get_next_page(html, bsObj)

# run the function! 
get_player_pages(html, bsObj)
f.close()
