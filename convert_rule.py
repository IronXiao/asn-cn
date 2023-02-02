#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import re

'''
rule format:
ip-asn, 123456, direct
'''

ASN_FILE_NAME = 'asn_cn.txt'
ASN_DOWNLOAD_PATH = 'https://raw.githubusercontent.com/VirgilClyne/GetSomeFries/main/ruleset/ASN.China.list'
RULE_SAMPLE = 'ip-asn, {}, direct'
RULE_FILE_NAME = 'asn_cn.list'

def main():
    print('正在下载ASN 文件... ...')
    result = download_file_from_net(ASN_DOWNLOAD_PATH, ASN_FILE_NAME)
    if result:
        print('ASN 文件下载成功！')
        all_asn = read_all_asn_form_file(ASN_FILE_NAME)
        rules = gen_rules(all_asn)
        write_rules_to_file(rules, RULE_FILE_NAME)
    else:
        print('ASN 文件下载失败，请检查网络！！！')



def download_file_from_net(url, save_path):
    try:
        r = requests.get(url, stream=True, timeout=15)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        r.close()
    except KeyboardInterrupt:
        os._exit(0)
    except:
        return False
    return True

def read_all_asn_form_file(file):
    all_asn = []
    with open(file, 'r') as f:
        for line in f.readlines():
            if line.startswith('IP-ASN'):
                result = re.search(r'\d+', line).group()
                all_asn.append(result)
    all_asn = list(dict.fromkeys(all_asn))
    return all_asn



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