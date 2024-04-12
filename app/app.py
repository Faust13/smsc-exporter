from settings import SMSC, METRICS, STAT_INTERVAL
import smsc_api
from flask import Flask, make_response
import datetime
import logging
#from pythonjsonlogger import jsonlogger

app = Flask(__name__)

#logging.basicConfig(level=LOG['LEVEL'])

logger = logging.getLogger()
logHandler = logging.StreamHandler()
# if LOG['FORMAT'] == 'json':
#     formatter = jsonlogger.JsonFormatter()
# else:
#     formatter = LOG['FORMAT']
# logHandler.setFormatter(formatter)
# logger.addHandler(logHandler)

def generateMetrics():
    curr_dt = datetime.datetime.now()
    timestamp = int(round(curr_dt.timestamp() * 1000))
    if STAT_INTERVAL=='day':
        today = datetime.date.today().strftime("%d.%m.%Y")
    elif STAT_INTERVAL=='week':
        today = (datetime.date.today()-datetime.timedelta(days=7)).strftime("%d.%m.%Y")
    elif STAT_INTERVAL=='month':
        today = (datetime.date.today()-datetime.timedelta(days=30)).strftime("%d.%m.%Y")

        

    if METRICS['BALANCE']==True:
        balance_raw = smsc_api.getBalance(SMSC['ENDPOINT'], SMSC['LOGIN'], SMSC['PASSWORD'])
        balance_descrion = "# HELP csms_balance Current balance account.\n"
        balance_type = '# TYPE csms_balance gauge\n'
        balance = f"csms_balance {balance_raw} {timestamp}\n"
        data = balance_descrion + balance_type + balance

    if METRICS["TOTAL_COST"]==True:
        messages_raw = smsc_api.getMessages(SMSC['ENDPOINT'], SMSC['LOGIN'], SMSC['PASSWORD'], today, SMSC['MESSAGE_LIMIT'])
        total_cost_description = '# HELP csms_messages_total_cost Total cost of all sent SMS messages.\n'
        total_cost_type = '# TYPE csms_messages_total_cost gauge\n'
        total_cost = f"csms_messages_total_cost {messages_raw[0]} {timestamp}\n"
    
        data = data + total_cost_description + total_cost_type + total_cost
    
        total_sent_description = '# HELP csms_messages_total_sent Total number of all sent SMS messages.\n'
        total_sent_type = '# TYPE csms_messages_total_sent counter\n'
        total_sent = f"csms_messages_total_sent {messages_raw[1]} {timestamp}\n"

        data = data + total_sent_description + total_sent_type + total_sent

        messages_counters = messages_raw[2]

    notfound_description = '# HELP csms_messages_notfound Total number of all sent SMS messages.\n'
    notfound_type = '# TYPE csms_messages_notfound counter\n'
    notfound = f"csms_messages_notfound {messages_counters['notfound']} {timestamp}\n"

    data = data + notfound_description + notfound_type + notfound

    stopped_description = '# HELP csms_messages_stopped Total number of all sent SMS messages.\n'
    stopped_type = '# TYPE csms_messages_stopped counter\n'
    stopped = f"csms_messages_stopped {messages_counters['stopped']} {timestamp}\n"

    data = data + stopped_description + stopped_type + stopped

    waiting_description = '# HELP csms_messages_waiting Total number of all sent SMS messages.\n'
    waiting_type = '# TYPE csms_messages_waiting counter\n'
    waiting = f"csms_messages_waiting {messages_counters['waiting']} {timestamp}\n"

    data = data + waiting_description + waiting_type + waiting

    transferred_description = '# HELP csms_messages_transferred Total number of all sent SMS messages.\n'
    transferred_type = '# TYPE csms_messages_transferred counter\n'
    transferred = f"csms_messages_transferred {messages_counters['transferred']} {timestamp}\n"

    data = data + transferred_description + transferred_type + transferred

    delivered_description = '# HELP csms_messages_delivered Total number of all sent SMS messages.\n'
    delivered_type = '# TYPE csms_messages_delivered counter\n'
    delivered = f"csms_messages_delivered {messages_counters['delivered']} {timestamp}\n"

    data = data + delivered_description + delivered_type + delivered

    readed_description = '# HELP csms_messages_readed Total number of all sent SMS messages.\n'
    readed_type = '# TYPE csms_messages_readed counter\n'
    readed = f"csms_messages_readed {messages_counters['readed']} {timestamp}\n"

    data = data + readed_description + readed_type + readed

    expired_description = '# HELP csms_messages_expired Total number of all sent SMS messages.\n'
    expired_type = '# TYPE csms_messages_expired counter\n'
    expired = f"csms_messages_expired {messages_counters['expired']} {timestamp}\n"

    data = data + expired_description + expired_type + expired

    link_clicked_description = '# HELP csms_messages_link_clicked Total number of all sent SMS messages.\n'
    link_clicked_type = '# TYPE csms_messages_link_clicked counter\n'
    link_clicked = f"csms_messages_link_clicked {messages_counters['link_clicked']} {timestamp}\n"

    data = data + link_clicked_description + link_clicked_type + link_clicked

    unable_delivery_description = '# HELP csms_messages_unable_delivery Total number of all sent SMS messages.\n'
    unable_delivery_type = '# TYPE csms_messages_unable_delivery counter\n'
    unable_delivery = f"csms_messages_unable_delivery {messages_counters['unable_delivery']} {timestamp}\n"

    data = data + unable_delivery_description + unable_delivery_type + unable_delivery

    wrong_number_description = '# HELP csms_messages_wrong_number Total number of all sent SMS messages.\n'
    wrong_number_type = '# TYPE csms_messages_wrong_number counter\n'
    wrong_number = f"csms_messages_wrong_number {messages_counters['wrong_number']} {timestamp}\n"

    data = data + wrong_number_description + wrong_number_type + wrong_number

    blocked_description = '# HELP csms_messages_blocked Total number of all sent SMS messages.\n'
    blocked_type = '# TYPE csms_messages_blocked counter\n'
    blocked = f"csms_messages_blocked {messages_counters['blocked']} {timestamp}\n"

    data = data + blocked_description + blocked_type + blocked

    out_of_money_description = '# HELP csms_messages_out_of_money Total number of all sent SMS messages.\n'
    out_of_money_type = '# TYPE csms_messages_out_of_money counter\n'
    out_of_money = f"csms_messages_out_of_money {messages_counters['out_of_money']} {timestamp}\n"

    data = data + out_of_money_description + out_of_money_type + out_of_money

    number_unreachable_description = '# HELP csms_messages_number_unreachable Total number of all sent SMS messages.\n'
    number_unreachable_type = '# TYPE csms_messages_number_unreachable counter\n'
    number_unreachable = f"csms_messages_number_unreachable {messages_counters['number_unreachable']} {timestamp}\n"

    data = data + number_unreachable_description + number_unreachable_type + number_unreachable

    single_msg_description = '# HELP csms_message Info about of sent SMS message with extra tags.\n'
    single_msg_type = '# TYPE csms_message counter\n'
    data = data + single_msg_description + single_msg_type
    for item in messages_raw[3]:
        data = data + f'{str(messages_raw[3][item])} 1 {timestamp}\n'

    return data
 


#### FRONT ####
@app.route('/metrics', methods=['GET'])
def metircs():

    response = make_response(generateMetrics(), 200)
    response.mimetype = "text/plain"
    return response

if __name__ == "__main__":
    app.run(host= '0.0.0.0')