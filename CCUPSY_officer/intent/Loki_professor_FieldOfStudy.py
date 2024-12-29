#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for professor_FieldOfStudy

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict,
        refDICT       dict,
        pattern       str

    Output:
        resultDICT    dict
"""

from random import sample
import json
import os
import sys
import pandas as pd
import Loki_ask_lecture_activity as lecture

INTENT_NAME = "professor_FieldOfStudy"
CWD_PATH = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(os.path.dirname(CWD_PATH), "lib"))

from Account import *
"""
Account 變數函數清單
[變數] BASE_PATH       => 根目錄位置
[變數] LIB_PATH        => lib 目錄位置
[變數] INTENT_PATH     => intent 目錄位置
[變數] REPLY_PATH      => reply 目錄位置
[變數] ACCOUNT_DICT    => account.info 內容
[變數] ARTICUT         => ArticutAPI (用法：ARTICUT.parse()。 #需安裝 ArticutAPI.)
"""

sys.path.pop(-1)

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(CWD_PATH, "USER_DEFINED.json"), encoding="utf-8"))
except:
    pass

replyDICT = {}
replyPathSTR = os.path.join(REPLY_PATH, "reply_{}.json".format(INTENT_NAME))
if os.path.exists(replyPathSTR):
    try:
        replyDICT = json.load(open(replyPathSTR, encoding="utf-8"))
    except Exception as e:
        print("[ERROR] reply_{}.json => {}".format(INTENT_NAME, str(e)))
CHATBOT = True if replyDICT else False

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if ACCOUNT_DICT["debug"]:
        print("[{}] {} ===> {}".format(INTENT_NAME, inputSTR, utterance))

def get_professors_by_field(field):
 
    """
    根據領域查找教授
    Args:
        field: 領域名稱（如"發展"）
    Returns:
        list: 該領域的教授列表
    """
    try:
        file_path = os.path.join(os.path.dirname(CWD_PATH), "intent", "data", "professor_FieldOfStudy.xlsx")
        df = pd.read_excel(file_path)
        
        # 根據不同領域選擇對應的列名
        field_column_mapping = {
            "社心": "社會與人格領域",
            "發展": "發展領域",
            "臨床": "臨床領域",
            "認知": "認知領域",
            "生心": "生理領域",
            "計量與方法": "計量與方法領域"
        }
        
        field_column = field_column_mapping.get(field)
        if field_column and field_column in df.columns:
            # 獲取該領域的所有教授（排除NaN值）
            professors = df[field_column].dropna().tolist()
            return professors
        return []
    except Exception as e:
        print(f"查詢教授時發生錯誤: {str(e)}")
        return []

def find_field_in_args(args):

    """
    在args中尋找可能的領域名稱
    """
    # 定義領域及其同義詞對應關係
    field_mapping = {
        "社心": ["社心", "社會與人格", "社會心理學", "社會心理學領域","社心領域"],
        "發展": ["發展", "發展心理學", "發展心理學領域","發展領域"],
        "臨床": ["臨床", "臨床心理學", "臨床心理學領域","臨床領域"],
        "認知": ["認知", "認知心理學", "認知心理學領域","認知領域"],
        "生心": ["生心", "生理心理學", "生理心理學領域","生心領域"],
        "計量與方法": ["計量與方法", "計量", "研究方法","計量領域"],
        "活動":["活動"]
    }
    for arg in args:
        if arg == "活動":
            utterance = "[系上]有哪些活動"
            
            replySTR = lecture.getReply(utterance, args) 
            return replySTR

    for arg in args:
        # 檢查每個參數是否匹配任何領域或其同義詞
        for field, synonyms in field_mapping.items():
            if arg in synonyms:
                return field
    return None

def getReply(utterance, args):
    """
    從 reply JSON 文件中獲取回應
    """
    try:
        # 在args中尋找領域名稱
        field = find_field_in_args(args)
        if field:
            professors = get_professors_by_field(field)
            
            if professors:
                # 格式化教授列表
                professors_str = "\n".join(f"{i+1}. {prof}" for i, prof in enumerate(professors))
                # 組合完整回應
                replySTR = f"{replyDICT[utterance]}\n{professors_str}"
            else:
                replySTR = f"抱歉，找不到{field}領域的教授。"
        else:
            replySTR = replyDICT.get("default", "")

            
        return replySTR
    except Exception as e:
        print(f"getReply 發生錯誤: {str(e)}")
        return replyDICT.get("default", "")

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern="", toolkitDICT={}):
    debugInfo(inputSTR, utterance)

    if utterance == "[專門]從事[發展]的[教授]有誰":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[專門]研究[發展]的[教授]有誰":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[發展]有哪些教授":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[發展]有哪些老師":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[發展]的[教授]有哪些人":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[發展]的[教授]有誰":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "哪些[教授][專門]從事[發展]研究":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "哪些[教授]在[發展]有[專長]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "從事[發展]研究的[教授]有誰":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    return resultDICT


if __name__ == "__main__":
    from pprint import pprint

    resultDICT = getResult("發展有哪些教授", "[發展]有哪些[教授]", [], {}, {})
    pprint(resultDICT)