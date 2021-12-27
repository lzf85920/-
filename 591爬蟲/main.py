import requests
import re
import pandas as pd
import numpy as np
import json
import multiprocessing as mp
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import requests.packages.urllib3
import time
import datetime

requests.packages.urllib3.disable_warnings()

# 將想要爬取的Post id存在兩個csv內，分別用多工爬取。
index_1 = pd.read_csv('c:\\Users\\user\\Downloads\\591crawler\\post_id_1.csv')['index'].tolist()
index_2 = pd.read_csv('c:\\Users\\user\\Downloads\\591crawler\\post_id_2.csv')['index'].tolist()


def itr_data1():
    
    headers = {
        'Accept': '*/*',
        'User-Agent': UserAgent().random,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'device': 'pc',
        'deviceid': 'aj99rvsgdr7c88a5t1liimfdv0',
        'token': 'aj99rvsgdr7c88a5t1liimfdv0',
        'sec-ch-ua-platform': "macOS",
        'X-CSRF-TOKEN': 'rIPJaViPiLSWmHwZtrSqHiid5R9bmoFE4bnh8AGC'
    }
    
    def GetDate(result, idx):
        try:
            data = {
                'index' : idx,
                'url' : result['data']['shareInfo']['url'],
                'posttime' : time.strftime("%Y-%m-%d", time.localtime(result['data']['favData']['posttime'])),
                'dealtime' : result['data']['dealTime'],
                'city' : result['data']["breadcrumb"][0]['name'],
                'region' : result['data']["breadcrumb"][1]['name'],
                'address' : result['data']['favData']['address'],
                'lat' : float(result['data']['positionRound']['lat']),
                'lng' : float(result['data']['positionRound']['lng']),
                'rentprice' : result['data']['favData']['price'],
                'park' : result['data']["service"]['facility'][-1]['active']
            }
        except:
            data = {
                'index' : idx,
                'url' : result['data']['shareInfo']['url'],
                'posttime' : time.strftime("%Y-%m-%d", time.localtime(result['data']['favData']['posttime'])),
                'dealtime' : result['data']['dealTime'],
                'city' : result['data']["breadcrumb"][0]['name'],
                'region' : result['data']["breadcrumb"][1]['name'],
                'address' : result['data']['favData']['address'],
                'lat' : float(result['data']['positionRound']['lat']),
                'lng' : float(result['data']['positionRound']['lng']),
                'rentprice' : result['data']['favData']['price'],
                'park' : 'park'
            }
        for i in result['data']['info']:
            data[i['key']] = i['value']

        for i in result['data']["costData"]['data']:
            data[i['key']] = i['value']
            
        for i in result['data']['service']['facility']:
            data[i['key']] = i['active']

        return data

    datalist = []
    savecount = 0

    for i in tqdm(index_1):
        savecount+=1
        time.sleep(0.5)
        try:
            result = requests.get('https://bff.591.com.tw/v1/house/rent/detail?id=%s'%(i), headers = headers, timeout=10).text
            result = json.loads(result)
            if result['data'] != '':
                datalist.append(GetDate(result, i))

        except Exception as e:
            print(e)
            with open('C:\\Users\\user\\Downloads\\591crawler\\requesterror_log1.txt', 'a+', encoding='utf-8') as f:
                f.write(str(i)+',')
                
            with open('C:\\Users\\user\\Downloads\\591crawler\\requesterror_log1.txt', 'r', encoding='utf-8') as f:
                leng = f.read()
            leng = leng.split(',')
            if len(leng) > 50:
                break    
            
            continue
                    
        if (savecount%1000 == 0) | (i == 6639572):

            output = pd.read_csv('C:\\Users\\user\\Downloads\\591crawler\\rent_3.csv')
            output = output.append(pd.DataFrame(datalist))
            output.to_csv('C:\\Users\\user\\Downloads\\591crawler\\rent_3.csv', index=False, encoding='utf-8-sig')
            datalist = []
            savecount=0
    
    return None

def itr_data2():
    
    headers = {
        'Accept': '*/*',
        'User-Agent': UserAgent().random,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'device': 'pc',
        'deviceid': 'aj99rvsgdr7c88a5t1liimfdv0',
        'token': 'aj99rvsgdr7c88a5t1liimfdv0',
        'sec-ch-ua-platform': "macOS",
        'X-CSRF-TOKEN': 'rIPJaViPiLSWmHwZtrSqHiid5R9bmoFE4bnh8AGC'
    }
    
    def GetDate(result, idx):

        try:
            data = {
                'index' : idx,
                'url' : result['data']['shareInfo']['url'],
                'posttime' : time.strftime("%Y-%m-%d", time.localtime(result['data']['favData']['posttime'])),
                'dealtime' : result['data']['dealTime'],
                'city' : result['data']["breadcrumb"][0]['name'],
                'region' : result['data']["breadcrumb"][1]['name'],
                'address' : result['data']['favData']['address'],
                'lat' : float(result['data']['positionRound']['lat']),
                'lng' : float(result['data']['positionRound']['lng']),
                'rentprice' : result['data']['favData']['price'],
                'park' : result['data']["service"]['facility'][-1]['active']
            }
        except:
            data = {
                'index' : idx,
                'url' : result['data']['shareInfo']['url'],
                'posttime' : time.strftime("%Y-%m-%d", time.localtime(result['data']['favData']['posttime'])),
                'dealtime' : result['data']['dealTime'],
                'city' : result['data']["breadcrumb"][0]['name'],
                'region' : result['data']["breadcrumb"][1]['name'],
                'address' : result['data']['favData']['address'],
                'lat' : float(result['data']['positionRound']['lat']),
                'lng' : float(result['data']['positionRound']['lng']),
                'rentprice' : result['data']['favData']['price'],
                'park' : 'park'
            }
        for i in result['data']['info']:
            data[i['key']] = i['value']

        for i in result['data']["costData"]['data']:
            data[i['key']] = i['value']
            
        for i in result['data']['service']['facility']:
            data[i['key']] = i['active']
        return data

    datalist = []
    savecount = 0

    for i in tqdm(index_2):
        time.sleep(0.5)
        savecount+=1
        try:
            result = requests.get('https://bff.591.com.tw/v1/house/rent/detail?id=%s'%(i), headers = headers, timeout=10).text
            result = json.loads(result)
            if result['data'] != '':
                datalist.append(GetDate(result, i))

        except Exception as e:
            print(e)
            with open('C:\\Users\\user\\Downloads\\591crawler\\requesterror_log1.txt', 'a+', encoding='utf-8') as f:
                f.write(str(i)+',')
                
            with open('C:\\Users\\user\\Downloads\\591crawler\\requesterror_log1.txt', 'r', encoding='utf-8') as f:
                leng = f.read()
            leng = leng.split(',')
            if len(leng) > 50:
                break    
            
            continue
                    
        if (savecount%1000 == 0) | (i == 2490410):

            output = pd.read_csv('C:\\Users\\user\\Downloads\\591crawler\\rent_4.csv')
            output = output.append(pd.DataFrame(datalist))
            output.to_csv('C:\\Users\\user\\Downloads\\591crawler\\rent_4.csv', index=False, encoding='utf-8-sig')
            datalist = []
            savecount=0
    
    return None

  
if __name__ == '__main__' :
    p1 = mp.Process(target=itr_data1)
    p2 = mp.Process(target=itr_data2)
    start_time = time.time()
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end_time = time.time()
    print('It costs '+str(end_time - start_time)+' s')




