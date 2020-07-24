import requests

response = requests.get('https://httpibn.org/ip')
print('response was: ', response)
print(dir(response))                # to see the methods that i can acces with this response object
print(response.text)
print(response.status_code)         # print code
print(response.ok)                   # print TRUE for anything less than 400
print(response.headers)              # headers that come back with the response

payload = {'page': 2, 'count': 25}  # dictionary
response = requests.get('https://httpbin.org/get', params=payload)
print(response.url)

# to post some data
payload = {'username': 'carlos', 'password': 'testing'}  # dictionary
response = requests.post('https://httpbin.org/post', data=payload)

print(response.text)

# better like this-------------
response_dict = response.json()    # returns json response in a dictionary
print(response_dict['form'])