#!/usr/bin/python
# -*- coding: UTF-8 -*-

import httplib
import json
import socket
import os
import time
import pandas as pd
from flask import Flask, jsonify
from flask import send_from_directory

class switch(object):
    def __init__(self, value):      # 初始化需要匹配的值value
        self.value = value
        self.fall = False           # 如果匹配到的case语句中没有break，则fall为true。
 
    def __iter__(self):
        yield self.match            # 调用match方法 返回一个生成器
        raise StopIteration         # StopIteration 异常来判断for循环是否结束
 
    def match(self, *args):         # 模拟case子句的方法
        if self.fall or not args:   # 如果fall为true，则继续执行下面的case子句
                                    # 或case子句没有匹配项，则流转到默认分支。
            return True
        elif self.value in args:    # 匹配成功
            self.fall = True
            return True
        else:                       # 匹配失败
            return False


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



app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/codebase/<path:path>')
def send_codebase(path):
    print 'request_path:'+path
    root_dir = os.path.dirname(os.getcwd())
    pwd_root_dir = os.getcwd()
    print 'pwd:'+os.getcwd()
    print 'root_dir:'+root_dir
    return send_from_directory(os.path.join(pwd_root_dir, 'static', 'codebase'), path)


@app.route('/sysinfo/api/v1.0/consul_<view>', methods=['GET'])
def get_tasks(view):
    base_url = os.environ["consul_url"]
    conn1 = httplib.HTTPConnection( base_url )
    conn1.request('GET', '/v1/catalog/services')
    resp=conn1.getresponse()
    print resp.status
    resp_data = json.loads(resp.read().decode('utf-8'))
    print resp_data

    if( view == "summery" ):
        datahub_service = []
        
        for key in resp_data:
            datahub_service.append({'id':key,'item':key})
        print  datahub_service
        conn1.close()
        return json.dumps( datahub_service )

    if( view == "detail" ):
        datahub_service = []

        for id in resp_data:
            conn1.request('GET', '/v1/catalog/service/'+id)
            resp=conn1.getresponse()
            print resp.status
            resp_data = json.loads(resp.read().decode('utf-8'))
            print resp_data
            for resp_item in resp_data:
                datahub_service.append(resp_item)

        conn1.close()
        return json.dumps( {'data':datahub_service} )


@app.route('/sysinfo/api/v1.0/container_<view>', methods=['GET'])
def get_container_summ_tasks(view):
    getsome = getdockerinfo('/containers/json?all=1')
    getsome_json = json.loads(getsome)
    print getsome_json
    con_name_list, con_image_list, con_status_list, con_status_time = [], [], [], []
    for con in getsome_json:
        print con
        print con['Names']
        if(con['Names'] == None):
            con_name_list.append( "" )
        else:
            con_name_list.append( con['Names'][0].split('/',1)[1] )
        con_image_list.append(con['Image'])
        con_status_list.append(con['Status'].split(' ',1)[0] )
        try:
            con_status_time.append(con['Status'].split(' ',1)[1] )
        except IndexError ,e:
            con_status_time.append( "" )
    cont_up = pd.DataFrame({"name":con_name_list,"image":con_image_list,"status":con_status_list, "time":con_status_time})
    print "cont_up"
    print cont_up
    
    for case in switch(view):  
        if case('summ'):
            dh_app = pd.DataFrame({'app_name':['bill'],'app_container':['13_datahub_bill_db_1'] })
            dh_app = dh_app.append( pd.DataFrame({'app_name':['bill']   ,'app_container':['13_datahub_bill_datahub_bill_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['user']   ,'app_container':['0_datahub_user_db_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['user']   ,'app_container':['0_datahub_user_datahub_user_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['consul'] ,'app_container':['1_datahub_consul_consul_1']}))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['kafka']  ,'app_container':['11_datahub_kafka_datahub_kafka_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['message'],'app_container':['12_datahub_message_db_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['message'],'app_container':['12_datahub_message_datahub_message_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['synchro'],'app_container':['14_datahub_synchro_db_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['synchro'],'app_container':['14_datahub_synchro_datahub_synchro_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['registrator']    ,'app_container':['2_datahub_registrator_registrator_1']}))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['subscriptions']  ,'app_container':['4_datahub_subscriptions_datahub_subscriptions_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['subscriptions']  ,'app_container':['4_datahub_subscriptions_db_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['star']   ,'app_container':['4-1datahub_star_db_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['star']   ,'app_container':['4-1datahub_star_datahub_star_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['comments']       ,'app_container':['4-2datahub_comments_db_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['comments']       ,'app_container':['4-2datahub_comments_datahub_comments_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['repository']     ,'app_container':['5_datahub_repository_master_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['repository']     ,'app_container':['5_datahub_repository_datahub_repository_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['repository']     ,'app_container':['5_datahub_repository_slave_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['web']    ,'app_container':['6_datahub_web_datahub_web_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['heartbeat']      ,'app_container':['8_datahub_heartbeat_redis_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['heartbeat']      ,'app_container':['8_datahub_heartbeat_datahub_heartbeat_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['servicediscovery'],'app_container':['9_datahub_servicediscovery_redis_1'] }))
            dh_app = dh_app.append( pd.DataFrame({'app_name':['servicediscovery'],'app_container':['9_datahub_servicediscovery_service_discovery_1'] }))
            cont_total =  pd.merge(dh_app, cont_up, how='left', left_on='app_container' ,right_on='name')
            #con_up_num = cont_total[['name','status']].groupby(['status']).count()
            con_up_num = cont_up[['name','status']].groupby(['status']).count()
            con_up_num['data'] = con_up_num['name']
            print type(con_up_num)
            print con_up_num
            print type(con_up_num['data'].to_json(orient='columns'))
            ret_json =  json.loads( con_up_num['data'].to_json(orient='columns') )
            ret_json['id'] = 1
            print ret_json
            ret_json =  json.dumps( {'data': [ret_json] } )
            break
        if case('detail'):
            print cont_up.to_json(orient='records')
            print type(cont_up.to_json(orient='records'))
            ret_json = json.dumps({'data': json.loads(cont_up.to_json(orient='records')) })
            break
    print ret_json
    return ret_json

#@app.route('/sysinfo/api/v1.0/container_detail', methods=['GET'])
#//def get_container_detail_tasks():
#//    getsome = getdockerinfo('/containers/json?all=1')
#//    getsome_json = json.loads(getsome)
#//    image_list = []
#//    for con in getsome_json:
#//        image_list.append({'id':con['Names'][0],
#//                           'name':con['Names'][0],
#//                           'image':con['Image']  ,
#//                           'status':con['Status'] })
#    
#    return jsonify({'data': image_list })

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
