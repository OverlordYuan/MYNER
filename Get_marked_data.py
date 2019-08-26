# -*- coding:utf-8 -*-
"""
 Created by Overlord Yuan at 2019/8/26
"""
import re
import pandas as pd


def get_people(sent,label_list,targets):
    for target in targets:
        flag = 1
        start = 0
        end = len(sent)
        while flag:
            start = sent.find(target,start)
            if start<0:
                flag = 0
            else:
                label_list[start] = 'B-PER'
                label_list[start+1:start+len(target)-1]=['I-PER']*(len(target)-1)
                start += len(target)


def get_address():
 return 0

def get_org():
 return 0

data_df = pd.read_csv('query_result.csv',sep='%')
for index in data_df.index:
    temp = data_df.loc[index].values
    if temp[2] == 'undefined' and temp[3] == 'undefined'and  temp[4] == 'undefined':
        continue
    else:
        content =re.sub(r'\n|\\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\\', '', temp[0] + '。' + temp[1])
        sents = re.split("[。？!]",content)
        people = temp[2].replace('[', '').replace(']', '').replace('"','').split(',')
        address = temp[3].replace('[', '').replace(']', '').replace('"', '').split(',')
        org = temp[4].replace('[', '').replace(']', '').replace('"', '').split(',')
        for sent in sents:
            label_list = [0]*len(sent)
            if people[0] != 'undefined':
                get_people(sent,label_list,people)
            if address[0] != 'undefined':
                get_address()
            if org[0] != 'undefined':
                get_org()

print(data_df)