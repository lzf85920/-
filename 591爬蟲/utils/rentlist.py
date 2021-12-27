import requests
import json
import urllib.parse
from tqdm import tqdm
import numpy as np

def get_data(head, getall=None, section=None, kind=None, order='arrow', ordertype='desc'):
    
    '''
        order = [arrow, posttime, money, area]
        ordertype = [asc, desc]
    '''
    
    oreder_list =  ['arrow', 'posttime', 'money', 'area']
    ordertype_list = ['asc', 'desc']

    initurl = 'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&type=1&shType=clinch'
    url = initurl + '&order=%s&orderType=%s&kind=%s&section=%s&searchtype=1'%(order, ordertype, kind, section)
    result = requests.get(url, headers = head, timeout=10).text
    result = json.loads(result)
    try:
        num_data = int(result['records'].replace(',', ''))
    except:
        num_data = int(result['records'])

    if not getall: # 只顯示預設50筆資料
        return result
    else:
        custdata = []

        '''
            由於591一次只能查詢20000筆，升序降序總共可得40000筆。
        '''
        total_page = min(399, num_data//50)
        if 40000 < num_data:
            
            for ord in oreder_list:
                for ordt in ordertype_list:
                    bigurl = initurl + '&order=%s&orderType=%s&kind=%s&section=%s&searchtype=1'%(ord, ordt, kind, section)
                    for page in tqdm(range(total_page+1)):
                        pageurl = bigurl + '&firstRow=%s&totalRows=%s'%(page*50, num_data)
                        result = requests.get(pageurl, headers = head, timeout=10).text
                        result = json.loads(result)

                        '''
                            依據使用者需求這裡可以自行取得需要的資料
                        '''
                        for d in result['data']['data']:
                            custdata.append(d['post_id'])
            
            custdata = list(set(custdata))
            print('number of rent data excess 40000')
            print('only get %s/%s'%(len(custdata), num_data))
            return custdata
        else:

            for page in tqdm(range(total_page+1)):
                try:
                    pageurl = url+'&firstRow=%s&totalRows=%s'%(page*50, num_data)
                    result = requests.get(pageurl, headers = head, timeout=10).text
                    result = json.loads(result)
                    '''
                    依據使用者需求這裡可以自行取得需要的資料
                    '''
                    for d in result['data']['data']:
                        custdata.append(d['post_id'])
                except:
                    pass
            '''
                如果大於20000筆，則須按照反序多抓一批資料。
            '''
            if 20000 <= num_data <= 40000:
                url = 'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&type=1&shType=clinch&order=%s&orderType=%s&kind=%s&section=%s&searchtype=1'%(order, 'asc', kind, section)
                last_page = (num_data-20000)//50
                for page in range(last_page+1):
                    try:
                        pageurl = url+'&firstRow=%s&totalRows=%s'%(page*50, num_data)
                        result = requests.get(pageurl, headers = head, timeout=10).text
                        result = json.loads(result)
                        for d in result['data']['data']:
                            custdata.append(d['post_id'])
                    except:
                        pass
            print('data completed , %s/%s '%(len(set(custdata)), num_data))

            return custdata


