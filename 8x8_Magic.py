import requests
import json
import time
import sys


def custom_API_post(ip, passwd, urlExtension, pathToData):
    try:
        a = requests.get('https://' + ip, verify=False)
    except Exception:
        print('========> The host %s seems to be down or is not responding' % ip)
        return False
    try:
        with open(pathToData) as file:
            data = file.read().replace('\n', '')
            r = requests.post(url='https://' + ip + urlExtension, auth=('Polycom', passwd), verify=False, json=data)
    except Exception as e:
        data = {}

    try:
        print(json.loads(json.dumps(r.text)))
    except Exception:
        print(r.text)
        print('========> The host %s seems to not have the API enable' % ip)
        return False


def custom_API_get(ip, passwd, urlExtension):
    try:
        a = requests.get('https://' + ip, verify=False)
    except Exception:
        print('========> The host %s seems to be down or is not responding' % ip)
        return False

    r = requests.post(url='https://' + ip + urlExtension, auth=('Polycom', passwd), verify=False)

    try:
        print(json.loads(json.dumps(r.text)))
    except Exception:
        print(r.text)
        print('========> The host %s seems to not have the API enable' % ip)
        return False


def set_config(ip, passwd, pathToData):
    try:
        a = requests.get('https://' + ip, verify=False)
    except Exception:
        print('========> The host %s seems to be down or is not responding' % ip)
        return False

    with open(pathToData) as file:
        data = file.read().replace('\n', '')
        r = requests.post(url='https://' + ip + '/api/v1/mgmt/config/set', auth=('Polycom', passwd), verify=False, json=data)

    try:
        print(json.loads(json.dumps(r.text)))
    except Exception:
        print(r.text)
        print('========> The host %s seems to not have the API enable' % ip)
        return False


def safe_restart(ip, passwd):
    try:
        a = requests.get('https://' + ip, verify=False)
    except Exception:
        print('========> The host %s seems to be down or is not responding' % ip)
        return False

    try:
        time.sleep(3)
        r = requests.post('https://' + ip + '/api/v1/mgmt/safeRestart', auth=('Polycom', passwd), json={}, verify=False)
        print(json.loads(json.dumps(r.text)))
    except Exception:
        print('========> The host %s seems to not have the API enable' % ip)
        return False


def safe_reboot(ip, passwd):
    try:
        a = requests.get('https://' + ip, verify=False)
    except Exception:
        print('========> The host %s seems to be down or is not responding' % ip)
        return False

    try:
        time.sleep(3)
        r = requests.post('https://' + ip + '/api/v1/mgmt/safeReboot', auth=('Polycom', passwd), json={}, verify=False)
        print(json.loads(json.dumps(r.text)))
    except Exception:
        print('========> The host %s seems to not have the API enable' % ip)
        return False


def help_display():
    print(f'\nUsage: python {sys.argv[0]} [ --ip-address | -a <ip> ] [ --password | -p <ip> ] [ --file | -f '
          f'<path_to_file> ] [ --url-extension | -x <url_extension> ] [ --command | -c <command_ID_#> ] [ --help | -h'
          f' ] ')
    print('''
    Commands:
        1: Safe Restart (Just restarts the application of the phone, so it doesn't kill the network switching through phone)
            Has a 3 second delay
            Needs IP and Password
        2: Safe Reboot (Restarts the entire computer of the phone, so it also kills the network switching through phone)
            Has a 3 second delay
            Needs IP and Password
        3: Set Configurations
            Needs IP and Password and Path to File
            File must contain requested data changed in JSON format of 
            "data {
                    <CONFIGURATION SETTINGS> : <VALUE>,
                    ...
                    <CONFIGURATION SETTINGS> : <VALUE>
                }"
            The data settings and values can be found on the Polyom API PDF
        4: Send Custom Made API POST Requests
            Needs IP and Password and Path to File and URL Extension
            The URL extensions can be found in the PDF, and gets appended to
                "https://##.##.##.##" so include the leading / in the url extension
            The data file also needs be filled
        5: Send Custom Made API GET Requests
            Needs IP and Password and URL Extension
            The URL extension needs to be the same like the POST one
        #: Any other number will bring up this help display
        
        ======== PS this uses the REQUESTS python library ========
    ''')


def commandLineTool():
    is_error = False
    needs_help = False
    ip_address = ''
    password = ''
    path_to_file = ''
    url_extension = ''
    command = ''

    for index, arg in enumerate(sys.argv):
        if arg in ['--ip-address', '-a'] and len(sys.argv) > index + 1:
            ip_address = sys.argv[index + 1]
            del sys.argv[index]
            del sys.argv[index]
            break

    for index, arg in enumerate(sys.argv):
        if arg in ['--password', '-p'] and len(sys.argv) > index + 1:
            password = sys.argv[index + 1]
            del sys.argv[index]
            del sys.argv[index]
            break

    for index, arg in enumerate(sys.argv):
        if arg in ['--file', '-f'] and len(sys.argv) > index + 1:
            path_to_file = sys.argv[index + 1]
            del sys.argv[index]
            del sys.argv[index]
            break

    for index, arg in enumerate(sys.argv):
        if arg in ['--url-extension', '-x'] and len(sys.argv) > index + 1:
            url_extension = sys.argv[index + 1]
            del sys.argv[index]
            del sys.argv[index]
            break

    for index, arg in enumerate(sys.argv):
        if arg in ['--command', '-c'] and len(sys.argv) > index + 1:
            command = int(sys.argv[index + 1])
            del sys.argv[index]
            del sys.argv[index]
            break

    for index, arg in enumerate(sys.argv):
        if arg in ['--help', '-h'] and len(sys.argv) > index + 1:
            needs_help = True
            del sys.argv[index]
            break

    if len(sys.argv) > 1:
        is_error = True
    else:
        for arg in sys.argv:
            if arg.startswith('-'):
                is_error = True

    if is_error:
        print('\n========> is_error was set to true')
        help_display()
        sys.exit(1)
    elif needs_help:
        print('\n========> needs_help was set to true')
        help_display()
    else:
        try:
            if command == 1:
                safe_restart(ip_address, password)
                print('Restart Request Successfully Sent')
            elif command == 2:
                safe_reboot(ip_address, password)
                print('Reboot Request Successfully Sent')
            elif command == 3:
                set_config(ip_address, password, path_to_file)
                print('Configuration Set Request Successfully Sent')
            elif command == 4:
                custom_API_post(ip_address, password, url_extension, path_to_file)
                print('Custom API POST Request Successfully Sent')
            elif command == 5:
                custom_API_get(ip_address, password, url_extension)
                print('Custom API GET Request Successfully Sent')
            else:
                print('The command selected does not exist')
                help_display()
        except Exception as e:
            print('\n========> An error occurred somewhere when calling the function:\n%s' % e)


if __name__ == '__main__':
    commandLineTool()
