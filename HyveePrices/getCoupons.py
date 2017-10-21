import urllib2

# Pretend to be firefox and get the webpage
url = "https://www.couponmom.com/best-coupon-deals-hyvee"
headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(url, None, headers)
html = urllib2.urlopen(req).read()

# Use BeautifulSoup
#soup = BeautifulSoup(html, 'html.parser')

# We cant use beautifulsoup :( Get all the deals
#deals = BeautifulSoup(str(soup.find_all('ol', 'hot_deal_list', 'href')), 'html.parser')

#get the start of the coupons
start = html.find('<ol class=\"hot_deal_list\">') + 27
html = html[start:]

# list for coupons
allCoupons = []
count = 0

theEnd = 1;
while bool(theEnd):
    # Get coupon price
    startPrice = html.find('<span class=\"\">') + 15
    endPrice = html.find(':')
    itemPrice = html[startPrice:endPrice]

    # Get coupon desc
    startDesc = html.find('</span>') + 8
    endDesc = html.find('</a>')
    itemDesc = html[startDesc:endDesc]
    itemDesc = itemDesc.replace("ct", "count")
    itemDesc = itemDesc.replace("oz", "ounces")

    # cut the html down to get next item
    nextItem = html.find('</li>') + 6
    html = html[nextItem:]

    #build text
    allCoupons.insert(count, itemDesc + 'are on sale for ' + itemPrice)
    count = count + 1

    #check for end of coupons
    end = html.find('</ol>')
    if end < 10:
        theEnd = 0

print allCoupons
