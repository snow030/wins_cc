import requests

url = 'https://translate-pa.googleapis.com/v1/translateHtml'
headers = {
    'content-type':'application/json+protobuf',
    'x-goog-api-key':'AIzaSyATBXajvzQLTDHEQbcpq0Ihe0vWDHmO520',
}

def trans_li(text_li,target,source='auto') -> list[str]:
    if len(text_li) == 0: return []
    response = requests.post(url,json=[[text_li,source,target],'te_lib'],headers=headers)
    if response.status_code == 200:
        return response.json()[0]
    else:
        raise response.raise_for_status()