#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

'''
rule format:
ip-asn, 123456, direct
'''

ASN_URL = 'https://bgp.he.net/country/CN'
RULE_SAMPLE = 'ip-asn, {}, direct'
RULE_FILE_NAME = 'asn_cn2.list'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

def main():
    print('正在从网页获取ASN ... ...')
    all_asn = read_all_asn_form_net(ASN_URL)
    if all_asn:
        print('从网页获取ASN 成功！')
        rules = gen_rules(all_asn)
        write_rules_to_file(rules, RULE_FILE_NAME)
    else:
        print('从网页获取ASN 失败！请检查！！！')

def read_all_asn_form_net(url):
    asns = []
    try:
        r = requests.get(url, headers=HEADERS)
        ''' <td><a href="/AS133492"
        <a href="/AS63582" title
        '''
        strs = re.findall(r'<a href="/AS\d+" title', r.text)
        for str in strs:
            result = re.search(r'\d+', str).group()
            print('asn', result)
            asns.append(result)
    except:
        return []
    asns = list(dict.fromkeys(asns))
    return asns

def gen_rule(asn):
    return RULE_SAMPLE.format(asn)

def gen_rules(asns):
    rules = []
    for asn in asns:
        rules.append(gen_rule(asn))
    return rules

def write_rules_to_file(rules, file_path):
    if rules:
        with open(file_path, 'w') as f:
            for rule in rules:
                f.write(rule)
                f.write('\n')
        print('生成{}个规则, 已导出到{}'.format(len(rules), file_path))
    else:
        print("没有生成有效规则")

if __name__ == '__main__':
    main()
