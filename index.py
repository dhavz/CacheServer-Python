import os.path
from os import path
from urllib.parse import urlparse
import urllib
import requests as r
import re

from flask import Flask, request, render_template
app = Flask(__name__,template_folder='template')


"""
fin = open('cache\\cachedispelling-the-myths-surrounding-security-technology-and-gdpr.html','r',encoding='utf-8')
content = fin.read()
fin.close()
"""


@app.route('/')
def index():
    return render_template('form.html')

@app.route('/data')
def data():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    #URL from textbox
    url = request.form['text']

    #Parsed URL for Request
    parsed_result = urlparse(url)
    requrl=url.split("?")[0]

    
    #request Data form server using URL
    response = r.get(requrl)
    
    #File Name for Caching
    urlpath=parsed_result.path
    filename = parsed_result.netloc+urlpath
    fname=""
    if ".html" in filename: #or ".php" in filename:
        fpname = filename.split(".html")
        fname = fpname[0].split("/")
        fname = fname[-1]
    else:
        fname = fpname[0].split("/")
        fname = fname[-1]
        
    #Extract poison Data from URL
    poisiondata = ""
    qdata="TEMP"
    qdata = parsed_result.query
    if "TEMP" in qdata:
        print("in")
        poisiondata = "null"

    qdata1=qdata.split("&")
    
    for qtemp in qdata1:
        for q in qtemp:
            if "=" in q:
                fst=qtemp.index('=')+1
                poisiondata=poisiondata+qtemp[fst:]
                break
            
    #Preaparing Response Header
    resp_dict = response.headers
    heads="HTTP/1.0 200 OK\n"
    for head in resp_dict:
        heads = heads + head+":"+resp_dict[head] + "\n"

    f=0
    #Check the file Availble in Server Cache
    if path.exists("cache\cache"+fname)==True:
            
            cached_file = open('cache\cache'+fname, 'r+',encoding='utf-8')
            filecont = cached_file.read()
            cached_file.close()

            """
            print("-------------------File cont",filecont[-1])
            if "0" in filecont[-1]:
                pass
            else:
            """
            print("Posion Data",poisiondata)
            if "null" in poisiondata:
                print("No poision data")
                pass
            else:
                print("Some poision data")
                match = re.search(poisiondata, filecont)

                if match:
                    
                    print("Find in file",posiondata)
                    pass
                else:
                    print("Not Find,Write in a file")
                    ResponseBody=response.text
                    cached_file = open('cache\cache'+fname, 'w',encoding='utf-8')
                    changeData = re.sub(r'(<body*.+>)', r'\1'+poisiondata, filecont)
                    cached_file.write(changeData)
                    cached_file.write('0')
                    cached_file.close()
            
            fin = open('cache\cache'+fname, 'r',encoding='utf-8')
            content = fin.read()
            fin.close()
            response = content
            #response = 'HTTP/1.0 304 Not Modified\n' + heads +'\n'+ content
            print("----------------------DATA FROM CACHE----------------------------")
            return response
    else:
        if "Pragma" not in heads and "Cache-control" not in heads:
            #Response Body Data
            ResponseBody=response.text

            if response.status_code == 200:
                print('Saving a copy of {} in the cache'.format(fname))
                #print(fname)
                cached_file = open('cache\cache'+fname, 'w',encoding='utf-8')
                cached_file.write(ResponseBody)
                cached_file.write('1')
                cached_file.close()

                return response.text
            elif response.status_code == 404:
                print('<center><h1>Error 404: Not Found.</h1></center>')
                
        elif "Pragma" not in heads or "Cache-control" not in heads:
            ResponseBody=response.text
            
            if response.status_code == 200:
                print('Saving a copy of {} in the cache'.format(fname))
                #print(fname)
                cached_file = open('cache\cache'+fname, 'w',encoding='utf-8')
                cached_file.write(ResponseBody)
                cached_file.write('1')
                cached_file.close()

                return response.text
            elif response.status_code == 404:
                    print('<center><h1>Error 404: Not Found.</h1></center>')
                    
        else:
            print("------------------NO DATA STORE IN THE CACHE------------------")
            if response.status_code == 200:
                return response.text
            elif response.status_code == 404:
                    print('<center><h1>Error 404: Not Found.</h1></center>')
            
    #return processed_text

if __name__ == '__main__':
    app.run()


"""
DIFFERENCE

with open('first_file.txt', 'r') as file1:
    with open('second_file.txt, 'r') as file2:
        difference = set(file1).difference(file2)
        difference.discard('\n')
        with open('diff.txt', 'w') as file_out:
        for line in difference:
            file_out.write(line)

"""
