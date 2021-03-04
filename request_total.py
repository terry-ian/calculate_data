headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
            }
import json
ttt = session_requests.get('http://zfcj.gz.gov.cn/zfcj/tjxx/mrxjspfksxxRequest' , headers=headers )
output_data=ttt.json()
output_data=json.loads(output_data)['data']
pd.json_normalize(output_data)