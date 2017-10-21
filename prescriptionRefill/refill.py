import requests
url = "https://www.hy-vee.com/my-pharmacy/refill"
payload = "{'someContent':'SomeValue'}"
headers = {
    'accept': "application/json",
    'content-type': "application/json; charset=UTF-8"
    }
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
