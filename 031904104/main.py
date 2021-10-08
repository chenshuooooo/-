# -*- coding:utf-8 -*-
import linecache
import re
from cnradical import Radical, RunOption
from xpinyin import Pinyin
import sys
def find4(string,word):#用于处理纯拼音的情况（不带音节）例如falungong
    p = Pinyin()
    result1 = p.get_pinyin(word)
    # print(result1)
    end=0
    head=0
    s = result1.split('-')
    # print(s)
    #print(s[-1])
    #print(a[-1])
    result1=""
    result2=""
    # print(result3)
    res= re.search(s[0],string)
    if res != None:
        head = res.start()
        reg = re.search(s[-1],string)
        if reg != None:
            end = reg.end()
        result2 = string[head:end]
    return result2
    if res == None:
        return result1

def find2(string,word):#用于处理拆偏旁的情况
    output1 = ""
    end=0
    head=0
    output=""
    radical = Radical(RunOption.Radical)#调用拆偏旁的方法
    word_radical=[radical.trans_ch(ele) for ele in word]#这里得到的是一个列表
    #print(word_radical)
    x1 = word_radical[0]
    y1 = word_radical[-1]
    #print(x1,y1)
    reg = re.search(x1,string)#用正则表达式匹配位置
    res = re.search(y1,string)
    if reg!= None:
        head = reg.start()
        if res != None:
            end = res.end()
            output = string[head:end]
        return output
    if reg == None:
        return output1

def find1(string,word):#用于处理原形及谐音的情况
    output = ""
    pinyin = Radical(RunOption.Pinyin)
    word_pinyin=[pinyin.trans_ch(ele) for ele in word]#转换为带音调的拼音列表
    #print(word_pinyin)
    x1=word_pinyin[0]
    y1=word_pinyin[-1]
    try:
        #string = "留下珐论功，站也不是，坐也不是。嘴里的话，更鞋csc教加说不法轮功出口了。"
        pinyin = Radical(RunOption.Pinyin)
        pinyin = [pinyin.trans_ch(ele) for ele in string]
        str1 = list(string)
        #print(pinyin)
        for i, n in enumerate(pinyin):
            #print(i,n)
            if pinyin[i] == x1:
                head = i
                #print(head)
                break
        for j, m in enumerate(pinyin):
            #print(i,n)
            if pinyin[j] == y1 and j>head:
                end = j
                #print(end)
                break
        str2 = str1[head:end+1]
        a = ''
        output = a.join(str2)
        # print(i)
        # print(str)
        # print(pinyin)
    except :
        pass
        output=""
    return output

def find3(string,word):#处理英文敏感词 例如fuck
    x=word[0]
    x=x.lower()
    y=word[-1]
    y=y.lower()
    try:
        #string = "f留下珐论ulck功，站g也不是，坐也不是。嘴里的话，更加说不法轮功出口了。"
        string1=string.lower()
        # print(str1)
        result=""
        result1=""
        end=0
        head=0
        res = re.search(x,string1)
        reg = re.search(y,string1)
        if res != None:
            head = res.start()
            if reg != None:
                end = reg.end()
            result = string[head:end]
        return result
        if res == None:
            return result1
    except :
        pass
        output=""
    return output

if len(sys.argv) == 4:
    fileword = sys.argv[1]
    fileorg = sys.argv[2]
    fileans = sys.argv[3]
else:
    print("输入参数个数不符，请重新输入。")
def deal_sensitive(fileword,fileorg,fileans):#主函数
    with open(fileword, "r", encoding='UTF-8') as f:  # 读取敏感词文件
        word = []
        j = 0
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            #print(line)
            j = j + 1
            word.append(line)
        # print(a)
        total=0
        with open(fileorg, "r", encoding="utf-8") as f:
            count = -1
            for line in f:
                count = count + 1
                # print(line.strip())#测试用,可删
            # print(count)#测试用,可删
            num = 0
            while num <= count:
                text = linecache.getline(fileorg, num)  # "读取指定行"
                num1 = str(num)
                h=0
                while h<j:
                    if word[h].encode('UTF-8').isalpha() == False:
                        a = find1(text, word[h])
                        b = find2(text, word[h])
                        d = find4(text, word[h])
                        with open(fileans, "a", encoding='UTF-8') as fi:
                            if d != "":
                                total = total + 1
                                fi.write("Line" + num1 + ": <" + word[h] + "> " + d + "\n")
                        with open(fileans, "a", encoding='UTF-8') as fi:
                            if a != "":
                                total = total + 1
                                fi.write("Line" + num1 + ": <" + word[h] + "> " + a + "\n")
                        with open(fileans, "a", encoding='UTF-8') as fi:
                            if b != "":
                                total = total + 1
                                fi.write("Line" + num1 + ": <" + word[h] + "> " + b + "\n")
                    if word[h].encode('UTF-8').isalpha() == True:
                        c = find3(text, word[h])
                        with open(fileans, "a", encoding='UTF-8') as fi:
                            if c != "":
                                total = total + 1
                                fi.write("Line" + num1 + ": <" + word[h] + "> " + c + "\n")
                    h=h+1
                num = num + 1
    total1=str(total)
    return total1

def total(total,fileans):#在输出文件首部插入总共有多少个敏感词
    with open(fileans, 'r+', encoding='UTF-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("Total:"+ total + "\n"+content)
total1=deal_sensitive(fileword,fileorg,fileans)
total(total1,fileans)
