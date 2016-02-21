#!/usr/bin/python
# -*- coding: UTF-8 -*-

import httplib
import json
import socket
import time
import pandas as pd

__all__ = ['HTTPConnection', 'HTTPError', 'get']


class ConnectDocker(httplib.HTTPConnection):

    def __init__(self):
        httplib.HTTPConnection.__init__(self, 'localhost')

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect('/var/run/docker.sock')
        self.sock = sock

class HTTPError(Exception):

    def __init__(self, status, reason):
        self.status = status
        self.reason = reason


def getdockerinfo(path, async=False):
    conn = ConnectDocker()
    try:
        conn.request('GET', path)
        resp = conn.getresponse()
       
        if resp.status != 200:
            raise HTTPError(resp.status, resp.reason)
    except Exception:
        conn.close()
        raise

    try:
        if async:
            return resp
        elif resp.getheader('Content-Type') == 'application/json':
             resp_data = resp.read().decode('utf-8')
             return resp_data
#             return json.loads(resp_data)
#             return resp.read().decode('utf-8')
        else:
            return resp.read()
    finally:
        if not async:
            conn.close()

if __name__ == '__main__':
    getsome = get('/containers/json?all=1')
    getsome_json = json.loads(getsome)
    con_name_list, con_image_list, con_status_list = [], [], []
    for con in getsome_json:
        con_name_list.append(con['Names'][0])
        con_image_list.append(con['Image']) 
        con_status_list.append(con['Status'])

    print(con_name_list)
    print(con_image_list)
    print(con_status_list)

    base_url = '54.223.58.0:8500'
    conn1 = httplib.HTTPConnection( base_url )
    conn1.request('GET', '/v1/catalog/services')
    resp=conn1.getresponse()
    resp_data = json.loads(resp.read().decode('utf-8'))
    
    print resp_data  
    
    datahub_service = []
    print type(resp_data) 
    for key in resp_data:
        datahub_service.append(key)

    for svc in datahub_service:  
        print(svc)

        request_url = '/v1/catalog/service/' + svc
        print request_url
        conn1.request('GET', request_url )
 
        resp=conn1.getresponse()
        print resp.status
        if resp.status == 200: 
            resp_data = json.loads(resp.read().decode('utf-8'))
            print resp_data

    conn1.close()
    
    now = int(time.time())  
    print now

    print pd.DataFrame({"name":con_name_list,"image":con_image_list,"statu":con_status_list})
