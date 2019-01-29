# -*- coding: utf-8 -*-
import re
import pandas as pd
from pandas import DataFrame, Series
from google.cloud import translate  # Use google cloud API instead

translate_client=translate.Client()

ori_data = pd.read_excel("./JS.xlsx",header=3,sheet_name=0)
# Import data, put the third line as header
from pypinyin import pinyin, lazy_pinyin, Style
# Import pinyin script
# print(ori_data)
# Print data
countylist=list(ori_data.columns.str.strip())
# print(countylist)
countylist_pinyin=[]
# Extract county from table

count=0
for county in countylist:
    countyname_pinyin_list=lazy_pinyin(county,strict=False) # County name is converted into pinyin, but put in the list
    countystr_t=" ".join(countyname_pinyin_list) # Combine the pinyin in the list (the element is charactor) to a word (county name) by blank
    print(countystr_t)
    if re.match(r"(\w+\s\w+)(?:\sfu|\sxian|\szhi\sli\szhou|\sting|\szhou|\szhi\sli\sting)",countystr_t)!=None:
        countytitlebe=re.match(r"(\w+\s\w+)(?:\sfu|\sxian|\szhi\sli\szhou|\sting|\szhou|\szhi\sli\sting)",countystr_t)
        pirnt(countytitlebe)
        countytitle=countytitlebe.group(1)
        # Check and match pinyin of county name with "fu, xian, zhou, ting, zhi li zhou" as level
    else:
        countytitle=countystr_t # No match case
    print(countytitle)
    countystr=countytitle.replace(" ","") # Delete blank
    print(countystr)
    countylist_pinyin.append(countystr)
    count+=1
    print(count)

countylist_EN=[]  # Prepare an empty list
counte=0
def is_chinese(uchar):         
    if '\u4e00' <= uchar<='\u9fff':
        return True
    else:
        return False
# Check if the variable is Chinese
def is_other(uchar):
    if not is_chinese(uchar):
        return True
    else:
        return False
# Check if the variable is not Chinese
for county in countylist:
    #translator=Translator() # Try to initialize
    counte +=1 # count in case some missing translation
    dic_county=translate_client.translate(county)
    # Translate every county in countylist
    print(counte)
    t_county=dic_county["translatedText"]
    if re.match(r"(\w+)(?:\sPrefecture|\sCounty|\sZhisli\sState|\sHall|\sState|\sZhili\sHall)",t_county)!=None:
        tt_county=re.match(r"(\w+)(?:\sPrefecture|\sCounty|\sZhisli\sState|\sHall|\sState|\sZhili\sHall)",t_county).group(1).lower()
        # Check for the level and drop the level-name
    else:
        tt_county=str(t_county).lower()
    
    countylist_EN.append(tt_county)
    print(t_county)
        # Add translations into new list. Convert translations into string
    #else:
        #citylist_EN.append("0")
        # Some words are not translated. Replace them with "0"
       
        # This try was failed in this sample 
print(countylist_EN)

for county in countylist_pinyin:
    if county!=countylist_EN[countylist_pinyin.index(county)]: # Check these two list whether they have the same name
        print(county)
        print(countylist_EN[countylist_pinyin.index(county)])
        print(countylist_pinyin.index(county))
    else:
        print('ok')

countylist_pinyin[34]="changzhou"

alist=range(1368,1913)
blist=[str(x) for x in alist]
#print(blist)
df_t=pd.DataFrame(columns=countylist_pinyin,index=blist)
print(df_t)

#df_t.to_excel("./JS_default.xlsx")