import requests
import time
import os

# Get RAW data from Nightscout related to calibration time
#URL = 'https://grugelki-klikemia-jan.herokuapp.com/api/v1/devicestatus.json?find[device]=medtronic-600://640G&count=1'
URL = 'https://grugelki-klikemia-jan.herokuapp.com/api/v1/devicestatus.json?find[_id]=6064f94a4c8d1c0004b1cf3b'
#URL = 'https://grugelki-klikemia-jan.herokuapp.com/api/v1/devicestatus.json?find[_id]=608fb555bed68000049e5fc7' #95m

# GET data releted to pump calibration time from JSON
response = requests.get(URL)
data = response.json()
status = data[0]['pump']['status']['status']
print("RAW data from JSON:",status)

# Section related to convert time from JSON to readable value
import re
match = re.match('.* ([0-9]+)h([0-9]+)m.*', status) # in this line removed space before 2nf dot... (fix)
hours, minutes = match.groups()
print(f"Information converted from JSON by REGEX: {hours} hours and {minutes} minutes")


credentials = os.environ.get('_SECRET_SLACK_WEBHOOK_')
message = f"You must perform calibration before left {hours} hours and {minutes} minutes"

def post_to_slack(message, credentials):
    data = {'text': message}
    url = credentials
    requests.post(url, json=data, verify=False)



########### TEST SECTION ###############

# Send information about time to calibration every time when code is run. Comment this section if not need it.
print("Message sent to SLACK")
post_to_slack(message, credentials)
post_to_slack(f"Cogodzinny test GitHUB Actions. Kalibracja za maksymalnie {hours} godzin i {minutes} minut.", credentials)
##############################################################################################################

if int(hours) == 6: # and int(minutes) == 0:
        print(f"{hours} hours")
        print("Message sent to SLACK")
        post_to_slack(message, credentials)


##############################################################################################################

# Conditions

if int(hours) == 2:
        print(f"more than {hours} hours")
        print("Message sent to SLACK")
        post_to_slack(message, credentials)

if int(hours) == 1:
        print("more than 1 hours", int(hours))
        print("Message sent to SLACK")
        post_to_slack(message, credentials)

''' Temporary not working
if int(hours) == null:
        print("less than 1 hours", int(hours))
        print("Message sent to SLACK")
        post_to_slack(message, credentials)
'''

