import requests
from xml import etree
headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}
res = requests.get(url= 'https://www.cnsoftbei.com/',headers=headers).text
# res = requests.get(url='https://www.fhyx.com/list/left-h_all_one_3_0_0_3_0_1_0_0_0_0_0_0.html', headers=headers).text
print(res)