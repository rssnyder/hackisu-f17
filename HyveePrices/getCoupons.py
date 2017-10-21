import urllib2
from bs4 import BeautifulSoup

def getCoupons():
    # Pretend to be firefox and get the webpage
    url = "https://www.couponmom.com/best-coupon-deals-hyvee"
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()

    # Use BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    #Get all the deals
    deals = BeautifulSoup(str(soup.find_all('ol', 'hot_deal_list', 'href')), 'html.parser')

    # Storage for deals
    allCoupons = []
    count = 0

    # Get the item
    # item = deals.find_all('a')[0]
    for deal in deals.find_all('a'):
        item = str(deal)

        # Get the deal price
        startPrice = item.find("<span class=\"\">") + 15
        endPrice = item.find(":")
        itemPrice = item[startPrice:endPrice]

        # Get the deal name
        startDesc = item.find("</span>\\n") + 9
        endDesc = item.find("</a>")
        itemDesc = item[startDesc:endDesc]

        # Correct the short words for better alexa speak
        itemDesc = itemDesc.replace("ct", "count")
        itemDesc = itemDesc.replace("oz", "ounces")

        allCoupons.insert(count, itemDesc + 'are on sale for ' + itemPrice)
        count = count + 1

    # In the end we have list allCoupons that has the whole deals as strings
