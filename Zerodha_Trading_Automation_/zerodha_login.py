# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 13:14:10 2022

@author: HD
"""

from kiteconnect import KiteConnect
from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
from pyotp import TOTP

cwd = os.chdir("C:\\Users\\HD\\.conda\\envs\\algo\\ZerodhaAPI")

def autologin():
    token_path = "credentials.txt"
    print(token_path)
    key_secret = open(token_path,'r').read().split()
    kite = KiteConnect(api_key=key_secret[0])
    service = webdriver.chrome.service.Service('./chromedriver')
    service.start()
    #options =   webdriver.ChromeOptions()
    #options.add_argument('--headless') this code will not render page
    #options = options.to_capabilities()
    driver = webdriver.Remote(service.service_url,options=webdriver.ChromeOptions())
    driver.get(kite.login_url())
    driver.implicitly_wait(10)
    driver.find_element
    
    username = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input")
    password = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input")
    username.send_keys(key_secret[2])
    password.send_keys(key_secret[3])
    
    driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button").click()
    
    totp = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/input") 
    totp_token = TOTP(key_secret[4])
    token = totp_token.now()
    print(token)
    totp.send_keys(token)
    
    driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[3]/button").click()
    time.sleep(10)
    
    request_token = driver.current_url.split('request_token=')[1][:32]
    with open('request_token.txt','w') as the_file:
        the_file.write(request_token)
    driver.quit()
    
autologin()


request_token = open("request_token.txt",'r').read()
key_secret = open("credentials.txt",'r').read().split()
kite = KiteConnect(api_key = key_secret[0])
data = kite.generate_session(request_token,api_secret = key_secret[1])
with open('access_token.txt','w') as file:
    file.write(data['access_token'])
        