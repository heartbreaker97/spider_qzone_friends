from selenium import webdriver
from time import sleep
import json

chromedriver = 'C:/Users/13180/AppData/Local/Google/Chrome/Application/chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.get('https://user.qzone.qq.com/1318074793/main')
driver.switch_to.frame('login_frame')
#找到账号密码登陆的地方
driver.find_element_by_id('switcher_plogin').click()
driver.find_element_by_id('u').send_keys('1318074793')
driver.find_element_by_id('p').send_keys('962464myr')
driver.find_element_by_id('login_button').click()
#保存本地的cookie
sleep(1)
cookies = driver.get_cookies()
cookie_dic = {}
for cookie in cookies:
    if 'name' in cookie and 'value' in cookie:
        cookie_dic[cookie['name']] = cookie['value']
    with open('cookie_dict.txt', 'w') as f:
        json.dump(cookie_dic, f)