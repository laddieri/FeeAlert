import requests, time

BITCOIN_FEE_THRESHOLD = 10
BITCOIN_API_URL = 'https://mempool.space:8999/api/v1/fees/recommended'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
IFTTT_KEY_FILE = 'iftttKey.txt'

def get_fastest_bitcoin_fee():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json['fastestFee'])  # Convert the price to a floating point number

def get_ifttt_Key_from_file():
    f = open(IFTTT_KEY_FILE,'r')
    contents = f.read()
    return contents

def post_ifttt_webhook(event, value):
    data = {'value1': value}  # The payload that will be sent to IFTTT service
    ifttt_Key = get_ifttt_Key_from_file()
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event, ifttt_Key)
    requests.post(ifttt_event_url, json=data)  # Sends a HTTP POST request to the webhook URL

def main():
    while True:
        fee = get_fastest_bitcoin_fee()

        # Send an emergency notification
        if fee < BITCOIN_FEE_THRESHOLD:
            print('IFTTT event published. Fee: ' + fee)
            post_ifttt_webhook('bitcoin_low_fee', fee)
        else:
            print('Fees are too high to alert: ' + str(fee))

        time.sleep(5*60)  # Sleep for 5 minutes (for testing purposes you can set it to a lower number)

if __name__ == '__main__':
    main()
