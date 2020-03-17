from selenium import webdriver
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from time import sleep
import time
import os
import shutil
from datetime import datetime
from random import randint
from slackclient import SlackClient





token = ""      # found at https://api.slack.com/web#authentication
sc = SlackClient(token) 


def slack_message(message,chan):
    
    sc.api_call(
    "chat.postMessage", channel= chan, text= message,
    username='Forecasting_update', icon_emoji=':smile:')




def execute():
    
    chrome_path = r"C:\\Library\\chromedriver_win32\\chromedriver.exe"
    
    driver = webdriver.Chrome(chrome_path)
    slack_message("open..","#python_sion")
    driver.set_window_size(1480,1324)
    driver.get("http://scout.spigen.com/")
    sleep(3)
    driver.find_element_by_name("email").send_keys("spigen@spigen.com")
    driver.find_element_by_name("password").send_keys("square9975")
    driver.find_element_by_xpath("""//button[@class="btn btn-primary btn-block btn-flat"]""").click()
    sleep(3)
    slack_message("downloading..","#python_sion")
    driver.get("http://scout.spigen.com/sqirvine1")
    sleep(2)
    driver.find_element_by_xpath("""//a[@class="btn btn-default buttons-collection"]""").click()
    sleep(1)
    driver.find_element_by_xpath("""//li[@class="dt-button buttons-csv"]/a""").click()
    sleep(7)
    slack_message("download complete..","#python_sion")
    driver.quit()


def move():

    slack_message("moving file..","#python_sion")
    dap = dict() 
    for x in os.listdir("C:\\Users\\tommy\\Downloads"):
        if x[-4:] == ".csv":
            dap["C:\\Users\\tommy\\Downloads\\"+str(x)] = os.path.getmtime("C:\\Users\\tommy\\Downloads\\"+str(x))
    
    dap = {k:v for k,v in sorted(dap.items(), key = lambda x: -x[1])}
    final=''
    for k,x in dap.items():
        final = k
        break
        
    shutil.move(final,"C:\\Library\\scout_data\\scout_new")
    slack_message("moved","#python_sion")
    
def scout():
    for a,b,c in os.walk("C:\\Library\\scout_data\\scout_new"):
        
        dap = os.path.join(a,c[0])

    final=[]
    with open(dap, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            final.append(row)
    return final   

def scout_upload():

    yoyo = scout()[1:]
    half = int(len(yoyo)/2)
   
    pre= []
    for x in yoyo[:half]:
        pre = pre + x
    slack_message("added","#python_sion")
    cell_list = test.range(3,1,half+2,len(yoyo[0]))
      
    for b in zip(cell_list,pre):
        b[0].value = b[1]
    slack_message("Processing..","#python_sion")
    
    test.update_cells(cell_list)

    slack_message("50%..","#python_sion")
    pre2=[]
    other_half = half+2
    for y in yoyo[half:]:
        pre2 = pre2 + y
    
#       
    cell_list2 = test.range(other_half+1,1,len(yoyo)+2,len(yoyo[0]))
      
    for c in zip(cell_list2,pre2):
        c[0].value = c[1]
      
    test.update_cells(cell_list2)
      

    
def remove():
    for a,b,c in os.walk("C:\\Library\\scout_data\\scout_new"):
        dap = os.path.join(a,c[0])
        os.rename(dap,"C:\\Library\\scout_data\\scout_old\\"+str(randint(1000,10000000))+".csv")    
   
        
        

    
def main():
    try:
        global scope, creds, client,check,test
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Library\\workspace\\ship_world\\SQspreadsheet-6594fdac22511.json', scope)

        client = gspread.authorize(creds)
        check = client.open("eBiz Product Management").worksheet("Log")
        test = client.open("eBiz Product Management").worksheet("SQ Inventory")
        check.update_acell("E8",datetime.now())
        execute()
        move()
        scout_upload()
        remove()
        slack_message("Scout Inv Updated!","#python_sion")
        check.update_acell("B8",datetime.now())
        check.update_acell("C8","Success")
        check.update_acell("D8","")
    except Exception as e:
        check.update_acell("B8",datetime.now())
        check.update_acell("C8","Fail")
        check.update_acell("D8",str(e))


