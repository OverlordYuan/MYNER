# -*- coding:utf-8 -*-
"""
 Created by Overlord Yuan at 2019/8/26
"""
import re,os
import pandas as pd

def get_people(sent,label_list,targets):
    res = 0
    for target in targets:
        flag = 1
        start = 0
        while flag:
            start = sent.find(target,start)
            if start<0:
                flag = 0
            else:
                label_list[start] = 'B-PER'
                label_list[start+1:start+len(target)]=['I-PER']*(len(target)-1)
                start += len(target)
                res += 1
    return res


def get_address(sent,label_list,targets):
    res = 0
    for target in targets:
        flag = 1
        start = 0
        while flag:
            start = sent.find(target, start)
            if start < 0:
                flag = 0
            else:
                label_list[start] = 'B-LOC'
                label_list[start + 1:start + len(target)] = ['I-LOC'] * (len(target) - 1)
                start += len(target)
                res += 1
    return res
def get_org(sent,label_list,targets):
    res = 0
    for target in targets:
        flag = 1
        start = 0
        while flag:
            start = sent.find(target, start)
            if start < 0:
                flag = 0
            else:
                label_list[start] = 'B-ORG'
                label_list[start + 1:start + len(target)] = ['I-ORG'] * (len(target) - 1)
                start += len(target)
                res += 1
    return res

def write_label(sent,label):
    path_file_name = 'output/data_label.txt'
    sent = list(sent)
    label = label
    df = pd.DataFrame({"sent":sent, "label":label})
    if not os.path.exists(path_file_name):
        df.to_csv(path_file_name ,sep=' ', header=False,index=False)
    else:
        df.to_csv(path_file_name ,sep=' ', mode='a', header=False,index=False)



data_df = pd.read_csv('query_result.csv',sep='%')
for index in data_df.index:
    temp = data_df.loc[index].values
    if temp[2] == 'undefined' and temp[3] == 'undefined'and  temp[4] == 'undefined':
        continue
    else:
        content =re.sub(r'\n|\\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\\', '', temp[0] + '。' + temp[1]).strip()
        sents = list(filter(None,re.split("[。？!]",content)))
        people = temp[2].replace('[', '').replace(']', '').replace('"','').split(',')
        address = temp[3].replace('[', '').replace(']', '').replace('"', '').split(',')
        org = temp[4].replace('[', '').replace(']', '').replace('"', '').split(',')
        for sent in sents:
            label_list = [0]*len(sent)
            res  = 0
            if people[0] != 'undefined':
                res += get_people(sent,label_list,people)
            if address[0] != 'undefined':
                res += get_address(sent,label_list,address)
            if org[0] != 'undefined':
                res += get_org(sent,label_list,org)
            if res:
                write_label(sent,label_list)



print(data_df)