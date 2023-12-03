import requests
import json
import pandas as pd
import base64
import os

class BetaFaceApi:
    def __init__(self, image_path):
        self.image_path = image_path

    def image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string

    def send_image_to_API(self, encoded_string):
        apiShit = {"api_key": "d45fd466-51e2-4701-8da8-04351c872236", "file_base64": encoded_string, "detection_flags": "classifiers,content, extended"}
        jsonData = json.dumps(apiShit)
        newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}

        print('Sending API request...')
        try:
            response = requests.post('https://www.betafaceapi.com/api/v2/media', headers=newHeaders, data=jsonData)
            print("Status code:", response.status_code)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.exceptions.HTTPError as e:
            print(f"Unable to send API request. Error: {e}")
            return None

        with open('facial_data.json', 'w') as f:
            json.dump(response.json(), f)

        return response.json()

    def faceData_race(self, response_json):
        race = response_json['media']['faces'][0]['tags'][31]['value']
        confidence = response_json['media']['faces'][0]['tags'][31]['confidence']
        race_confidence = confidence * 100
        return race, race_confidence


# image_path = os.path.abspath(".\\jackie_chan.jpg")

# api_instance = BetaFaceApi(image_path)

# encoded_image_string = api_instance.image_to_base64(api_instance.image_path)
# response_json = api_instance.send_image_to_API(encoded_image_string)

# data = api_instance.faceData_race(response_json)

# print(data)
