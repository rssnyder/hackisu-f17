import urllib2

# Pretend to be firefox and get the webpage
url = "https://twitter.com/HyVee"

headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(url, None, headers)
html = urllib2.urlopen(req).read()

print html
