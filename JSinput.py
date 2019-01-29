import re
import pandas as pd
from pandas import DataFrame, Series
from pypinyin import pinyin, lazy_pinyin, Style
# Import pinyin script

ori_data = pd.read_excel("./JS_default.xlsx",header=0,sheet_name=0)


with open("freeze.txt",'r',encoding="utf-8-sig") as f:
    linelist = f.readlines()
    
countylist=list(ori_data.columns.str.strip())

countylist[countylist.index("changzhou")]="zhangzhou"
countylist[countylist.index("changzhou.1")]="changzhou"
countylist[countylist.index("jiangning.1")]="nanjing"
countylist[countylist.index("yizhen")]="yizheng"
print(countylist)
alist=range(1368,1913)
blist=[str(x) for x in alist]
#print(blist)
df_a=pd.DataFrame(columns=countylist,index=blist) # Construct dataframe
df_t=df_a.fillna(0)

#checkpr=" ".join(countylist)
#print(checkpr)
#check=str(checkpr)
#checkword=re.match("jiangning",check)
#print(checkword)

#print(lazy_pinyin("长洲",strict=False))
for ele in linelist:
    record=re.match(r"(\d\d\d\d)：(.*)",ele)
    if re.match(r"(\d\d\d\d)：(.*)",ele)!=None:
        #print(record)
        year=str(record.group(1))
        county=str(record.group(2))
        #print(year)
        #print(county)
        countyre=lazy_pinyin(county,strict=False) # Pinyinlize the string, but every charator is put in list as single element
        #print(countyre)
        countyrestr="".join(countyre) # Convert list into string, joint them without blank
        #print(countyrestr)
        countyrelist=re.split(r"[^a-z]+",countyrestr) # Get rid of "、" and then convert them into list again
        #print(countyrelist)
        for recounty in countyrelist:
            
            test=re.match(r"(\w+)(?:fu)",recounty)           
            #print(test)
            checklist=[]
            if re.match(r"(\w+)(?:fu)",recounty)==None:
                #print(test)
                p=re.compile(recounty)
                #print("if process of county "+ recounty) # Hint of if process
                #print(check)
                #print(p.match(check))
                #count=0
                
                for countypy in countylist:
                    #count+=1
                    #print(count)
                    if p.match(countypy)!=None:
                        #print(p.match(countypy))
                        #result=p.match(countypy).group(0)
                        #print(result)
                        #print(countypy)
                        if df_t.loc[year,countypy]==0:
                            df_t.loc[year,countypy]=1
                            #print("0 to 1")
                        else:
                            df_t.loc[year,countypy]+=1
                            #print("1 to some")
                        #print("fine county:"+recounty+" in year "+year)
                    checklist.append(p.match(countypy))
            else:
                repre=test.group(1)
                #print(repre)
                p=re.compile(repre)
                #print("else process of pre "+ repre)
                for countypy in countylist:
                    if p.match(countypy)!=None:
                        #print(p.match(countypy))
                        #result=p.match(countypy).group(0)
                        #print(result)
                        if df_t.loc[year,countypy]==0:
                            df_t.loc[year,countypy]=1
                            #print("0 to 1")
                        else:
                            df_t.loc[year,countypy]+=1
                            #print("1 to some")
                        #print("fined prefecture:"+repre+" in year "+year)
                    checklist.append(p.match(countypy))
            #print(checklist)
            if checklist==[None]*len(checklist):
                print(recounty+" "+year)
print(df_t)
#print(countylist)