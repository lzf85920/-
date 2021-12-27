import json
import re
from selenium import webdriver
import time

## TODO
chrome_drive_path = '/Users/lee/Downloads/chromedriver'

#click region and get section id
def get_section_id(browser, sec_num):
    click_count = 0
    
    section = {}
    
    for i in browser.find_elements_by_class_name('vue-filter-item'):

        if click_count >= 1:
            
            
            section_name = i.text
            i.click()

            time.sleep(1)
            # extrac section id from url
            section_id = int(re.findall(r'=(\d+)&', browser.current_url)[-1])
            section[section_name] = section_id
            
            # cacel section
            i.click()
            
        click_count+=1
        if click_count == sec_num:
            break
            
    return section


def get_location_variable(chrome_drive_path):


    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    chromeOptions.add_argument('ignore-certificate-errors') 
    browser = webdriver.Chrome(chrome_drive_path,options=chromeOptions)
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow'}}
    browser.get('https://rent.591.com.tw/?shType=clinch&order=money&orderType=asc&kind=1&region=1') 

    location = {
        '台北市':{'region_id' : 1},
        '基隆市':{'region_id' : 2},
        '新北市':{'region_id' : 3},
        '桃園市':{'region_id' : 6},
        '新竹市':{'region_id' : 4},
        '新竹縣':{'region_id' : 5},
        '宜蘭縣':{'region_id' : 21},
        '台中市':{'region_id' : 8},
        '彰化縣':{'region_id' : 10},
        '雲林縣':{'region_id' : 14},
        '苗栗縣':{'region_id' : 7},
        '南投縣':{'region_id' : 11},
        '高雄市':{'region_id' : 17},
        '台南市':{'region_id' : 15},
        '嘉義市':{'region_id' : 12},
        '嘉義縣':{'region_id' : 13},
        '屏東縣':{'region_id' : 19},
        '台東縣':{'region_id' : 22},
        '花蓮縣':{'region_id' : 23},
        '澎湖縣':{'region_id' : 24},
        '金門縣':{'region_id' : 25},
        '連江縣':{'region_id' : 26}, 
    }

    for reg, reg_id in location.items():
        
        # get region 
        browser.get('https://rent.591.com.tw/?shType=clinch&region=%s'%reg_id['region_id']) 
        time.sleep(3)
        # count total section
        section_num = len(browser.find_elements_by_class_name('town-list.clearfix')[0].text.split('\n'))
        
        location[reg]['section'] = get_section_id(browser, section_num)
    browser.quit()

    return location

loc_variable = get_location_variable(chrome_drive_path)


index = []
for k, v in loc_variable.items():
    for w, e in v['section'].items():
        index.append(e)

if len(set(index)) == len(index):
    print('success')
else:
    print('error')

print(loc_variable)





