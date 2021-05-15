"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config
from utils.serverchan_push import push_to_wechat

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies    

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content

def push_qq(msg):
    """
    推送消息到QQ酷推
    """
    if key == '':
        print("[注意] 未提供key，推送！个🍗")
    else:
        server_url = f"https://qmsg.zendee.cn/send/{key}?"
        params = {
             "msg": msg
        }
      
        response = requests.get(server_url, params=params)
        json_data = response.json()
        if json_data['reason'] == "操作成功":
            print(f"推送成功")
        else:
            print(f" 推送失败:鬼知道哪错了")
     
        print("QQ酷推鬼知道修改成功没")    


if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["COOKIES"]
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    resp = "什么值得买每日签到\n" + res
    print(res)
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY"]
    key = os.environ["KEY"]
    print('sc_key: ', SERVERCHAN_SECRETKEY)
    if isinstance(SERVERCHAN_SECRETKEY,str) and len(SERVERCHAN_SECRETKEY)>0:
        print('检测到 SCKEY， 准备推送')
        push_qq(resp))
        push_to_wechat(text = '什么值得买每日签到',
                        desp = str(res),
                        secretKey = SERVERCHAN_SECRETKEY)
    print('代码完毕')
