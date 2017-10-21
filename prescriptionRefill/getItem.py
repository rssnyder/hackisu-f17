import urllib
import json

def getItem(str):
    # item = str(search)
    url = "https://www.hy-vee.com/grocery/calls/SearchList.aspx?search=" + str + "&dep=0&depgroup=0&cat=0&subcat=0&brands=&diets=&sizes=&onsale=0&fuelsaver=0&coupon=0&whatIBuy=0&startIndex=1&ReturnAmount=120&sortID=5&init=true&squID=63339564&lockerEligibleFilter=false&type=filter&sreID=0"
    f = urllib.urlopen(url)
    # Get the raw html
    html = f.read()

    # Find the beginning and the end of the json string
    startOfJSON = html.find("dataLayer.push(") + 15
    endOfJSON = html.find("productListGTM-1") - 12

    # Clip the html down to just the json string and get into dictionary
    raw_json = html[startOfJSON:endOfJSON] + '}';
    # raw_json.rstrip("\r\n")
    raw_json = raw_json.replace('\n', ' ').replace('\r', '').replace('\'', '\"')
    parsed_json = json.loads(raw_json)

    # Make the dict of items
    items = parsed_json["ecommerce"]["impressions"]

    for item in items:
        #do whatever with each item in the query
        print item["name"] + '\t\t\t\t\t\t $' + item['price']


getItem("steak")
