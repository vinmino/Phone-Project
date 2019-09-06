import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import pandas as pd
import json


# ###################  Used to cover errors that occur in Selenium when the page isn't loaded  ####################
def tryToClick(func, param):
    while True:
        try:
            func(param).click()
            return True
        except Exception as e:
            lol = 1 + 1


def tryToType(func, param, text):
    while True:
        try:
            func(param).send_keys(text)
            return True
        except Exception as e:
            lol = 1 + 1


def tryFunc(func, param):
    while True:
        try:
            func(param)
            return True
        except Exception as e:
            lol = 1 + 1


# #########################################################################


# #######   Function that uses Selenium and PyAutoGUI to attempt to turn the API on for the phone
# #######   DO NOT MOVE MOUSE WHILE CALLING THIS FUNCTION
# Returns True or False depending on whether the request gets an error. This prevents attempting to send
#   two separate requests when the first one fails
def turnOnAPIForPhone(ip, passW):
    selURL = 'https://' + ip
    # Tests to see if the phone is online / will respond to a simple GET request
    try:
        r = requests.get(selURL + '/api/v1/mgmt/device/info', verify=False)
        if r.status_code == 200:
            print('API is already enabled at: ' + ip)
            log_file.write('API is already enabled at: ' + ip + '\n')
            return False
    except requests.RequestException as e:
        log_file.write('FAILED to start API at ' + ip + ' with error: ' + str(e))
        print('FAILED to start API at ' + ip + ' with error: ' + str(e))
        down.append(ip)
        return False
    except json.JSONDecodeError as e:
        lol = 1 + 1
    # Attempts to enable API
    brow = webdriver.Chrome()
    brow.get(selURL)
    tryToType(brow.find_element_by_name, 'password', passW + Keys.ENTER)
    # time.sleep(2)
    # pyautogui.moveTo(x=373, y=261)
    # time.sleep(1.5)
    # pyautogui.moveTo(x=375, y=370)
    # time.sleep(1)
    # pyautogui.click()
    # time.sleep(1.5)
    # pyautogui.click(x=348, y=777)
    # time.sleep(1.2)
    # pyautogui.click(x=412, y=809)
    # time.sleep(1.1)
    # pyautogui.scroll(-100)
    # time.sleep(1)
    # pyautogui.moveTo(x=906, y=953)
    # time.sleep(1.1)
    # pyautogui.click()
    # time.sleep(1)
    # pyautogui.moveTo(x=819, y=494)
    # time.sleep(1.1)
    # pyautogui.click()
    # time.sleep(2)
    t = input('Done?: ')
    try:
        brow.close()
    except Exception as e:
        lol = 1 + 1
    # Logs and updates the console
    log_file.write('Attempted to enable API on ' + ip + '\n')
    print('Attempted to enable API on ' + ip)
    return True


# #######  This Function sets the configs that are set below.
# Only runs if the API Function returns true
def turnOnPaging(ip, passW):
    url = 'https://' + ip + '/api/v1/mgmt/config/set'
    data = {
        'data': {
            'ptt.pageMode.enable': '1',
            'bg.color.bm.1.name': 'https://i.imgur.com/DfAwjaG.jpg',
            'bg.color.selection': '2,1'
        }
    }
    try:
        r = requests.post(url, auth=('Polycom', passW), json=data, verify=False)
        time.sleep(3)
        t = requests.post('https://' + ip + '/api/v1/mgmt/safeRestart', auth=('Polycom', passW), json={}, verify=False)
        print(t.text)
    except Exception as e:
        # Only fails if the phone goes down between the API function and this one. Should never happen...
        log_file.write('FAILED to start API at ' + ip + ' with error: ' + str(e) + '\n')
        print('FAILED to start API at ' + ip + ' with error: ' + str(e) + '\n')
        return False
    log_file.write(str(r.status_code))
    print(str(r.status_code))

    # Assigns the IP to the correct list for logging purposes
    if r.status_code != 200:
        log_file.write('Failed at ' + ip + '\n')
        print('Failed at ' + ip)
        failed.append(ip)
    elif json.loads(r.text)['Status'] == '2000':
        log_file.write('Success at ' + ip + '\n')
        print('Success at ' + ip)
        successes.append(ip)
    else:
        log_file.write('Unknown response at ' + ip + '\n')
        print('Unknown response at ' + ip)
        unknown.append([ip, r])


def updateConfig(ip, passwd, urlExtension, pathToData):
    with open(pathToData) as file:
        data = file.read().replace('\n', '')
    r = requests.post(url='https://' + ip + urlExtension, auth=('Polycom', passwd), verify=False, json=data)
    try:
        print(json.loads(json.dumps(r.text)))
    except Exception:
        print(r.text)


# Assigns variables
folder_name = 'resources' + str(time.time())
os.mkdir(folder_name)
log_file = open(folder_name + '/log.txt', 'w')
failed = []
successes = []
unknown = []
down = []
start_time = time.time()

df = pd.read_excel(io='Polycom_Phones_Bradford_Export.xlsx', header=0, sheet_name='Polycom_Phones_Bradford_Export')
for i in range(df['IP_Address'].size):
    workingIP = df['IP_Address'][i]
    password = df['Device_Password'][i]
    if turnOnAPIForPhone(workingIP, password):
        time.sleep(1)
        turnOnPaging(workingIP, password)

log_file.write('\n=====Finished=====\n')
print('\n\n=====Done=====\n\n')
log_file.write('Failed at IPs:\n')
print('Failed at IPs:')

# Logs to the log file and to the console
for add in failed:
    log_file.write('\t' + add + '\n')
    print('\t' + add)
log_file.write('Succeeded at IPs:\n')
print('Succeeded at IPs:')
for add in successes:
    log_file.write('\t' + add + '\n')
    print('\t' + add)
log_file.write('Devices are Down:\n')
print('Devices are Down:')
for add in down:
    log_file.write('\t' + add + '\n')
    print('\t' + add)
log_file.write('Unknown Response at IPs:\n')
print('Unknown Response at IPs:')
for add in unknown:
    log_file.write('\t' + add + '\n')
    print('\t' + add)

# Logs the status lists to their designated CSVs
failed_df = pd.DataFrame(
    {
        'failed': failed,
    })
successes_df = pd.DataFrame(
    {
        'successes': successes,
    })
down_df = pd.DataFrame(
    {
        'down': down,
    })
unknown_df = pd.DataFrame(
    {
        'unknown': unknown,
    })
failed_df.to_csv(folder_name + '/failed.csv')
successes_df.to_csv(folder_name + '/successes.csv')
down_df.to_csv(folder_name + '/down.csv')
unknown_df.to_csv(folder_name + '/unknown.csv')
log_file.write('Finished writing to csv\n')
print('Finished writing to csv')
end_time = str(time.time() - start_time)
log_file.write('Amount of time since start of program: ' + end_time)
log_file.close()
print('Amount of time since start of program: ' + end_time)

# At the end of the program, make sure to change the name of the output folder or else it will overwrite
#   the next time that it is run
