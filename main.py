from email.headerregistry import Address
from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import shutil
import os
from selenium.webdriver.chrome.service import Service
from pandas import read_excel
from selenium.webdriver.common.by import By
import pandas as pd

#data
ser = Service('/media/apps/usr/bin/geckodriver')
waitingTime = 3
my_sheet = 'Sheet1'
file_name = 'Addresses.xlsx'
addresses = []
seed = "enter your seed here"
password = "enter any temporary pass here"
nft = "https://opensea.io/assets/matic/0x2953399124f0cbb46d2cbacd8a89cf0599974963/102802638809950387088771308260732218407868249031415453701960212136921334284388"

# #driver
driver = webdriver.Firefox(service=ser)
driver.install_addon('Metamask.xpi',temporary=False)
actions = ActionChains(driver)


# #openUrl
url = "https://opensea.io/"
driver.get(url)


#logs the user in
def loginMetamask():
    c = driver.window_handles[0]
    #switch to tab browser
    driver.switch_to.window(c)
    c = driver.window_handles[1]
    #switch to tab browser
    driver.switch_to.window(c)
    l=driver.find_element(by=By.XPATH,value = """/html/body/div[1]/div/div[2]/div/div/div/button""")
    l.click()
    l=driver.find_element(by=By.XPATH,value = """/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button""")
    l.click()
    l=driver.find_element(by=By.XPATH,value = """/html/body/div[1]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]""")
    l.click()
    l=driver.find_element(by=By.XPATH,value = """//*[@id="import-srp__srp-word-0"]""")
    l.click()
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    l=driver.find_element(by=By.XPATH,value = """//*[@id="password"]""")
    l.click()
    actions.send_keys(password).perform()
    l=driver.find_element(by=By.XPATH,value = """//*[@id="confirm-password"]""")
    l.click()
    actions.send_keys(password).perform()
    l=driver.find_element(by=By.XPATH,value = """//*[@id="create-new-vault__terms-checkbox"]""")
    l.click()
    l=driver.find_element(by=By.XPATH,value = """//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button""")
    l.click()
    time.sleep(waitingTime*3)
    c = driver.window_handles[0]
    #switch to tab browser
    driver.switch_to.window(c)
    c = driver.window_handles[1]
    #switch to tab browser
    driver.switch_to.window(c)
    driver.get("https://opensea.io/assets/matic/0x2953399124f0cbb46d2cbacd8a89cf0599974963/102802638809950387088771308260732218407868249031415453701960212136921334284388")   

def login():
    time.sleep(waitingTime*2)
    l=driver.find_element(by=By.XPATH,value = """/html/body/div[1]/div/div[1]/nav/ul/div/li/button""")
    l.click()
    l=driver.find_element(by=By.XPATH,value = """/html/body/div[1]/div/aside[2]/div[2]/div/div[2]/ul/li[1]/button/div[2]/span""")
    l.click()
    time.sleep(waitingTime)
    mainPage = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != mainPage:
            sign = handle
    driver.switch_to.window(sign)
    time.sleep(waitingTime*2)
    l=driver.find_element(by=By.XPATH,value = """/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/button[2]""")
    l.click()
    l=driver.find_element(by=By.XPATH,value = """/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]""")
    l.click()
    driver.switch_to.window(mainPage)
    time.sleep(waitingTime)
    driver.get("https://opensea.io/collection")
    driver.get("https://opensea.io/collection/snoopdob")
    driver.get(nft)

def sendNFT(address):
    actions = ActionChains(driver)
    time.sleep(waitingTime*3)
    l=driver.find_elements(by=By.XPATH,value = "//*[contains(text(), 'send')]")
    l = l[0]
    l.click()
    time.sleep(waitingTime)
    actions.send_keys(Keys.TAB).perform()
    time.sleep(waitingTime)
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    actions.send_keys("1").perform()
    actions.send_keys(Keys.TAB).perform()
    
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    actions.send_keys(address)
    actions.send_keys(Keys.TAB).perform()
    # time.sleep(waitingTime)
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(waitingTime)
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    # time.sleep(waitingTime)
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(waitingTime)
    mainPage = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != mainPage:
            sign = handle
    driver.switch_to.window(sign)
    time.sleep(waitingTime*2)
    l=driver.find_element(by=By.XPATH,value = """/html/body/div[1]/div/div[2]/div/div[3]/div[1]/img""")
    l.click()
    l=driver.find_element(by=By.XPATH,value = """/html/body/div[1]/div/div[2]/div/div[4]/button[2]""")
    l.click()
    driver.switch_to.window(mainPage)
    time.sleep(waitingTime*3)
    try:
        transId=driver.find_element(by=By.XPATH,value = """/html/body/div[12]/div/div/div/div[1]/section/section/div/div/div[2]/div[2]/a""")
        transId = transId.get_attribute('href')
    except:
        transId = "Failed"
    time.sleep(waitingTime)
    driver.refresh()
    driver.get(nft)
    return transId

def sync():
    address = []
    status = []
    sync_data = open('report.txt','r')
    for i in sync_data.readlines():
        i = i.strip()
        data = i.split(',')
        address.append(data[0])
        status.append(data[1])
    sync_data.close()
    sync_data = pd.DataFrame(list(zip(address, status)),columns =['Address', 'Status'])
    # print(sync_data.head())
    df = read_excel(file_name, sheet_name = my_sheet)
    # print(df.head())
    for i in range(len(sync_data['Status'])):
        df['Status'][i] = sync_data['Status'][i]
    df.to_excel(file_name,sheet_name=my_sheet, index = False)

loginMetamask()
login()
print("ready to send")


df = read_excel(file_name, sheet_name = my_sheet)
for i in range(len(df["Address"])):
    stts = df["Status"][i]
    address = df["Address"][i]
    if stts=="Failed" or stts=="Pending":
        print("Sending to : ")
        try:
            print(address)
            transId = sendNFT(address)
            print(transId)
            writr = open('report.txt','a')
            writr.write(address+','+transId)
            writr.write("\n")
            writr.close()
            stts = transId
        except:
            df["Status"][i] = "Failed"
            stts = "Failed"
            writr = open('report.txt','a')
            writr.write(address+','+stts)
            writr.write("\n")
            writr.close()
            # df.to_excel(file_name,sheet_name=my_sheet, index = False)
    else:
        writr = open('report.txt','a')
        writr.write(address+','+stts)
        writr.write("\n")
        writr.close()
sync()