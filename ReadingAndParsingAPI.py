# password for Fixer Tq8FmUGsW8CQyZe
# API access key e5a25e5371f078adf18b6e10329bb0fc
# http://data.fixer.io/api/latest?access_key=e5a25e5371f078adf18b6e10329bb0fc

import json
import requests

url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"  # connect to the site
url2 = "https://api.exchangeratesapi.io/latest?base=USD"

Fixer_base_url = "http://data.fixer.io/api/"
Fixer_accessKey = "e5a25e5371f078adf18b6e10329bb0fc"

OpenNotify_url = "http://api.open-notify.org"

response = requests.get(url)
data = response.text                    # get the data in string form (UTF-8) this is serialized
                                        # in JSON format
parsed = json.loads(data)               # loads the payload as dictionary encoded in a string
                                        # other way is using response.json().
                                        # this also deserialize the data into a dictionary

print(json.dumps(parsed, indent=4))     # converts the dictionary to JSON format with indent
                                        # this step is not neccesary, only for better reading
date = parsed["date"]
gbp_rate = parsed["rates"]["GBP"]
usd_rate = parsed["rates"]["USD"]

print("On " + date + " EUR equals " + str(gbp_rate) + " GBP")
print("On " + date + " EUR equals " + str(usd_rate) + " USD")

response2 = requests.get(url2)
parsed = json.loads(response2.text)
series = json.dumps(parsed, indent=4)
print(series)

response = requests.get(Fixer_base_url+"latest?access_key="+Fixer_accessKey)
data = response.text
parsed = json.dumps(json.loads(data), indent=4)
print(parsed)

# An endpoint is a server route that is used to retrieve different data from the API.
# For example, the /comments endpoint on the Reddit API might retrieve information
# about comments, whereas the /users endpoint might retrieve data about users.
# To access them, you would add the endpoint to the base url of the API.

# The ISS Pass endpoint returns when the ISS will next pass over a given location on earth.
# In order to compute this, we need to pass the coordinates of the location to the API.
# We do this by passing two parameters — latitude and longitude.
# We can do this by adding an optional keyword argument, params, to our request.
# In this case, there are two parameters we need to pass: lat and lon

# We can make a dictionary with these parameters,
# and then pass them into the requests.get function.

# Set up the parameters we want to pass to the API.
# This is the latitude and longitude of New York City.
parameters = {"lat": 40.71, "lon": -74}
response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
print('\n\n')
print(response.content)
print('\n\n')
# You can get the content of a response as a python object by using the .json() method
# on the response.
data = response.json()          # get the data as dictionary in a string form
print(data)
print('\n\n')
# Get the response from the API endpoint.
response = requests.get("http://api.open-notify.org/astros.json")
data = response.json()              # same that json.loads()
# 9 people are currently in space.
print(data["number"])
print('\n\n')
print(json.dumps(data, indent=4))
print('\n\n')

# According to the HTTP specification, POST, PUT, and the less common PATCH requests
# pass their data through the message body rather than through parameters in the query string.
# Using requests, you’ll pass the payload to the corresponding function’s data parameter.

# data takes a dictionary, a list of tuples, bytes, or a file-like object.
# You’ll want to adapt the data you send in the body of your request to the specific
# needs of the service you’re interacting with.

# If, however, you need to send JSON data, you can use the json parameter.
# When you pass JSON data via json, requests will serialize your data and add the correct
# Content-Type header for you.


