#!/usr/bin/python
#-*-coding:utf-8 -*-
import unittest
import json
import requests
import random
import sys

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.s = requests.session()
        self.url_home="http://111.13.63.2:9800"
        self.ip = "111.13.63.2"

    def tearDown(self):
        pass

    #随机生成手机号
    def create_phone(self):
        # 第二位数字
        self.second = [3, 4, 5, 7, 8][random.randint(0, 4)]

        # 第三位数字
        self.third = {
            3: random.randint(0, 9),
            4: [5, 7, 9][random.randint(0, 2)],
            5: [i for i in range(10) if i != 4][random.randint(0, 8)],
            7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
            8: random.randint(0, 9),
        }[self.second]

        # 最后八位数字
        self.suffix = random.randint(9999999, 100000000)

        # 拼接手机号
        return "1{}{}{}".format(self.second,self.third,self.suffix)

    #注册
    #@unittest.skip("no reason")
    def testRegist(self):
        self.phone=self.create_phone()
        self.url = "https://111.13.63.2:9801/api/auth/regist/100000"
        self.json_data = {"phone_num":self.phone,
                     "device_id":"device_123_id",
                     "cmdVersion":"0"
                    }
        self.r = self.s.post(url=self.url, json=self.json_data,verify=False)
        self.assertEqual(self.r.json()["errCode"], '0',msg=self.r.json()["errMsg"])
        if(self.r.json()["errCode"]=="0"):
            try:
                with open("registedPhone.dat","a+") as f:
                    f.write(self.phone)
                    f.write(",")
                    f.write(self.r.json()["sec_code"])
                    f.write("\n")
            finally:
                f.close()
            return self.phone, self.r.json()["sec_code"]
        else:
            print "注册返回的数据：%s" % (self.r.json())
            print u"注册返回的提示信息为：%s" % (self.r.json()["errMsg"])

    #登陆
    #@unittest.skip("no reason")
    def testLogin(self):
        self.phoneNum,self.sec_code = self.testRegist()
        self.url = "https://111.13.63.2:9801/api/auth/login/100000/"
        self.json_data = {"phone_num":self.phoneNum,
                          "device_id":"device_123_id",
                          "sec_code":self.sec_code
                          }
        self.r = self.s.post(url=self.url,json=self.json_data,verify=False)
        self.assertEqual(self.r.json()["errCode"], "0", msg="登陆失败")
        if(self.r.json()["errCode"]=="0"):
            self.access_token=self.r.headers["Set-Cookie"]#[13:205]access_token=access_token=IktsDkUJnN0MxVCXVNkX/AcJYZ/HcOVuCO
            print "------------%s-----------" %(self.r.cookies)
            print "phone=%s,userId=%s,accessToken=%s" %(self.phoneNum,self.sec_code,self.access_token)
            try:
                with open("loginedPhone","w+") as f:
                    f.write("%11s,%4s,%192s" %(self.phoneNum,self.sec_code,self.access_token))
                    f.write("\n")
            finally:
                f.close()
            print "%s" %(self.r.headers)
            return self.r.cookies

        print "登陆返回的cookies：%s" % (self.r.cookies)
        print "登陆返回的数据：%s" % (self.r.json())
        print "登陆返回的头信息为：%s" % (self.r.headers)


    @unittest.skip("no reason")
    def testInit(self):
        self.url = "https://111.13.63.2:9801/api/system/init/66099/100000"
        self.r = self.s.get(url=self.url,verify=False)
        print "认证返回的数据;%s" % (self.r.json())
        self.assertIsNotNone(self.r.json(),msg="初始化失败")

    #@unittest.skip("no reason")
    def testFavorAdd(self):
#{'Transfer-Encoding': 'chunked',
# 'Set-Cookie': 'access_token=IktsDkUJnN0MxVCXVNkX/AcJYZ/HcOVuCOgbsvLTFK1afbvjVgI3B9VM0BT2KSgcblqz2+upCcq24spaMT/wHW1A3t/A4VRkdrYD+kYpay3GML4ENEN8KhC6YPrYQgHp8x1jOy6rQ3PqoJN4qK7KlSYtlrPfN2xMplNft3f2X9enDCv8rw1bfxYc9BzMldML; expires=Sat, 20-Jul-19 09:34:56 GMT; path=/api/,
# phone_num=14569717161; expires=Sat, 20-Jul-19 09:34:56 GMT; path=/api/,
# user_id=294881; expires=Sat, 20-Jul-19 09:34:56 GMT; path=/api/,
# user_lvl=3; expires=Sat, 20-Jul-19 09:34:56 GMT; path=/api/,
# access_token=IktsDkUJnN0MxVCXVNkX/AcJYZ/HcOVuCOgbsvLTFK1afbvjVgI3B9VM0BT2KSgcblqz2+upCcq24spaMT/wHW1A3t/A4VRkdrYD+kYpay3GML4ENEN8KhC6YPrYQgHp8x1jOy6rQ3PqoJN4qK7KlSYtlrPfN2xMplNft3f2X9enDCv8rw1bfxYc9BzMldML;phone_num=14569717161;user_id=294881;user_lvl=3; expires=Sat, 20-Jul-19 09:34:56 GMT; path=/api/',
# 'user_lvl': '3', 'Server': 'nginx/1.14.0', 'Connection': 'keep-alive',
# 'Date': 'Wed, 25 Jul 2018 09:39:44 GMT', 'Content-Type': 'application/json; charset=utf-8',
# 'sign_token': 'IktsDkUJnN0MxVCXVNkX/AcJYZ/HcOVuCOgbsvLTFK1afbvjVgI3B9VM0BT2KSgc3CT6rEt0Dwcz6Mnilw47OG1A3t/A4VRkdrYD+kYpay2oB5a3WLzenl6bQW4NvSieVsLmBH4ElKgpArWiqSvpAjFJQnQvMhY02wR1saNgotY='}

#phone=13146666525,secCode=0914,accessToken=IktsDkUJnN0MxVCXVNkX/AcJYZ/HcOVuCOgbsvLTFK1afbvjVgI3B9VM0BT2KSgcXChkzPxLRDEfYIJa8WFkYN9tf7o2BlkcEjeIx7rtchpbzzFV3K0YbHx15liH5Zpq8x1jOy6rQ3PqoJN4qK7KlZ+Yckvx0OJ23/cRUJ+6U52nDCv8rw1bfxYc9BzMldML
        self.url = self.url_home + "/api/system/favor/add/100000"
        self.json_data = {"group":"\xE8\x87\xAA\xE9\x80\x89",
                          "favors":"2:3232"
                          }
        self.jar = requests.cookies.RequestsCookieJar()
        self.jar.set('phone_num', '14569717161', domain=self.ip, path='/api/')
        self.jar.set('user_id', '294881', domain=self.ip, path='/api/')
        self.jar.set('access_token', 'IktsDkUJnN0MxVCXVNkX/AcJYZ/HcOVuCOgbsvLTFK1afbvjVgI3B9VM0BT2KSgcblqz2+upCcq24spaMT/wHW1A3t/A4VRkdrYD+kYpay3GML4ENEN8KhC6YPrYQgHp8x1jOy6rQ3PqoJN4qK7KlSYtlrPfN2xMplNft3f2X9enDCv8rw1bfxYc9BzMldML', domain=self.ip, path='/api/')
        self.cookies = self.testLogin()
        self.r = self.s.post(url=self.url,json=self.json_data,cookies=self.cookies)
        print "%s" %(self.r.cookies)
        print "---%s" %(self.r.text)


if __name__ == "__main__":
    unittest.main()
