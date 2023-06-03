# -*- coding: utf-8 -*-
# @date：2023/5/25 9:46
# @Author：LiuYiJie
# @file： 00_commen
import random
from urllib.parse import urljoin

import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pandas as pd
from selenium.webdriver.common.keys import Keys
from lxml import etree
from urllib.parse import quote
from UserAgent import fake_useragent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup


class TeacherEmail:
    def __init__(self, error_email: list = None, school_name: str = None):
        self.email_names = list()
        self.remove_lists = pd.read_csv(r'F:\高校花名册\school_code\去除名字.csv', dtype=str)['name'].values.tolist()
        self.error_email = error_email
        self.school_name = school_name

    def get_email_auto(self,driver, link):
        driver.get(link)
        time.sleep(0.5)
        response = driver.page_source
        email_num = re.findall('([a-zA-Z0-9_.+-]+[@#][a-zA-Z0-9-.]+\.[a-zA-Z0-9-.]+)', response) or re.findall(
            '([a-zA-Z0-9_.+-]+\s@\s[a-zA-Z0-9-.]+\.[a-zA-Z0-9-.]+)', response)
        if email_num:
            email = ''
            for i_num in email_num:
                if 'Email' in i_num:
                    i_num = i_num.split('Email')[1]
                elif 'E-Mail' in i_num:
                    i_num = i_num.split('E-Mail')[1]
                if i_num not in self.error_email:
                    if i_num.endswith('com') or i_num.endswith('cn') or i_num.endswith('net'):
                        return i_num
                else:
                    email = ''
            return email
        else:
            return ''


    # 搜索
    def open_chrome(self,school_message):
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        option.add_argument("--incognito")
        # 不加载图片
        option.add_argument('blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(options=option)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                               {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})
        driver.maximize_window()
        driver.get('https://www.baidu.com')

        # driver.implicitly_wait(5)
        time.sleep(4)

        school_url_lists = school_message.get('school_urls')
        for i_collage in school_url_lists:
            link = i_collage.get('link')
            driver.get(link)
            # input('确认')
            # input('确认')
            time.sleep(2)
            res = driver.page_source
            if 'nth' in i_collage:
                self.get_teacher_xpath(driver, res, school_message, i_collage)
            else:
                self.get_teacher_details(driver, res, school_message, i_collage)


    # 设置随机user-agent
    def useragent(self):
        agent = random.choice(fake_useragent())
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "User-Agent": agent,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',

        }
        return headers

    # 获取教师姓名以及详情页地址
    def get_teacher_details(self,driver, response, school_message, i_collage):
        # 解析页面
        print('当前地址', i_collage.get('link'))
        res = self.parse_html(response)
        all_teachers = []
        # 提取第一页教师
        soup = BeautifulSoup(response, 'html.parser')

        if i_collage.get("docu"):
            aaaa = soup.select(f'.{i_collage.get("docu").strip().replace(" ", ".")}') or soup.select(
                f'#{i_collage.get("docu").strip().replace(" ", ".")}')
            aaaa = aaaa[0].descendants
            #        获取所有邮箱
            a_list = soup.select(f'.{i_collage.get("docu").strip().replace(" ", ".")}') or soup.select(
                f'#{i_collage.get("docu").strip().replace(" ", ".")}')
            a_list = a_list[0].find_all('a')
        else:
            aaaa = soup.descendants
            a_list = soup.find_all('a')

        out = []
        all_teachers_email = []
        for one in a_list:
            name = one.text.replace(' ', '').replace('​', '').replace('-', '').replace('\t', '').strip('\n') \
                   or one.get('title','').replace(' ','').replace('​', '').replace('\t', '').replace('-', '')
            name = re.sub(r'\d+年', '', name)
            name = re.sub(r'\d+班', '', name)
            name = re.sub(r'\d+月', '', name)
            name = re.sub(r'\d+', '', name)
            for s in ['院士', "博导", '硕导', '副教授', '教授', '讲师', '副研究员', '副主任医师', '主任医师', '主治医师', '医师','高级工程师', '高级实验师','研究员', '助理', '硕士', '博士后', '博士', '先生',]:
                name = name.replace(s, '\n').replace('*', '\n').replace('>', '').replace('/', '').replace('▪', '').replace('环境学院','')
            if not name or len(name) <= 1:
                continue
            hz_num = 0
            name = name.strip('·').strip(' ')
            for str1 in name:
                if u'\u4e00' < str1 < u'\u9fff' or str1 == '一':
                    hz_num += 1
            if hz_num == 2:
                while True:
                    for index, str1 in enumerate(name[1:]):
                        if u'\u4e00' < str1 < u'\u9fff' or str1 == '一':
                            break
                        name = name.replace(name[1], '', 1)
                    break
            if hz_num == 0:
                continue
            if name[1] == ' ':
                name = name.replace(' ', '', 1)
            names = name.replace('(', '\n').replace('（', '\n').replace(')', '\n').replace('）', '\n').replace(':', '\n').replace('：', '\n').replace(',','\n').replace('，', '\n').replace(' ', '\n').split('\n')
            for name in names:
                if not name:
                    continue
                # for s in ['院士', "博导", '硕导', '副教授', '教授', '讲师', '副研究员', '研究员', '助理', '硕士', '博士后', '博士', ")", "(", "（", "）"]:
                #     name = name.replace(s, '').replace(' ', '')
                if 1 < len(name) < 4 and (name not in self.remove_lists) and (name not in self.email_names) and u'\u4e00' < name[0] < u'\u9fff':
                    href = one.get('href')
                    if href:
                        url = urljoin(i_collage.get('link'), one.get('href').replace('\t', '').replace(' ', ''))

                        teacher_email = ''
                        teacher_email = self.get_teacher_em(url)
                        # teacher_email = get_email_auto(driver, url)

                        # url = url.split('id=')[1]
                        # teacher_email = get_teschers(url)
                        # 将获取过邮箱的教师一个列表
                        self.email_names.append(name)
                        self.email_names.append(name.replace(' ', '').replace('　', ''))
                        print(name, teacher_email)
                        all_teachers_email.append(
                            {'姓名': name.replace(' ', '').replace('　', ''), '机构': school_message.get('name').strip(),
                             'email': teacher_email, 'link': url.replace('\n', '')})
        all_teachers_email.append({'姓名': '一个区分名字', '机构': "一个区分名字学院", 'email': "一个区分名字邮箱1", 'link': ''})
        self.save_list(all_teachers_email, '官网别名表.csv', ['姓名', '机构', 'email', 'link'])

        for str1 in aaaa:
            if len(str(str1).split('>')) > 2:
                continue
            name = []
            namet = str1.text
            namet = namet.replace('(', '（').split('（')[0]
            for str2 in namet:
                # 名字中带有一字的
                if str2 == '一':
                    name.append(str2)
                elif len(namet) == 1 and namet in ['女', '男']:
                    continue
                # elif u'\u4e00' < str2 < u'\u9fff' and str2 not in ['女', '男']: 以前写的
                elif u'\u4e00' < str2 < u'\u9fff':
                    name.append(str2)
                else:
                    name.append(' ')
            Name = ''.join(name)
            for s in ['硕导', '副教授', '教授', '讲师', '副研究员', '副主任医师', '主任医师', '主治医师','医师','高级工程师', '高级实验师','研究员', '助理', '硕士', '博士后', '博士','院士', '工程师', '先生']:
                Name = Name.replace(s, '')
            Name = Name.split(' ')
            out += Name
        out = [str2 for str2 in out if str2 != '']
        index = 0
        all_name = []
        for str3 in out:
            if index < len(out) - 1:
                start = out[index]
                end = out[index + 1]
                index += 1
                if len(start) == 1 and len(end) == 1:
                    all_name.append(start + end)
                    index += 1
                elif len(start) > 1 and len(start) < 4:
                    all_name.append(start)

        if out and len(out[-1]) != 1:
            all_name.append(out[-1])
        for teacher_name in all_name:
            if len(teacher_name) < 4 and teacher_name not in self.remove_lists and teacher_name not in self.email_names:
                all_teachers.append({'姓名': teacher_name.strip(), '机构': school_message.get('name').strip(), 'email': '', 'link': ''})
        all_teachers.append({'姓名': '一个区分名字', '机构': "一个区分名字学院", 'email': "一个区分名字邮箱2", 'link': ''})
        self.save_list(all_teachers, '官网别名表.csv', ['姓名', '机构', 'email', 'link'])

        # # 判断是否有下一页
        # driver.get(i_collage.get('link'))
        # time.sleep(1)
        next_page = res.xpath(
            "//a[contains(@title, '下页')] | //a[contains(@title, '下一页')] | //span[contains(@title, '下页')] | //span[contains(@title, '下一页')]") or res.xpath(
            "//a[contains(text(), '下页')] | //a[contains(text(), '下一页')] | //span[contains(text(), '下页')] | //span[contains(text(), '下一页')]")
        if next_page:
            try:
                # # 拿到下一页的名称
                next_link = res.xpath(
                    "//a[contains(@title, '下页')]/@title | //a[contains(@title, '下一页')]/@title | //span[contains(@title, '下页')]/@title | //span[contains(@title, '下一页')]/@title") or res.xpath(
                    "//a[contains(text(), '下页')]/text() | //a[contains(text(), '下一页')]/text() | //span[contains(text(), '下页')]/text() | //span[contains(text(), '下一页')]/text()")
                # next_url = res.xpath(
                #     "//a[contains(text(), '下页')]/@href | //a[contains(text(), '下一页')]/@href | //span[contains(text(), '下页')]/../@href | //span[contains(text(), '下一页')]/../@href")[
                #     0]
                next_link = next_link[0]

                driver.find_element(by=By.LINK_TEXT, value=next_link).click()

                url = driver.current_url
                i_collage['link'] = url
                time.sleep(random.randint(2, 4))
                resp = driver.page_source
                if resp == response:
                    return
                self.get_teacher_details(driver, resp, school_message, i_collage)
            except:
                return
        else:
            return

    # 根据xpath获取老师信息
    def get_teacher_xpath(self, driver, response, school_message, i_collage):
        print('当前地址', i_collage.get('link'))
        res = self.parse_html(response)
        all_teachers_email = []
        lists = res.xpath(i_collage.get('zth'))  # /td[1]/table/tbody/tr[1]/td[2]/text()')
        url = ''
        for one in lists:
            str1 = i_collage.get('nth')
            name = one.xpath(str1)[0] if one.xpath(str1) else ''
            if name and (name not in self.remove_lists) and (name not in self.email_names):
                name = name.replace('姓名:', '').replace('姓名：', '').replace('\n', '').split('：')[0]
                str2 = i_collage.get('eth')
                link111 = one.xpath(str2)
                link111 = ''.join(link111)
                if '@' in link111 or 'AT' in link111 or 'at' in link111:
                    link111 = link111.replace('[at]', '@').replace(' AT ', '@').replace(' at ', '@').replace('AT','@').replace('at', '@')
                    teacher_email = self.get_email(link111)
                    # teacher_email = link111.replace('邮箱：', '')
                else:
                    url = urljoin(i_collage.get('link'), link111)
                    teacher_email = ''
                    teacher_email = self.get_teacher_em(url)
                    # teacher_email = link111.replace('Email: ','').replace('\n', '').replace(' ', '')

                if u'\u4e00' < name[0] < u'\u9fff':
                    name = name.replace('　', '').replace('  ', '').replace(' ', '')
                print(name, teacher_email)
                # 将获取过邮箱的教师一个列表
                self.email_names.append(name)
                self.email_names.append(name.replace(' ', '').replace('　', ''))
                all_teachers_email.append(
                    {'姓名': name.strip(' ').strip('　'), '机构': school_message.get('name').strip(),
                     'email': teacher_email, 'link': url.replace('\n', '')})
        all_teachers_email.append({'姓名': '一个区分名字', '机构': "一个区分名字学院", 'email': "一个区分名字邮箱1", 'link': ''})
        self.save_list(all_teachers_email, '官网别名表.csv', ['姓名', '机构', 'email', 'link'])

        # # 判断是否有下一页
        # driver.get(i_collage.get('link'))
        # time.sleep(1)
        next_page = res.xpath(
            "//a[contains(@title, '下页')] | //a[contains(@title, '下一页')] | //span[contains(@title, '下页')] | //span[contains(@title, '下一页')]") or res.xpath(
            "//a[contains(text(), '下页')] | //a[contains(text(), '下一页')] | //span[contains(text(), '下页')] | //span[contains(text(), '下一页')]")
        if next_page:
            try:
                # # 拿到下一页的名称
                next_link = res.xpath(
                    "//a[contains(@title, '下页')]/@title | //a[contains(@title, '下一页')]/@title | //span[contains(@title, '下页')]/@title | //span[contains(@title, '下一页')]/@title") or res.xpath(
                    "//a[contains(text(), '下页')]/text() | //a[contains(text(), '下一页')]/text() | //span[contains(text(), '下页')]/text() | //span[contains(text(), '下一页')]/text()")
                # next_url = res.xpath(
                #     "//a[contains(text(), '下页')]/@href | //a[contains(text(), '下一页')]/@href | //span[contains(text(), '下页')]/../@href | //span[contains(text(), '下一页')]/../@href")[
                #     0]
                next_link = next_link[0]

                driver.find_element(by=By.LINK_TEXT, value=next_link).click()

                url = driver.current_url
                i_collage['link'] = url
                time.sleep(random.randint(2, 4))
                resp = driver.page_source
                if resp == response:
                    return
                self.get_teacher_xpath(driver, resp, school_message, i_collage)
            except:
                return
        else:
            return

    # 保存到csv文件
    def save_list(self, data, file, name):
        # desk = os.path.join(os.path.expanduser('~'), 'Desktop')
        # 当前文件夹
        file_path = fr'F:\高校花名册\file_in\{self.school_name}\花名册\\' + file
        if os.path.isfile(file_path):
            df = pd.DataFrame(data=data)
            df.to_csv(file_path, encoding="utf-8", mode='a', header=False, index=False)
        else:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df = pd.DataFrame(data=data, columns=name)
            df.to_csv(file_path, encoding="utf-8", index=False)

    # 处理老师的详细信息界面
    def get_teacher_em(self, email_link):
        try:
            import requests.packages.urllib3.util.ssl_
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

            time.sleep(0.5)
            # id = email_link.split('encodeURI')[1].replace('(\'','').replace('\'))', '')
            # email_link = f'http://bsoa.csu.edu.cn/blog/content2?name={quote(id)}'
            response = requests.get(url=email_link, headers=self.useragent(), timeout=3)
            response.encoding = response.apparent_encoding
            email_num = re.findall('([a-zA-Z0-9_.+-]+[@#][a-zA-Z0-9-.]+\.[a-zA-Z0-9-.]+)', response.text) \
                        or re.findall('([a-zA-Z0-9_.+-]+\s@\s[a-zA-Z0-9-.]+\.[a-zA-Z0-9-.]+)', response.text) \
                        or re.findall('([a-zA-Z0-9_.+-]+\[at\][a-zA-Z0-9-.]+\.[a-zA-Z0-9-.]+)', response.text)
            if email_num:
                email = ''
                for i_num in email_num:
                    i_num = i_num.replace('[at]', '@')
                    if 'Email' in i_num:
                        i_num = i_num.split('Email')[1]
                    elif 'E-Mail' in i_num:
                        i_num = i_num.split('E-Mail')[1]
                    if i_num not in self.error_email:
                        if i_num.endswith('com') or i_num.endswith('cn') or i_num.endswith('net'):
                            return i_num
                    else:
                        email = ''
                return email
            elif '_tsites_encrypt_field' in response.text:
                emtext = re.findall('Email : <span _tsites_encrypt_field="_tsites_encrypt_field" id="(.*?)" style="display:none;">(.*?)</span>',response.text)
                if not emtext:
                    emtext = re.findall('邮箱:<span _tsites_encrypt_field="_tsites_encrypt_field" id="(.*?)" style="display:none;">(.*?)</span>', response.text)
                if not emtext:
                    emtext = re.findall('邮箱 : <span _tsites_encrypt_field="_tsites_encrypt_field" id="(.*?)" style="display:none;">(.*?)</span>',response.text)
                if not emtext:
                    emtext = re.findall('邮箱: <span _tsites_encrypt_field="_tsites_encrypt_field" id="(.*?)" style="display:none;">(.*?)</span>',response.text)
                if not emtext:
                    emtext = re.findall('邮箱：<span _tsites_encrypt_field="_tsites_encrypt_field" id="(.*?)" style="display:none;">(.*?)</span>',response.text)
                if not emtext:
                    emtext = re.findall('邮箱 :<span _tsites_encrypt_field="_tsites_encrypt_field" id="(.*?)" style="display:none;">(.*?)</span>',response.text)
                if not emtext:
                    emtext = re.findall('邮件 : <span _tsites_encrypt_field="_tsites_encrypt_field" id="(.*?)" style="display:none;">(.*?)</span>',response.text)
                if not emtext:
                    emtext = re.findall('<span _tsites_encrypt_field="_tsites_encrypt_field" id="(.*?)" style="display:none;">(.*?)</span>',response.text)

                emil = '-------'
                for one1 in emtext:
                    url = f"https://teachers.jlu.edu.cn/system/resource/tsites/tsitesencrypt.jsp?id={one1[0]}&content={one1[1]}&mode=8"
                    headers = {
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Pragma': 'no-cache',
                        'Referer': email_link,
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                    }
                    response = requests.request("GET", url, headers=headers, verify=False).text
                    if '@' not in response:
                        continue
                    emil = re.findall('([a-zA-Z0-9_.+-]+[@#][a-zA-Z0-9-.]+\.[a-zA-Z0-9-.]+)', response)[0]
                return emil
            else:
                return ''
        except Exception as e:
            print(e)

    def get_email(self, text):
        # 处理老师的详细信息界面
        try:
            email_num = re.findall('([a-zA-Z0-9_.+-]+[@#][a-zA-Z0-9-.]+\.[a-zA-Z0-9-.]+)', text)
            if email_num:
                email = ''
                for i_num in email_num:
                    i_num = i_num.replace('[at]', '@')
                    if 'Email' in i_num:
                        i_num = i_num.split('Email')[1]
                    elif 'E-Mail' in i_num:
                        i_num = i_num.split('E-Mail')[1]
                    if i_num not in self.error_email:
                        if i_num.endswith('com') or i_num.endswith('cn') or i_num.endswith('net'):
                            return i_num
                    else:
                        email = ''
                return email
            else:
                return ''
        except:
            return ''

    # 解析页面
    def parse_html(self, res):
        response = etree.HTML(res)
        return response


