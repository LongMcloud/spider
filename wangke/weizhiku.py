import requests
from time import *
from lxml import etree
def main():
    begin_time=time()
    url_course = "https://jsjzyk.36ve.com/?q=items/student/study/339964"
    url_save="https://jsjzyk.36ve.com/?q=items/study/current/save"
    headers = {
        'Cookie': "__root_domain_v=.36ve.com; _qddaz=QD.851165895872734; major_id=2; has_js=1; Hm_lvt_47b17a3a4d3730384eb68c04970c6624=1685806348,1685858296; uc_local_login=2; easy_password=1; login_flag=0; user_sys_key=g3-shvpCMi6_I3YUHx3qOCd1ckl-2E5iKAdjOt4MG0guQDuJchr74GDjsvJ6HAd3oiYiXLZt-nIzm4XinzN75-MgK_ME2gHr3PHyJtTkEfJ_YSg_N7VvIZR_7qR-J8YvoTFj5vFv3wZ2FqYj3LFjiXX; uc_uid=80523; SESS336f456991f32c52141d3f4044c89382=oZUur6uufpI8b2-bL-h9LCk9TEECjE3VBpYHIsMVR3E; _qdda=3-1.22ytec; _qddab=3-m462aa.lih7b8fq; Hm_lpvt_47b17a3a4d3730384eb68c04970c6624=1685869881"







    }

    response = requests.get(url_course, headers=headers)
    # while True:
    #     try:
    #         response = requests.get(url_course, headers=headers, timeout=(30, 50), verify=False)
    #         break
    #     except:
    #         print("Connection refused by the server..")
    #         print("Let me sleep for 5 seconds")
    #         print("ZZzzzz...")
    #         sleep(5)
    #         print("Was a nice sleep, now let me continue...")
    #         continue

    html = etree.HTML(response.text)
    item_id = html.xpath("//li/a[@class='itemtitle']/@item_id")
    module_id = html.xpath("//li/a[@class='itemtitle']/@module_id")

    for x, y in zip(item_id, module_id):

        From = {
            "time": "1000",
            "fid": '47512',
            "totaltime": "1000",
            "resource": "0",
            "from": "http://jsjzyk.36ve.com/?q=items/student/study/68149/{}/{}".format(y, x),
            "item_id": '{}'.format(x)
        }

        response1=requests.post(url_save, headers=headers,data=From)
        print(response1)
    print("完成了！！！")
    end_time=time()
    middle = end_time-begin_time
    print(middle)

if __name__ == '__main__':
    main()