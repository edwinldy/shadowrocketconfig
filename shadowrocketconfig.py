#!/usr/bin/env python3
#coding=utf-8
import requests
import re
import datetime
import base64

def get_china_list():
    dnsmasq_china_list = 'https://github.com/felixonmars/dnsmasq-china-list/raw/master/accelerated-domains.china.conf'
    try:
        print('Getting china list...')
        data = requests.get(dnsmasq_china_list, verify=True)
        cache = open('chinalist', 'w', encoding='utf-8')
        cache.write(data.text)
        cache.close()
    except:
        print('Get china list update failed,use cache to update instead.')

    cache = open('chinalist', 'r', encoding='utf-8')
    china_list_config = ''
    for line in cache.readlines():
        domain = re.findall(r'\w+\.\w+', line)
        if len(domain) > 0:
            china_list_config += 'DOMAIN-SUFFIX,%s,DIRECT\n'%(domain[0])
    cache.close()
    return china_list_config

def get_gfw_list():
    gfw_list = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
    try:
        print('Getting gfw list...')
        data = requests.get(gfw_list, verify=True)
        data_decoded = base64.b64decode(data.text).decode('utf-8')
        #print(type(data_decoded))
        cache = open('gfwlist', 'w', encoding='utf8')
        cache.write(data_decoded)
        cache.close()
    except:
        print('Get gfw list update failed,use cache to update instead.')

    cache = open('gfwlist', 'r', encoding='utf8')
    gfw_domains = ''

    for line in cache.readlines():
        # 如果是是注释则跳过该行
        if re.findall('^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+', line):
            continue
        else:
            domain = re.findall('([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*', line)
            if len(domain) > 0:
                gfw_domains += 'DOMAIN-SUFFIX,%s,Proxy,force-remote-dns\n' % (domain[0])
    cache.close()
    return gfw_domains

def generate_config():
    tmp = open('./templates/Shadowrocket.conf', 'r', encoding='utf-8')
    config = open('Shadowrocket.conf', 'w', encoding='utf-8')
    rules = get_china_list() + get_gfw_list()
    tmp_content = tmp.read()
    print('generate config file...')
    tmp_content = tmp_content.replace('__rule__', rules)
    config.write(tmp_content)
    tmp.close()
    config.close()

if __name__ == '__main__':
    generate_config()