import os
import requests
from datetime import datetime
GENDER = "male"
AGE = 20
WEIGHT_KG = 78
HEIGHT_CM = 155.7528

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

# nutritionix.io and sheety.co api
# google sheet url
# https://docs.google.com/spreadsheets/d/1Gllilyk9Lrg5lUAcolJuttCrgxtQWPNzfyxME_4Va7A/edit#gid=0
exercise_endpoint = os.getenv("EXERCISE_ENDPOINT")
exercise_text = input("Tell me which exercise you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
exercise_body = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=exercise_endpoint, json=exercise_body, headers=headers)
result = response.json()

sheet_endpoint = os.getenv("SHEET_ENDPOINT")

today = datetime.now()
current_date = today.strftime("%d/%m/%Y")
current_time = today.strftime("%H:%M:%S")

sheet_header = {
    "Authorization": os.getenv("AUTHORIZATION")
}


for data in result["exercises"]:

    duration = data["duration_min"]
    exercise = data["user_input"].title()
    calorie = data["nf_calories"]
    sheet_body = {
        "workout": {
            "date": current_date,
            "time": current_time,
            "exercise": exercise,
            "duration": duration,
            "calories": calorie,
        }
    }
    sheet_response = requests.post(url=sheet_endpoint, json=sheet_body, headers=sheet_header)
    print(sheet_response.text)
