#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Storing sites or functions that not working anymore... maybe"""
from bs4 import BeautifulSoup
import requests
import logging
import regex as re


def crawl_xiaoshuang(url='https://xsjs.yhyhd.org/free-ss'):
    print('req xcud...')
    try:
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        data = soup.find('div', attrs={'id': 'ss-body'})
        data = data.text.strip().split('\n\n\n')
        info = {'message': data[0].split('\n')[0], 'name': '小双加速', 'url': url}
        data[0] = data[0].split('\n', maxsplit=1)[-1]
        servers = list()
        for server in data:
            server_data = server.strip().split('\n')
            servers.append(dict())
            servers[-1]['remarks'] = '小双{}'.format(server_data[0]).strip()
            servers[-1]['server'] = server_data[1].split()[1].strip()
            servers[-1]['server_port'] = server_data[1].split()[3].strip()
            servers[-1]['password'] = server_data[2].split()[3].strip()
            servers[-1]['method'] = server_data[2].split()[1].strip()
            servers[-1]['ssr_protocol'] = server_data[3].split()[1].split(':')[1].strip()
            servers[-1]['obfs'] = server_data[3].split()[2].split(':')[1].strip()
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info

# this cannot use for now


def crawl_newpac(url='https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7'):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    ss_list = list()

    for i in soup.find_all('p'):
        if re.match('\<p\>\s*服务器\d+[^:：]*[:：]', str(i)):
            ss_list.append(str(i))

    servers = list()
    for i in ss_list:
        servers.append(dict())
        servers[-1]['string'] = i
        # name
        tmp = re.findall('服务器\d+[^:：]*(?=\s*[:：])', i)
        if tmp:
            servers[-1]['remarks'] = tmp[0]

        # server
        tmp = re.findall('(?<=服务器\s*\d+[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[\w\d\.]+', i)
        if tmp:
            servers[-1]['server'] = tmp[0]

        # server_port
        tmp = re.findall('(?<=端口\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)\d+', i)
        if tmp:
            servers[-1]['server_port'] = tmp[0]

        # password
        tmp = re.findall('(?<=密码\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['password'] = tmp[0]

        # method
        tmp = re.findall('(?<=加密方[式法]\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['method'] = tmp[0]

        # SSR协议
        tmp = re.findall('(?<=SSR协议\s*[^:：]*[:：]\s*[^a-zA-Z_0-9]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['ssr_protocol'] = tmp[0]

        # 混淆
        tmp = re.findall('(?<=混淆\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['obfs'] = tmp[0]
    info = {'message': '', 'name': 'new-pac', 'url': url}
    return servers, info


def crawl_nobey(url='https://raw.githubusercontent.com/NoBey/Shadowsocks-free/master/README.md'):
    def strip_dot(x):
        return
    print('req nobey...')
    servers = list()
    try:
        data = re.split('##+|---+', requests.get(url).text)[2:5:2]
        info = {'message': '', 'name': 'NoBey', 'url': 'https://github.com/NoBey/Shadowsocks-free'}

        for i, server in enumerate(data):
            server = server.split('\n')

            name = server[0].strip()
            (
                ips,
                ports,
                _,
                method,
                password) = list(map(
                    lambda server: list(map(
                        lambda x: x.strip().strip('`').strip(),
                        server.strip('-').strip().split()[1:])),
                    server[1:6]))
            method = method[0]
            password = password[0]

            for j, ip in enumerate(ips):
                for k, port in enumerate(ports):
                    servers.append(dict())
                    servers[-1]['remarks'] = 'NoBey {}-{}-{}'.format(name, j, k)
                    (
                        servers[-1]['server'],
                        servers[-1]['password'],
                        servers[-1]['server_port'],
                        servers[-1]['method']) = (ip, password, port, method)

    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def crawl_5752me(url='https://wget.5752.me/Computer/soft/socks5%E4%BB%A3%E7%90%86/%E5%85%8D%E8%B4%B9ss%E8%B4%A6%E5%8F%B7.html'):
    print('req 5752...')
    servers = list()
    try:
        data = requests.get(url)
        if 'IP地址' in data.content.decode('gb2312'):
            data = data.content.decode('gb2312')
        elif 'IP地址' in data.text:
            data = data.text
        else:
            raise Exception('没找到5752信息：' + url)
        info = {'message': '', 'name': '自得其乐', 'url': 'https://www.5752.me/'}
        data = data.split('<br/>')

        avail_data = list(filter(lambda x: 'IP地址' in x, data))
        if len(avail_data) == 0:
            raise Exception('5752里面资料大概改变形式了' + '\n'.join(data))

        for i, server in enumerate(avail_data):
            servers.append(dict())
            servers[-1]['remarks'] = '自得其乐 {}'.format(i)
            (
                servers[-1]['server'],
                servers[-1]['password'],
                servers[-1]['server_port'],
                servers[-1]['method']) = server.split()[1::2]

    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def crawl_fq123(url='https://raw.githubusercontent.com/fq1234/home/master/README.md'):
    print('req fq123...')
    try:
        data = re.split('\s*\n\s*', requests.get(url).text.split('```')[1].strip())
        servers = [{
            'remarks': 'fq123.tk',
            'server': data[0].split()[1],
            'server_port': data[1].split()[1],
            'password': data[2].split()[1],
            'method': data[3].split()[1],
        }]
        info = {'message': '', 'name': 'fq123', 'url': 'http://fq123.tk/'}
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def crawl_freess_cx(url='https://ss.freess.org', headers=fake_ua):
    print('req fscx...')
    servers = list()
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.find('title').text
        msg = soup.find('section', attrs={'id': 'banner'}).text.strip()

        info = {'message': msg, 'url': url, 'name': str(title)}
        qr = list(map(lambda x: x.find('a').get('href'), soup.find_all('div', attrs={'class': '4u 12u(mobile)'})))
        for i, img_url in enumerate(qr):
            try:
                servers.append(parse(scanNetQR(img_url, headers=headers), ' '.join([title, str(i)])))
            except Exception as e:
                logging.exception(e, stack_info=False)
                print('IMG_URL FOR freess.cx:', img_url)
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def crawl_yitianjian(url='https://free.yitianjianss.com', headers=fake_ua):
    print('req yitianjian...')
    servers = list()
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'html.parser')
        title = 'yitianjianss'
        info = {'message': '为确保安全，服务器地址会不定期更新。', 'url': url, 'name': str(title)}
        qr = map(lambda x: url + x.attrs['src'], soup.find_all('img'))
        for i, img_url in enumerate(qr):
            try:
                servers.append(parse(scanNetQR(img_url, headers=headers), ' '.join([title, str(i)])))
            except Exception as e:
                logging.exception(e, stack_info=False)
                print('IMG_URL FOR yitianjianss:', img_url)
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def acquire_doub_url(url='https://doub.io/sszhfx/'):
    print('req doub...')

    try:
        html = requests.get(url, headers=fake_ua)
        soup = BeautifulSoup(html.text, 'html.parser')
        urls = list(set(map(lambda x: x.get('href'), filter(
            lambda x: x.text.strip() != '1', soup.find_all('a', attrs={'class': 'page-numbers'})))))
        urls.append(url)
    except Exception as e:
        logging.exception(e, stack_info=True)
        print('DOUB_URL:', url)
        urls = [url]
    return set(urls)


def crawl_iss(url='https://my.ishadowx.net', headers=fake_ua):
    print('req iss...')

    try:
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}

    try:

        info = {
            'message': soup.find('div', attrs={'id': 'portfolio'}).find('div', attrs={'class': 'section-title text-center center'}).text,
            'name': 'ishadowx',
            'url': url}

        '''servers[-1]['name'] = tmp[0]
        servers[-1]['server'] = tmp[0]
        servers[-1]['server_port'] = tmp[0]
        servers[-1]['password'] = tmp[0]
        servers[-1]['method'] = tmp[0]
        servers[-1]['ssr_protocol'] = tmp[0]
        servers[-1]['obfs'] = tmp[0]'''

        soup = BeautifulSoup(data.text, 'html.parser')
        all_server_data = soup.find_all('div', attrs={'class': 'hover-text'})
        servers = list()
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}

    for i, server in enumerate(all_server_data):
        try:
            servers.append(dict())
            server_data = re.split('\s*\n\s*', server.text.strip())
            servers[-1]['server'] = server_data[0].split(':')[-1].strip()
            servers[-1]['server_port'] = re.findall('\d+', server_data[1])[0]
            servers[-1]['remarks'] = ' '.join(['ishadowx.com', str(i)])
            servers[-1]['password'] = server_data[2].split(':')[-1].strip()
            servers[-1]['method'] = server_data[3].split(':')[-1].strip()
            if 'QR' not in server_data[4]:
                servers[-1]['ssr_protocol'], servers[-1]['obfs'] = server_data[4].strip().split(maxsplit=1)
                servers[-1]['remarks'] = ' '.join([servers[-1]['remarks'], 'SSR'])
        except Exception as e:
            logging.exception(e, stack_info=True)
    return servers, info



