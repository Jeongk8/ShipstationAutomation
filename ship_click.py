from selenium import webdriver
from time import sleep
from slackclient import SlackClient





token = ""      # found at https://api.slack.com/web#authentication
sc = SlackClient(token) 





def slack_message(message):
    
    sc.api_call(
    "chat.postMessage", channel="#python_shipstation", text= message,
    username='Grace Assistant :)', icon_emoji=':smile:')
    
   
 
def log_in():
    
    chrome_path = r"C:\\Library\\chromedriver_win32\\chromedriver.exe"
    global driver
    driver = webdriver.Chrome(chrome_path)
    
    
    slack_message("starting")
    
    driver.set_window_size(1280,1024)
    driver.get("https://ss4.shipstation.com/")
    sleep(5)
    driver.find_element_by_id("username").send_keys("scho")
    driver.find_element_by_id("password").send_keys("9838Research.")
    driver.find_element_by_id("btn-login").click()
    
    slack_message("Logging In")
    sleep(5)
    driver.get("https://ss4.shipstation.com/#/orders")
    sleep(2)
    driver.find_element_by_xpath("""//a[@class="btn-toggle-adv-search"]""").click()
    sleep(1)
    stores = driver.find_elements_by_xpath("""//span[@class="filter-option pull-left"]""")
    for x in stores:
        if x.text == "(Any)":
            x.click()
    fil_store = driver.find_elements_by_xpath("""//ul[@class="dropdown-menu inner selectpicker"]/li/a/span""")
    for x in fil_store:
        if x.text == "Spigen Inc": x.click()
        if x.text == "Spigen Shopify": x.click()
        
    for x in stores:
        if x.text == "6 of 6 selected": x.click()
        
    for x in fil_store:   
        if x.text == "Awaiting Payment":x.click()
        if x.text == "On Hold":x.click()
        if x.text == "Pending Fulfillment": x.click()
        if x.text == "Shipped": x.click()
        if x.text == "Cancelled": x.click()
    
    search_sku = driver.find_elements_by_xpath("""//input[@class="form-control input-sm"]""")
    for x in search_sku:
        if x.get_attribute("name") == "ItemSku":
            x.send_keys("000EM20634")
    
    driver.find_element_by_xpath("""//a[@class="btn btn-block btn-success do-search"]""").click()
    

    sleep(4)
    
    
def execute():
    

    sleep(3)
     
     
    carriers = driver.find_elements_by_xpath("""//a[@class="carrier-dropdown dropdown-toggle editor"]""")
    links = driver.find_elements_by_xpath("""//text/a[@class="ordernumber"]""")
    skus = driver.find_elements_by_xpath("""//td[@data-column="ItemSku"]""")
    status = driver.find_elements_by_xpath("""//td[@data-column="OrderStatusID"]""")

    slack_message("Now searching...")

    
    open("C:\\Library\\workspace\\ship_world\\order_log.txt","a")
    #file.close()
    file = open("C:\\Library\\workspace\\ship_world\\order_log.txt","r")

    
    order_nums = [x[:-1] for x in file.readlines()]
    file.close()
    #file = open("order_log.txt","a")
    for a,b,c,d in zip(links,carriers,skus,status):
        #print(b.text.encode())
        
        if b.text.encode() in [b'Express Worldwide',b'FedEx International Priority\xc2\xae',b'Globegistics eCom Packet',b'Globegistics eCom IPA',b'USPS First Class Mail Intl'] and c.text == "(Multiple Items)" and d.text == "Awaiting Shipment" and a.text not in order_nums:
            order_num = a.text

            a.click()

            sleep(1)
            price = driver.find_elements_by_xpath("""//ul[@class="itemsContainer"]/li/form/div/div[3]/input""")
            skuss = driver.find_elements_by_xpath("""//span[@data-name = "SKU"]""")
            
            
            for x in skuss:
                if "000EM20634" in x.text:
                    for y in price:
                        if y.get_attribute("value") == "0":
                            y.clear()
                            y.send_keys("0.01")
                            slack_message(order_num + " Price Fixed")
                            file = open("C:\\Library\\workspace\\ship_world\\order_log.txt","a")
                            file.write(order_num+"\n")
                            file.close()
                            #log.append(a.text)
                            sleep(1)
            driver.find_element_by_xpath("""//button[@class="close pull-right"]""").click()
            
            sleep(1)
    


def main():
    
    try:
        log_in()
        total_record = driver.find_element_by_xpath("""//em[@class="total-record-no"]""").text
        total_record = total_record.split(",")
        total_record = int("".join(total_record))
        slack_message("Currently there are " + str(total_record)+" orders")
        if total_record <= 500:
            execute()
        
        if total_record > 500:
            for x in range(int(total_record/500)+1):
                #print(x)
                if x == int(total_record/500):
                    #print("works")
                    execute()
                else:
                    execute()
                    sleep(2)
                    driver.find_element_by_xpath("""//a[@class="nextPage "]""").click()
                    sleep(8)
        slack_message("Finished!")
        driver.quit()
    except Exception as e:
        slack_message(str(e))
        driver.quit()
		








    

            

    





    
