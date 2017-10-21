import urllib2

# Pretend to be firefox and get the webpage
url = "https://www.hy-vee.com/company/press-room/"

headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(url, None, headers)
html = urllib2.urlopen(req).read()

# Test and see if we can get the news
uptime = html.find('<html><head><meta http-equiv=\"Pragma\" content=\"no-cache\"/>')
if uptime >= 0:
    url = "https://www.hy-vee.com/company/press-room/default.aspx?viewall=1"
    html = urllib2.urlopen(req).read()
    uptime2 = html.find('equiv=\"Pragma\" content=\"no-cache\"/>')
    if uptime2 >= 0:
        #This means we are not able to get news right now

# Cut the html down to the main news articles
start = html.find('ctl00_cph_main_content_ArticleList_gvRecentArticles')
html = html[start:]

# List for news articles
allNews = []
count = 0
end = 1000

while end > 100:
    # Find the title of the news item
    start = html.find('<a')
    html = html[start:]
    start = html.find('>') + 1
    # Here we have the start of the title
    html = html[start:]
    html = html.lstrip()
    # Here we mark the end of the title
    end = html.find('</a>')
    item = html[:end]
    # Find the beginning of the description
    start = html.find('<br/>') + 6
    html = html[start:]
    html = html.lstrip()
    # Find the end of the description
    end = html.find('<a')
    desc = html[:end]
    desc = desc.replace('\n', ' ')
    # Create article and store
    item = item + ': ' + desc
    allNews.insert(count, item)
    count = count + 1

    #Chop off some extra
    stop = html.find('</a>')
    html = html[stop:]

    end = html.find('</table>')
    print html
    print end

# allNews is the list of news snippits
