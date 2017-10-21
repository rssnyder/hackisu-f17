 # Untitled 
Our project for HackISU Fall 2017. 


Inspiration

When we first started to think about what Alexa Skill we wanted to create, we thought about creating a Hy-Vee related skill. When we talked to some of the Hy-Vee sponsors about our idea, they said that it might not be possible due to anti-bot software and not having an API. Thus, we took this as a challenge and began to work on the skill.
What it does

Our project is an Amazon Alexa skill that allows users to find current information on Hy-Vee prices, available coupons, gets news about Hy-Vee, and tells amazing jokes. The algorithm we created scrapes the Hy-Vee website for the current prices of different items using python. After getting this information, the AWS Lambda function we created analyzes the users speech and to tell up to date pricing information.
How we built it

First, we acquired data from the Hy-Vee website by scraping the website using python. The python saves the results of a post request and then manipulates the result into json format so that the lambda function can call the pricing or sales information. When using the echo dot, Alexa calls the lambda function every time that a user invokes the skill. We created multiple intents within the skill so that a user can say a variety of things and still get the correct results.
Challenges we ran into

One functionality we had wanted to implement was to auto-refill prescriptions via the Hy-Vee pharmacy website, however the website has encryptions so that we could not find the input text-box with python’s selenium.
Accomplishments that we're proud of

We are proud of our success in creating our first Alexa Skill, learning python, and for taking on a challenge that people were not sure if we could complete all within 36 hours.
What we learned

We learned how to use Amazon Alexa’s skill development kits, and we all learned how to use python for the first time during this hackathon.
What's next for HyVee Prices

We want to add functionality to express-refill prescriptions from Amazon Alexa, but we would need permissions from Hy-Vee to do so.
Built With

    python
    alexa
    echo
 
