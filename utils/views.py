import datetime
import decimal
import hashlib
import os
import urllib.parse
from functools import wraps

import requests
import json
import random
import hprose
import time
from random import choice

from alipay import AliPay

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from kuaishou_admin.models import Client, Project, Order
# 支付宝支付
from django.http import JsonResponse

from wechatpy import WeChatPay

from utils.tornado_websocket.websocket_test import redisconn


def Create_alipay_order():
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, "utils/app_private_key.pem"),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, "utils/alipay_public_key.pem"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False  配合沙箱模式使用
    )
    return alipay


# 微信支付配置信息
"""
zhouzhou

"""


def Create_wechatpay_order():
    wechatpay = WeChatPay(
        appid="123456",
        api_key='fafafafdsffsdafxzcsadsadqd',
        mch_id='3214324343',
        mch_cert=os.getcwd() + "/pay/conf/apiclient_cert.pem",
        mch_key=os.getcwd() + "/pay/conf/apiclient_key.pem",
    )
    return wechatpay


# 48小时候自动修改状态
"""
xialing
"""

def expired_message():
    try:
        orders = Order.objects.filter(status=1).all()

        now_time = time.time()
        for order in orders:
            c_time = str(order.create_date)
            new_time = c_time.split('.')[0]
            timeArray = time.strptime(new_time, "%Y-%m-%d %H:%M:%S")
            # 转换成时间戳
            timestamp = time.mktime(timeArray)
            if now_time - 86400 > timestamp:
                order.status = 2
                order.save()
    except Exception as e:
        return



"""
xialing and zhouzhou
"""


# 支付优惠
def amount2integral(user, amount):
    r = datetime.datetime.now().strftime('%Y-%m') + ":" + str(user.id)
    if amount >= 30 and (not redisconn.exists(r)):
        integral = int(amount * 100 * 2)
        msg = "每月首充另赠送%s积分" % (integral - int(amount * 100))

    else:
        bl = {10: 1000, 20: 2000, 30: 3500, 50: 6000, 100: 13000, 200: 30000, 300: 50000, 500: 100000}
        qj = (10, 20, 30, 50, 100, 200, 300, 500, 999999999999)
        for i in range(0, len(qj)):
            if amount >= qj[i] and amount < qj[i + 1]:
                integral = bl[qj[i]] + (amount - qj[i]) * 100
                break
        if amount >= 30:
            msg = "另赠送%s积分" % (integral - int(amount * 100))
        else:
            msg = "无优惠"

    showintegral = int(amount * 100)

    return integral, showintegral, msg


# webocke创建时间
def socket_create_order_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 处理用户id
def handle_user_id(user_id):
    hs_user_id = int(user_id) - 1000
    if hs_user_id < 0:
        return JsonResponse({"msg": "用户id错误"})
    return hs_user_id


# 判断条件
'''

xialing and zhouzhou

'''


def conditions(client, need_gold, ):
    need_gold = decimal.Decimal(need_gold)

    client_now_gold = client.gold
    consume_gold = client.consume_gold
    if client_now_gold < need_gold:
        #
        return False

    if client_now_gold >= need_gold:
        client_now_gold -= need_gold
        if client_now_gold < 0:
            # return JsonResponse(data={'status': 5005, 'msg': '积分不足'})
            return False
        consume_gold += need_gold
        client.gold = client_now_gold
        client.consume_gold = consume_gold
        client.save()
    return True


'''
xialing

'''


def check_token(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        data = json.loads(request.body.decode())
        token = data.get("token")
        if not token:
            return HttpResponseRedirect("http://yuweining.cn/t/Html5/404html/")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


'''
xialing

'''


# 检测登录状态
def login_admin_required_json(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return JsonResponse(data={"msg": "用户未登录"})
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


'''


'''


# 生成订单编号
def createOrdernumber(user_id, project_id):
    _date = datetime.datetime.now()
    ordernumber_1 = datetime.datetime.strftime(_date, '%Y%m%d%H%M%S')
    f = datetime.datetime.strftime(_date, '%f')
    ordernumber_2 = ""
    ordernumber_2 += random.choice("123456789")
    # ordernumber_2 += "0" * (3 - len(str(h_user_id))) + str(h_user_id)[0:3]
    ordernumber_2 += "0" * (3 - len(str(project_id))) + str(project_id)[0:3]

    ordernumber_2 += "0" * (3 - len(f)) + f[0:3]
    #     zj = project.gold *count
    ordernumber_2 += "".join([random.choice("0123456789") for j in range(0, 2)])
    return "%s%s" % (ordernumber_1, ordernumber_2)


# 无水印下载
class gifshow_base():
    def __init__(self, version=None):
        self.host = None

        self.hosts = ["api.gifshow.com",
                      "api.ksapisrv.com", ]
        self.proxy = None
        self.versions = {
            "4.46.1.1739": ("4.46", "4.46.1.1739", "3c2cd3f3", "382700b563f4"),
            "4.47.0.1852": ("4.47", "4.47.0.1852", "3c2cd3f3", "382700b563f4"),
            "4.43.0.1228": ("4.43", "4.43.0.1228", "3c2cd3f3", "382700b563f4"),
            "4.48.0.1930": ("4.48", "4.48.0.1930", "3c2cd3f3", "382700b563f4"),
            "4.50.0.2271": ("4.50", "4.50.0.2271", "3c2cd3f3", "382700b563f4"),
            "4.53.3.3098": ("4.53", "4.53.3.3098", "3c2cd3f3", "382700b563f4"),
            "5.2.0.4649": ("5.2", "5.2.0.4649", "3c2cd3f3", "382700b563f4"),
            "5.5.1.5704": ("5.5", "5.5.1.5704", "3c2cd3f3", "382700b563f4"),
        }
        self.headers = {
            "Connection": "Keep-Alive",
            "Accept-Language": "zh-cn",
            "User-Agent": "kwai-android",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip",
        }
        self.method = "POST"
        self.defaultparams = (
            "salt", "ud", "token", 'app', 'appver', 'c', 'client_key', 'country_code', 'did', 'language', 'lat', 'lon',
            'mod', 'net', 'oc', 'os', 'sys', 'ver')
        self.params = dict()

        self.urlparams = ['app', 'appver', 'c', 'country_code', 'did', 'language', 'lat', 'lon', 'mod', 'net', 'oc',
                          'sys', 'ud', 'ver']
        self.postparams = ['client_key', 'token', 'os']

        self.timeout = 10

        if version == None:
            self.version = self.versions["5.5.1.5704"]
        else:
            self.version = self.versions[version]

        self.token_client_salt = None

    def setDefaultValue_ver(self):
        return self.version[0]

    def setDefaultValue_appver(self):
        return self.version[1]

    def setDefaultValue_client_key(self):
        return self.version[2]

    def setDefaultValue_salt(self):
        return self.version[3]

    def setDefaultValue_ud(self):
        return "0"

    def setDefaultValue_token(self, ):
        return ""

    def setDefaultValue_app(self):
        return "0"

    def setDefaultValue_c(self):
        return "GENERIC"

    def setDefaultValue_country_code(self):
        return "CN"

    def setDefaultValue_did(self):
        return "ANDROID_" + hashlib.md5(str(self.params['ud']).encode()).hexdigest()[0:16].upper()

    def setDefaultValue_language(self):
        return "zh-cn"

    def setDefaultValue_lat(self):
        return "0"

    def setDefaultValue_lon(self):
        return "0"

    def setDefaultValue_mod(self):
        return "ONEPLUS(A0001)"

    def setDefaultValue_net(self):
        return "WIFI"

    def setDefaultValue_oc(self):
        return "GENERIC"

    def setDefaultValue_os(self):
        return "android"

    def setDefaultValue_sys(self):
        return "ANDROID_4.4.2"

    def setDefaultValues(self):
        for name in self.defaultparams:
            if not name in self.params.keys():
                value = getattr(self, "setDefaultValue_" + name)()
                self.params[name] = value

    def clear(self):
        self.params.clear()

    def gethost(self):
        if self.host != None:
            return self.host
        else:
            return random.choice(self.hosts)

    def getsign(self):
        param = []
        param.extend(self.urlparams)
        param.extend(self.postparams)
        param2 = []

        for name in param:
            if name != "sig":
                param2.append(name + "=" + self.params[name])

        param2 = "".join(sorted(param2)) + self.params['salt']
        md5 = hashlib.md5(param2.encode()).hexdigest()
        self.sig = md5

    def geturlparam(self):
        urlparams = self.urlparams
        urlparam = {}
        for name in urlparams:
            value = self.params[name]
            urlparam[name] = value
        return urllib.parse.urlencode(urlparam)

    def getpostparam(self):
        postparams = self.postparams
        # random.shuffle(urlparams)
        postparam = {}
        for name in postparams:
            value = self.params[name]
            postparam[name] = value
        return urllib.parse.urlencode(postparam) + "&sig=" + self.sig + "&"

    def seturl(self, url):
        self.url = url
        return self

    def setmethod(self, method):
        self.method = method
        return self

    def addurlparam(self, **kargs):
        for n, v in kargs.items():
            self.params[n] = str(v)
            if not n in self.urlparams:
                self.urlparams.append(n)
        return self

    def addpostparam(self, **kargs):
        for n, v in kargs.items():
            if n == "token":
                self.settoken(v)
            else:
                self.params[n] = str(v)

            if not n in self.postparams:
                self.postparams.append(n)
        return self

    def send(self):

        self.setDefaultValues()
        self.getsign()
        if self.proxy == None:
            proxies = None
        else:
            proxies = {
                "http": self.proxy,
                "https": self.proxy,
            }
        url = 'http://' + self.gethost() + '/' + self.url + "?" + self.geturlparam()
        if self.token_client_salt:
            self.params["__NStokensig"] = hashlib.sha256((self.sig + self.token_client_salt).encode()).hexdigest()
            self.postparams.append("__NStokensig")
        post = self.getpostparam()

        r = requests.post(url, data=post, headers=self.headers, proxies=proxies, timeout=self.timeout)
        return r.content

    def send_text(self):
        return self.send().decode()

    def send_json(self):
        return json.loads(self.send_text())

    def settoken(self, token):
        try:
            self.params['ud'] = token.split("-")[1]
            self.params["token"] = token
        except:
            self.params['ud'] = "0"
            self.params["token"] = ""
        return self

    def settoken_client_salt(self, token_client_salt):
        self.token_client_salt = token_client_salt
        return self

    def sethost(self, host):
        self.host = host
        return self

    def setproxy(self, proxy):
        self.proxy = proxy
        return self


class gifshow(gifshow_base):
    def follow(self, touid, page_ref=None, **kargs):

        self.seturl("rest/n/relation/follow")
        # ks://addfriend 1
        # ks://users/following/6816038 3
        if page_ref == None:
            pageref = random.randint(1, 22)
        else:
            pageref = page_ref
        self.addpostparam(page_ref=pageref, touid=touid, act_ref="", referer="", ftype=1)
        self.addpostparam(**kargs)
        result = self.send_json()
        return result

    def unfollow(self, touid, page_ref=None, **kargs):
        self.seturl("rest/n/relation/follow")
        # ks://addfriend 1
        # ks://users/following/6816038 3
        if page_ref == None:
            pageref = random.randint(1, 22)
        else:
            pageref = page_ref
        self.addpostparam(page_ref=pageref, touid=touid, act_ref="", referer="", ftype=2)
        self.addpostparam(**kargs)
        result = self.send_json()
        return result

    def rest_n_relation_fol(self, touid, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/relation/fol")
        self.addpostparam(touid=touid, ftype=1)
        return self.send_json()

    def rest_n_feed_profile(self, user_id, count=30, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/feed/profile")
        self.addpostparam(count=count, pcursor="", user_id=user_id, referer="", mtype=2, lang="zh")
        return self.send_json()

    def rest_n_user_search(self, user_name, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/user/search")
        self.addpostparam(user_name=user_name, page=1)
        return self.send_json()

    def register_email(self, email, userName, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/user/register/email")
        self.addurlparam(ud="41315")
        self.addpostparam(gender="U", userName=userName, password="", email=email)
        return self.send_json()

    def user_profile_v2(self, user, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/user/profile/v2")
        self.addpostparam(user=user)
        return self.send_json()

    def live_startPlay(self, author, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/live/startPlay/v2")
        self.addpostparam(author=author, exp_tag="")
        return self.send_json()

    def live_stopPlay(self, liveStreamId, **kargs):
        self.addpostparam(**kargs)
        self.sethost("live.gifshow.com")
        self.seturl("rest/n/live/stopPlay")
        self.addpostparam(liveStreamId=liveStreamId)
        return self.send_json()

    def live_like(self, liveStreamId, **kargs):
        self.addpostparam(**kargs)
        self.sethost("live.gifshow.com")
        self.seturl("rest/n/live/like")
        self.addpostparam(liveStreamId=liveStreamId, count=1)
        return self.send_json()

    def live_comment(self, liveStreamId, content, copy=False, **kargs):
        self.addpostparam(**kargs)
        self.sethost("live.gifshow.com")
        self.seturl("rest/n/live/comment")
        copy = "true" if copy else "false"
        self.addpostparam(content=content, liveStreamId=liveStreamId, copy=copy)
        return self.send_json()

    def photo_comment_list(self, user_id, photo_id, pcursor="", count=20, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/photo/comment/list")
        self.addpostparam(order="desc", pcursor=pcursor, ctype=1, user_id=user_id, photo_id=photo_id, count=count)
        return self.send_json()

    def photo_comment_add(self, user_id, photo_id, content, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/photo/comment/add")
        referer = "ks://photo/%s/%s/3/1_a/1541574338726342658_h80#addcomment" % (user_id, photo_id)
        self.addpostparam(content=content, reply_to="", user_id=user_id, referer=referer, photo_id=photo_id, copy=0)
        return self.send_json()

    def photo_like(self, user_id, photo_id, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/photo/like")
        referer = "ks://photo/%s/%s/3/1_a/1568350775795728384_n80#doublelike" % (user_id, photo_id)
        self.addpostparam(cancel=0, user_id=user_id, referer=referer, photo_id=photo_id)
        return self.send_json()

    def photo_click(self, user_id, photo_id, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/clc/click")
        # userid = random.randint(1,4000000000)
        # s = hashlib.md5(str(userid).encode()).hexdigest()
        # token = "%s4%s-%d"%(s[0:12],s[13:32],userid)
        # self.settoken(token)
        data = "%s_%s_p5" % (user_id, photo_id)
        self.addpostparam(downs="", data=data)

        return self.send_json()

    def photo_info(self, photoIds, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/photo/info")
        if type(photoIds) == list:
            photoIds = [str(i) for i in photoIds]
            photoIds = ",".join(photoIds)
        self.addpostparam(photoIds=photoIds)
        return self.send_json()

    def photo_likeshow2(self, photo_id, pcursor="", **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/photo/likeshow2")
        self.addpostparam(photo_id=photo_id, pcursor=pcursor)
        return self.send_json()

    def feed_list(self, count=20, page=1, type=7, pcursor="", **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/feed/list")
        self.addpostparam(count=count, page=page, pcursor=pcursor, pv="false", type=type)
        return self.send_json()

    def message_dialog(self, count=20, page=1, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/message/dialog")
        self.addpostparam(count=count, page=page)
        return self.send_json()

    def authStatus(self, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/live/authStatus")
        return self.send_json()

    def checkupdate(self, **kargs):
        self.addpostparam(**kargs)
        self.seturl("rest/n/system/checkupdate")
        self.addpostparam(mark=self.setDefaultValue_did(),
                          data="check_upgrade&SDK24&%s&samsung(SM-G9350)" % self.version[1], sdk="SDK24")
        return self.send_json()


def GetMiddleStr(content, startStr, endStr):
    startIndex = content.find(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
    endIndex = content.find(endStr, startIndex)
    return content[startIndex:endIndex]


class CheckError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class action_gifshow_like():
    def check(self, *args, **kwarg):
        return

    def format(self, photo, *args, **kwarg):
        userid = int(GetMiddleStr(photo + "&", "userId=", "&"))
        photoid = int(GetMiddleStr(photo + "&", "photoId=", "&"))
        if userid < 1 and photoid < 1:
            CheckError(-1, "链接异常")
        return {"userid": userid, "photoid": photoid}

    def getcount(self, userid, photoid, *args, **kwarg):
        userinfo = gifshow().rest_n_feed_profile(userid, count=100)

        def getphotoidcount(feeds, photoid):
            for feed in feeds:
                if feed['photo_id'] == photoid:
                    return feed['like_count']

        return getphotoidcount(userinfo['feeds'], photoid)

    def exe(self, userid, photoid, token, proxy, *args, **kwarg):

        try:
            result = gifshow().settoken(token[1]).setproxy(proxy).photo_like(userid, photoid)
        except Exception as e:
            result = None
            pass

        return result

    def show(self, userid, photoid, *args, **kwarg):
        return '''喜欢<a href="http://www.kuaishou.com/i/photo/lwx?userId=%s&photoId=%s" target="_black">%s-%s</a>''' % (
            userid, photoid, userid, photoid)


class action_gifshow_photocomment():
    # http://www.gifshow.com/i/photo/lwx?userId=86752451&photoId=943312486&cc=share_copylink&fid=6816038&et=1_a%2F1541574338726342658_h80


    def check(self, userid, *args, **kwarg):
        self.userinfo = gifshow().rest_n_feed_profile(userid)
        if self.userinfo['comment_deny'] == '1':
            raise CheckError(-1, "禁止评论！")

    def format(self, photo, content, *args, **kwarg):
        userid = int(GetMiddleStr(photo + "&", "userId=", "&"))
        photoid = int(GetMiddleStr(photo + "&", "photoId=", "&"))
        if userid < 1 and photoid < 1:
            CheckError(-1, "链接异常")
        _content = content.split("\r\n")
        content = []
        for v in _content:
            v = v.strip()
            if len(v) != 0:
                content.append(v)
        return {"userid": userid, "photoid": photoid, "contents": content}

    def getcount(self, userid, photoid, *args, **kwarg):
        info = gifshow().photo_comment_list(userid, photoid)
        count = info['commentCount']
        return count

    def exe(self, userid, photoid, contents, token, proxy, *args, **kwarg):
        content = choice(contents)
        try:
            result = gifshow().settoken(token[1]).setproxy(proxy).photo_comment_add(userid, photoid, content)
            # if token[0] > 0:
            #     client =  hprose.HproseHttpClient("http://120.27.35.91/api")
            #     client.followresult(userid,token[0],result)
        except Exception as e:
            result = None
            pass

        return result

    def show(self, userid, photoid, *args, **kwarg):
        return '''评论<a href="http://www.kuaishou.com/i/photo/lwx?userId=%s&photoId=%s" target="_black">%s-%s</a>''' % (
            userid, photoid, userid, photoid)


class action_gifshow_click():
    def check(self, userid, photoid, *args, **kwarg):
        self.photo_info(photoid)

    def format(self, photo, *args, **kwarg):
        userid = int(GetMiddleStr(photo + "&", "userId=", "&"))
        photoid = int(GetMiddleStr(photo + "&", "photoId=", "&"))
        if userid < 1 and photoid < 1:
            CheckError(-1, "链接异常")
        return {"userid": userid, "photoid": photoid}

    def getcount(self, userid, photoid, *args, **kwarg):
        photoinfo = self.photo_info(photoid)
        return photoinfo["view_count"]

    def photo_info(self, photoid):
        result = gifshow().sethost("180.186.38.200").photo_info(photoid)
        if result["result"] != 1:
            if "error_msg" in result.keys():
                msg = result["error_msg"]
            else:
                msg = "异常错误"
            raise CheckError(result["result"], msg)
        return result["photos"][0]

    def exe(self, userid, photoid, *args, **kwarg):

        try:
            g = gifshow()
            g.timeout = (5, 2)
            result = g.photo_click(userid, photoid)
        except Exception as e:
            result = None
            pass

        return result

    def show(self, userid, photoid, *args, **kwarg):
        return '''<a href="http://www.kuaishou.com/i/photo/lwx?userId=%s&photoId=%s" target="_black">%s-%s</a>''' % (
            userid, photoid, userid, photoid)


class action_gifshow_fans():
    userinfo = None
    t = 0

    def setdata(self, *args, **kwarg):
        pass

    def check(self, userid, *args, **kwarg):
        self.userinfo = gifshow().rest_n_feed_profile(userid)
        if self.userinfo['privacy_user'] == '1':
            raise CheckError(-1, "隐私用户！")

    def format(self, userid, *args, **kwarg):
        userid = int(userid)
        userids = [user["user_id"] for user in
                   gifshow().settoken("a5eaa088fa464ca3a66184cd869671fb-257905927").rest_n_user_search(userid)["users"]]
        if not userid in userids:
            raise CheckError(-1, "用户不存在！")
        return {"userid": userid}

    def getcount(self, userid, *args, **kwarg):
        if self.userinfo == None or (time.time() - self.t) > 1:
            self.userinfo = gifshow().rest_n_feed_profile(userid)
        count = self.userinfo['owner_count']['fan']
        self.userinfo = None
        return count

    def exe(self, userid, token, proxy, *args, **kwarg):
        try:
            result = gifshow().settoken(token[1]).setproxy(proxy).follow(userid)
            if token[0] > 0:
                client = hprose.HproseHttpClient("http://120.27.35.91/api")
                client.followresult(userid, token[0], result)
        except Exception as e:
            result = None
            pass
        return result

    def show(self, userid, *args, **kwarg):
        return str(userid)


def getproxys(api, count):
    # if not re.match('^(http://){0,1}[A-Za-z0-9][A-Za-z0-9\-\.]+[A-Za-z0-9]\.[A-Za-z]{2,}[\43-\176]*$',api):
    #     print("代理API不规范")
    #     return []

    i = api.find("%count%")
    if i > 0:
        api = api[:i] + str(count) + api[i + 7:]
    content = requests.get(api, timeout=5).text
    content = content.split('\r\n')
    ips = []
    for ip in content:
        ip = ip.strip()
        if len(ip) > 0:
            ips.append(ip)
    ips = list(set(ips))
    return ips
