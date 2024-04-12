import requests
from collections import defaultdict


def getMessages(smsc_host: str, smsc_user: str, smsc_password: str, start_date: str, smsc_limit : int):
#https://smsc.ru/sys/get.php?get_messages=1&login=test&psw=oass&start=01.03.2024&end=04.04.2024&cnt=1000&fmt=3

    try:
        link = f"{smsc_host}/get.php?get_messages=1&login={smsc_user}&psw={smsc_password}&start={start_date}&cnt={str(smsc_limit)}&fmt=3"
        print(link)
    except:
        print(Exception)
    
    request = requests.get(link)
    
    responce = request.json()
    total_cost= 0
    msg=defaultdict(int) 
    msg_list = defaultdict(int)

    for item in responce:
        current_index = responce.index(item)
        #clenup data for privacy and remove trash
        del item['message']
        del item['phone']
        if item['status'] == -3:
                msg['notfound'] += 1
        elif item['status'] == -2:
                msg['stopped'] += 1
        elif item['status'] == -1:
                msg['waiting'] += 1
        elif item['status'] == 0:
                msg['transferred'] += 1
        elif item['status'] == 1:
                msg['delivered'] += 1
        elif item['status'] == 2:
                msg['readed'] += 1
        elif item['status'] == 3:
                msg['expired'] += 1
        elif item['status'] == 4:
                msg['link_clicked'] += 1
        elif item['status'] == 20:
                msg['unable_delivery'] += 1
        elif item['status'] == 22:
                msg['wrong_number'] += 1
        elif item['status'] == 23:
                msg['blocked'] += 1
        elif item['status'] == 24:
                msg['out_of_money'] += 1
        elif item['status'] == 25:
                msg['number_unreachable'] += 1
        total_cost = total_cost+float(item['cost'])
        
        msg_list[current_index] = f"""csms_message{{status="{item['status']}",
                                    last_timestamp="{int(round(item['last_timestamp']*1000))}",
                                    flag="{item['flag']}",
                                    send_date="{item['send_date']}",
                                    send_timestamp="{int(round(item['send_timestamp']*1000))}",
                                    cost="{item['cost']}",
                                    sender_id="{item['sender_id']}",
                                    status_name="{item['status_name']}",
                                    mccmnc="{item['mccmnc']}",
                                    country="{item['country']}",
                                    operator="{item['operator']}",
                                    region="{item['region']}",
                                    type="{item['type']}",
                                    sms_cnt="{item['sms_cnt']}",
                                    id="{item['id']}",
                                    int_id="{item['int_id']}",
                                    format="{item['format']}",
                                    crc="{item['crc']}"
                                    }}""".replace("\n","").replace("  ","")

    total_cost = round(total_cost, 2)
    messages_sent = len(responce)
    return(total_cost, messages_sent, msg, msg_list)

def getBalance(smsc_host: str, smsc_user: str, smsc_password: str):

    link = f"{smsc_host}/balance.php?login={smsc_user}&psw={smsc_password}&fmt=3"
    print(link)
    
    request = requests.get(link)
    
    responce = request.json()
    balance = responce['balance']
    return(balance)