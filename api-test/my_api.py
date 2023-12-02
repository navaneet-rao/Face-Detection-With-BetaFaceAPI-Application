import requests
import json
import pandas as pd
import base64
import os

def send_image_to_API(encoded_string):
    apiShit = {"api_key": "d45fd466-51e2-4701-8da8-04351c872236", "file_base64": encoded_string, "detection_flags": "classifiers,content, extended"}
    jsonData = json.dumps(apiShit)
    newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}

    print('Sending API request...')
    try:
        response = requests.post('https://www.betafaceapi.com/api/v2/media', headers=newHeaders, data=jsonData)
        print("Status code:", response.status_code)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Unable to send API request. Error: {e}")
        return None

    with open('facial_data.json', 'w') as f:
        json.dump(response.json(), f)

    return response.json()

image_path = os.path.abspath(".\\api-test\\myimage.jpg")
image_path = os.path.abspath(".\\api-test\\weekend.jpg")
image_path = os.path.abspath(".\\api-test\\jackie_chan.jpg")

with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

#print(encoded_string)

response_json = send_image_to_API(encoded_string)

# print(response_json)

dataTags = pd.DataFrame(response_json['media']['faces'][0]['tags'])

race = dataTags[dataTags['name'] == 'race'].iat[0,1]

print("Your are : ", race)

if(race=='asian'):
    compliment = 'Rice is tasty, and hentai is the high pinnacle of modern art forms.'
elif(race=='white'):
    compliment = 'Your acceptance of psychopaths and crackheads as leaders is wonderful.'
else:
    compliment = 'I respect and admire your culture and heritage. Have a great day!'
    
print(compliment)
