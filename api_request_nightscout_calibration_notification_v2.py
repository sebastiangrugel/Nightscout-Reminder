import requests
import time
import os

# Get RAW data from Nightscout related to calibration time
URL = 'https://grugelki-klikemia-jan.herokuapp.com/api/v1/devicestatus.json?find[device]=medtronic-600://640G&count=1' #LatestfromSony
#URL = 'https://grugelki-klikemia-jan.herokuapp.com/api/v1/devicestatus.json?find[_id]=6064f94a4c8d1c0004b1cf3b' #8h55m
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


################ SECTION RELATED TO SLACK CONFIGURATION ##################################################
credentials = os.environ.get('_SECRET_SLACK_WEBHOOK_')
message = f"Kalibracja za maksymalnie {hours} godzin i {minutes} minut."
def post_to_slack(message, credentials):
    data = {'text': message}
    url = credentials
    requests.post(url, json=data, verify=False)



########### TEST SECTION ############### EXECUTED EVERY CODE IS RUNNING ####################################

# Send information about time to calibration every time when code is run. Comment this section if not need it.
print("Message sent to SLACK")
#post_to_slack(message, credentials)
post_to_slack(f"Kalibracja za maksymalnie {hours} godzin i {minutes} minut.", credentials)

##############################################################################################################

# Conditions

if int(hours) == 3: # calibration need it in less than 4 hours
        print(f"{hours} hours")
        print("Message sent to SLACK")
        post_to_slack(message, credentials)

if int(hours) == 2: # calibration need it in less than 3 hours
        print(f"more than {hours} hours")
        print("Message sent to SLACK")
        post_to_slack(message, credentials)

if int(hours) == 1: # calibration need it in less than 2 hours
        print("more than 1 hours", int(hours))
        print("Message sent to SLACK")
        post_to_slack(message, credentials)

        ###### CODE SENT PUSH NOTIFICATION TO MOBILEPHONE BY PUSHOVER.NET PLATFORM
        var_secret_pushover_token_ = os.environ.get('_SECRET_PUSHOVER_TOKEN_')
        var_secret_pushover_user_ = os.environ.get('_SECRET_PUSHOVER_USER_')
        import http.client, urllib
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.parse.urlencode({
                         "token": var_secret_pushover_token_,
                         "user": var_secret_pushover_user_,
                         "message": message,
                         "priority": "2",
                         "retry": "60",
                         "expire": "3600",
                         "sound": "alien",
                         "title": "!!!! KALIBRACJA !!!!",
                         "monospace": "1"
                     }), {"Content-type": "application/x-www-form-urlencoded"})
        conn.getresponse()
        #########################################################################

''' Temporary not working
if int(hours) == null:
        print("less than 1 hours", int(hours))
        print("Message sent to SLACK")
        post_to_slack(message, credentials)
'''

