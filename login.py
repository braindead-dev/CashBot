import requests
from datetime import datetime
import json

# time parse
def parsedt():
    dt = datetime.now()
    if len(str(dt.month)) ==1:
        month = "0"+str(dt.month)
    if len(str(dt.day)) ==1:
        day = "0"+str(dt.day)
    return str(dt.year) + "-" + month + "-" + day + "T" + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.hour) + ":06-07:00;;"

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def get_info(cookie):
    headers_withcred1 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'cash_web_session='+cookie,
        'referer': 'https://cash.app/account/activity',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',

    }
    cstoken_webreq = requests.get(url="https://cash.app/account/activity", headers = headers_withcred1)
    sourcetext = cstoken_webreq.text
    cstoken = find_between(sourcetext, "var csrfToken = '", "';" )

    headers_withcred2 = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "2",
        "content-type": "application/json",
        "cookie": "cash_web_session="+cookie, #essential
        "origin": "https://cash.app",
        "referer": "https://cash.app/login",
        "sec-ch-ua": '''\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"''',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '''"Windows"''',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "time-zone": parsedt(),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "x-bt-id": "0.0",
        "x-csrf-token": cstoken, #essential
        "x-js-id": "no",
        "x-request-signature": "replace with new",
        "x-request-uuid": "replace with new",
        "x-requested-with": "XMLHttpRequest"
    }

    info_results = requests.post(url="https://cash.app/2.0/cash/get-profile", headers = headers_withcred2, data='''{}''')

    result_text = info_results.text
    return json.loads(result_text)
    
def transactions(cookie):
    headers_withcred1 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'cash_web_session='+cookie,
        'referer': 'https://cash.app/account/activity',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',

    }
    cstoken_webreq = requests.get(url="https://cash.app/account/activity", headers = headers_withcred1)
    sourcetext = cstoken_webreq.text
    cstoken = find_between(sourcetext, "var csrfToken = '", "';" )

    headers_withcred = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "138",
        "content-type": "application/json",
        "cookie": "cash_web_session="+cookie, #essential
        "origin": "https://cash.app",
        "referer": "https://cash.app/account/activity",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "time-zone": parsedt(),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "x-bt-id": "0.0",
        "x-csrf-token": cstoken, #essential
        "x-js-id": "no",
        "x-request-signature": "REPLEACE_WITH_NEW",
        "x-request-uuid": "REPLEACE_WITH_NEW",
        "x-requested-with": "XMLHttpRequest"
    }
    
    info_results = requests.post(url="https://cash.app/2.0/cash/get-paged-sync-entities", headers = headers_withcred, data='''{"limit":50,"order":"DESC","show_completed":true,"show_in_flight":true,"show_failed_transfers":true,"show_sent":true,"show_received":true}''')
    result_text = info_results.text
    return result_text

def update_cash_status(cookie, int_amount, random_note):
    transaction_list = transactions(cookie)
    whole_number_amount = int_amount.split('.')[0]
    decimal_amount = int_amount.split('.')[1]
    if decimal_amount == "00":
        int_amount = whole_number_amount

    search_for = "sent you $" + int_amount + " for " + random_note
    if search_for in transaction_list:
        return "TRANSACTION CONFIRMED"
    else:
        return "TRANSACTION UNCONFIRMED"