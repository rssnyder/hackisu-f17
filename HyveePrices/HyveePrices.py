"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib
import json
import urllib2
import random

jokes=[
    'What if soy milk is just regular milk introducing itself in Spanish?',
    'What do you call cheese that isn’t yours? Nacho cheese',
    'What did the baby corn say to its mom? Where’s my pop corn?',
    'What do you call a fake noodle? An impasta',
    'Why did the tomato blush? Because it saw the salad dressing.',
    'Why don’t eggs tell jokes? They’d crack each other up!',
    'What does a nosey pepper do? Gets jalapeño business!',
    'Waffles are just pancakes with abs',
    'Your name must be Coca Cola, because you’re soda licious.'
]


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Method to get prices of grocery items ----------------------

def get_item(str):
    # item = str(search)
    url = "https://www.hy-vee.com/grocery/calls/SearchList.aspx?search=" + str + "&dep=0&depgroup=0&cat=0&subcat=0&brands=&diets=&sizes=&onsale=0&fuelsaver=0&coupon=0&whatIBuy=0&startIndex=1&ReturnAmount=120&sortID=5&init=true&squID=63339564&lockerEligibleFilter=false&type=filter&sreID=0"
    f = urllib.urlopen(url)
    # Get the raw html
    html = f.read()

    # Find the beginning and the end of the json string
    startOfJSON = html.find("dataLayer.push(") + 15
    endOfJSON = html.find("productListGTM-1") - 12

    # Clip the html down to just the json string and get into dictionary
    raw_json = html[startOfJSON:endOfJSON] + '}'
    # raw_json.rstrip("\r\n")
    raw_json = raw_json.replace('\n', ' ').replace('\r', '').replace('\'', '\"')
    parsed_json = json.loads(raw_json)

    # Make the dict of items
    items = parsed_json["ecommerce"]["impressions"]

    # for item in items:
        #do whatever with each item in the query
        # print item["name"] + '\t\t\t\t\t\t $' + item['price']
    return items[0]['name'] + " is " + "$" + items[0]['price']
        # item["name"] + '\t\t\t\t\t\t $' + item['price']

# --------------- Method to get current top coupons ----------------------
def get_coupons():
    # Pretend to be firefox and get the webpage
    url = "https://www.couponmom.com/best-coupon-deals-hyvee"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()

    # Use BeautifulSoup
    # soup = BeautifulSoup(html, 'html.parser')

    # We cant use beautifulsoup :( Get all the deals
    # deals = BeautifulSoup(str(soup.find_all('ol', 'hot_deal_list', 'href')), 'html.parser')

    # get the start of the coupons
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

        # build text
        allCoupons.insert(count, itemDesc + 'are on sale for ' + itemPrice)
        count = count + 1

        # check for end of coupons
        end = html.find('</ol>')
        if end < 10:
            theEnd = 0

    return allCoupons


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Hyvee Prices. " \
                    "Ask about grocies or deals"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what item's price you'd like to know by saying, " \
                    "what is the price of, and the item you're looking for"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def helper_method_get_instructions():

    session_attributes = {}
    card_title = "Help"
    speech_output = "Please tell me what item's price you'd like to know by saying, " \
                    "what is the price of, and the item you're looking for"

    reprompt_text = "What would you like me to do?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text,should_end_session))

def get_smile(intent, session):
    card_title= "What can I find in every aisle?"
    speech_output= "A smile"
    should_end_session=True
    reprompt_text = "What would you like to do?"
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Hyvee Prices. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_food_attributes(food_asked):
    return {"foodAsked": food_asked}


def set_food_in_session(intent, session):
    """ Sets the food that the user asked about.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'food' in intent['slots']:
        food = intent['slots']['food']['value']
        session_attributes = create_food_attributes(food)

        food_price = get_item(food)
        speech_output = food_price
        #                 ". You can ask me your favorite color by saying, " \
        #                 "what's my favorite color?"
        reprompt_text = "What item would you like to know the price of?"
    else:
        speech_output = "I'm not sure what food you said. " \
                        "Please try again."
        reprompt_text = "I'm not sure what food you said. " \
                        "Please tell me what item's price you'd like to know by saying, " \
                        "what is the price of, and the item you're looking for"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_food_price(food_asked):
    session_attributes = {}
    reprompt_text = None

    price = get_item(food_asked)

    session_attributes['returnedPrice'] = price

    #change later:
    should_end_session = True

    # if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
    #     favorite_color = session['attributes']['favoriteColor']
    #     speech_output = "Your favorite color is " + favorite_color + \
    #                     ". Goodbye."
    #     should_end_session = True
    # else:
    #     speech_output = "I'm not sure what your favorite color is. " \
    #                     "You can say, my favorite color is red."
    #     should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))



def set_coupons(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    coupons = get_coupons()

    rando = random.randint(0,len(coupons))
    speech_output = coupons[rando]

    reprompt_text = "What would you like to do?"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "PriceIntent":
        return set_food_in_session(intent, session)
    elif intent_name == "CouponIntent":
        return set_coupons(intent, session)
    elif intent_name == "GetSmile" :
        return get_smile(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return helper_method_get_instructions()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
