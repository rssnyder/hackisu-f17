import urllib2
from bs4 import BeautifulSoup


# Pretend to be firefox and get the webpage
url = "https://www.hy-vee.com/company/press-room/"
# headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(url, None)
html = urllib2.urlopen(req).read()

# Use BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

print soup.prettify()
