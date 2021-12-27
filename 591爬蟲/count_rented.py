import pandas as pd
import requests
import json
import urllib.parse

from requests.api import head
import utils.get_token
import utils.rentlist

with open('c:\\Users\\user\\Downloads\\location_id.json', 'r', encoding='utf-8') as f:
    loc_index = json.load(f)

with open('c:\\Users\\user\\Downloads\\rent_kind.json', 'r', encoding='utf-8') as f:
    rent_kind = json.load(f)

rented = pd.DataFrame(columns=['縣市','行政區','整層住家','獨立套房','分租套房', '雅房','車位'])


renew_count = 0

csrf, xsrf_token, new_session = utils.get_token.get_token()

for reg, reg_data in loc_index.items():


    if renew_count >= 25:
        csrf, xsrf_token, new_session = utils.get_token.get_token()
        renew_count = 0

    region = urllib.parse.quote(reg)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'webp=1; PHPSESSID=gmposia4niqo9apeqpshhm3gl6; newUI=1; T591_TOKEN=gmposia4niqo9apeqpshhm3gl6; tw591__privacy_agree=0; _ga=GA1.3.18374178.1637760097; _ga=GA1.4.18374178.1637760097; __auc=ad3146f817d521bd9fd64ce3512; user_index_role=1; __utmc=82835026; __utmz=82835026.1637830661.1.1.utmcsr=rent.591.com.tw|utmccn=(referral)|utmcmd=referral|utmcct=/; new_rent_list_kind_test=0; is_new_index=1; is_new_index_redirect=1; last_search_type=1; _gid=GA1.3.1096370833.1639639587; _gid=GA1.4.1096370833.1639639587; __utma=82835026.18374178.1637760097.1639671651.1639711646.8; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A2515%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A11835533%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A9047197%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A1394%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A11723009%3B%7D%7D; house_detail_stat=%5B%7B%22type%22%3A%221%22%2C%22resource%22%3A%2214%22%2C%22post_id%22%3A%222258%22%7D%2C%7B%22type%22%3A%221%22%2C%22resource%22%3A%2214%22%2C%22post_id%22%3A%2219236%22%7D%2C%7B%22type%22%3A%221%22%2C%22resource%22%3A%2214%22%2C%22post_id%22%3A%2211867417%22%7D%2C%7B%22type%22%3A%221%22%2C%22resource%22%3A%2214%22%2C%22post_id%22%3A%222181%22%7D%5D; bid[pc][1.200.106.179]=3228; _gat_UA-97423186-1=1; XSRF-TOKEN='+xsrf_token+'; 591_new_session='+new_session+'; _gat=1; _dc_gtm_UA-97423186-1=1'+'; urlJumpIp='+str(reg_data['region_id'])+'; urlJumpIpByTxt='+region,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'X-CSRF-TOKEN': csrf,
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    for sec_name, sec_id in reg_data['section'].items():
        records = []
        for kind, kind_id in rent_kind.items():
            record = int(str(utils.rentlist.get_data(headers, getall=False, section=sec_id, kind=kind_id)['records']).replace(',', ''))
            records.append(record)
        print([reg, sec_name]+records)
        rented = rented.append(pd.DataFrame(data=[[reg, sec_name]+records], columns=['縣市','行政區','整層住家','獨立套房','分租套房', '雅房','車位']))

    renew_count += 1 

print(rented)

#rented.to_csv('c:\\Users\\user\\Downloads\\591crawler\\count_rented.csv', index=False, encoding='utf-8-sig')

