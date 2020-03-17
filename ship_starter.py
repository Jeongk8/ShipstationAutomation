
import random, string
import time
from slackclient import SlackClient
token = ""# found at https://api.slack.com/web#authentication
sc = SlackClient(token)

def slack_message(message,chan):
    
    sc.api_call(
    "chat.postMessage", channel= chan, text= message,
    username='Python_Bot', icon_emoji=':smile:')


sc.api_call(
"chat.postMessage", channel="#python_sion", text= "Type your Command!",
username='Forecasting Update', icon_emoji=':smile:')

sc.api_call(
"chat.postMessage", channel="#python_shipstation", text= "Type your Command!",
username='Grace Assistant :)', icon_emoji=':smile:')


while True:
   
    try:
        if sc.rtm_connect():
          while True:
              for x in sc.rtm_read():
                  try:
                      keyword = x['text']
                      ts = float(x['ts'])
                      ts = int(ts)
                      print(keyword)
                      print(ts)
                      print(int(time.time()))
                      if keyword == "U100" and int(time.time()) - ts < 4:
                        print("second")
                        from ship_click import main as start
                        start()

                    
                        
                      elif keyword == "fcst" and int(time.time()) - ts < 4:
                          print("third")
                          from SQ_FCST import main as start
                          slack_message("Starting..","#python_sion")
                          slack_message("Working...","#python_sion")
                          start()
                          slack_message("Finished please check log","#python_sion")
                      elif keyword =="sct-upt" and int(time.time()) - ts < 4:
                          from scout_download import main as start
                          slack_message("Starting..","#python_sion")
                          start()
                          slack_message("Finished Please check log","#python_sion")
                      elif keyword =="pm update" and int(time.time()) - ts < 4:
                          slack_message("Starting..","#python_log")
                          import starter as start
                          start()
                              
                      elif keyword == "u here?" and int(time.time()) - ts < 4:
                         slack_message("I'm still running!!","#python_shipstation")
                         slack_message("I'm still running!!","#python_sion")
                          
                   
                         
                  except: pass
                  time.sleep(1)
        else:
          print("Connection Failed, invalid token?")
    except: pass
        
        


