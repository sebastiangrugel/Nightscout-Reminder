import requests
import time

# Get RAW data from Nightscout related to calibration time
#URL = 'https://grugelki-klikemia-jan.herokuapp.com/api/v1/devicestatus.json?find[device]=medtronic-600://640G&count=1'
URL = 'https://grugelki-klikemia-jan.herokuapp.com/api/v1/devicestatus.json?find[_id]=6064f94a4c8d1c0004b1cf3b'


response = requests.get(URL)
data = response.json()
status = data[0]['pump']['status']['status']
print(status)

# Section related to convert time from JSON to readable value
import re
match = re.match('.* ([0-9])+h([0-9])+m .*', status)
hours, minutes = match.groups()



# To Display collected earlier data and send notification to SLACK
import json
credentials = r'C:\Users\Sebastian\PycharmProjects\pythonProject\credentials.json'
message = f"You must perform calibration before left {hours} hours and {minutes} minutes"


def get_credentials(credentials):
    '''
    Read credentials from JSON file.
    '''
    with open(credentials, 'r') as f:
        creds = json.load(f)
    return creds['slack_webhook']


def post_to_slack(message, credentials):
    data = {'text': message}
    url = get_credentials(credentials)
    requests.post(url, json=data, verify=False)

# Conditions

while int(hours) == 2:
        print(f"more than {hours} hours")
        print("Message sent to SLACK")
        post_to_slack(message, credentials)
        time.sleep(1800) #repeat message every

while int(hours) == 1:
        print("more than 2 hours", int(hours))
        print("Message sent to SLACK")
        post_to_slack(message, credentials)
        time.sleep(900)

while int(hours) < 1:
        print("more than 1 hours", int(hours))
        print("Message sent to SLACK")
        post_to_slack(message, credentials)
        time.sleep(600)

