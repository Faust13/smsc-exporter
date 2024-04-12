import os

SMSC = {
    "ENDPOINT" : os.environ.get('SMSC_ENDPOINT', 'https://smsc.ru/sys').strip(),
    "LOGIN" : os.environ.get('SMSC_LOGIN', 'test').strip(),
    "PASSWORD" : os.environ.get('SMSC_PASSWORD', 'test').strip(),
    "MESSAGE_LIMIT": os.environ.get('SMSC_MESSAGE_LIMIT', 1000)
}
METRICS = {
    "BALANCE" : os.environ.get('METRIC_BALANCE', True),
    "TOTAL_COST": os.environ.get('METRIC_TOTAL_COST', True),
    "TRACE_MESAGES" : os.environ.get('EXPORTER_TRACE_MESAGES', True),

}
STAT_INTERVAL = os.environ.get('STAT_INTERVAL', 'day')
# LOG = {
#     "FORMAT" : os.environ.get('LOG_FORMAT', 'json'),
#     "LEVEL" : os.environ.get("LOG_LEVEL", "INFO").upper
#     }