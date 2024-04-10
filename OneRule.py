# -*- coding: utf-8 -*-
def rule(Data,s0,c0):
   #获取字段名称（行业名称_up），并转化为列表
   import numpy as np
   import pandas as pd
   c=list(Data.columns) 
   list1=[] #预定义定义列表list1，用于存放规则
   list2=[] #预定义定义列表list2，用于存放规则的支持度
   list3=[] #预定义定义列表list3，用于存放规则的置信度
   for k in range(len(c)):
       for q in range(len(c)):
           #对第c[k]个行业与第c[q]个行业计算行业轮动规则
           #规则的前件为c[k]
           #规则的后件为c[q]，计算周期与c[k]需后移一个周期
           c1=Data[c[k]][0:-1]
           c2=Data[c[q]][1:]
           I1=c1.values==1
           I2=c2.values==1
           t12=np.zeros((len(c1)))
           t1=np.zeros((len(c1)))
           t12[I1&I2]=1
           t1[I1]=1
           sp=sum(t12)/len(c1) #支持度
           co=sum(t12)/sum(t1) #置信度
           if co>c0 and sp>s0:
              list1.append(c[k]+'--'+c[q])
              list2.append(sp)
              list3.append(co)
           
   #定义字典，用于存放关联规则及其置信度、支持度   
   R={'rule':list1,'support':list2,'confidence':list3}
   #将字典转化为数据框
   R=pd.DataFrame(R)
   #将结果导出到Excel
   R.to_excel('R.xlsx')
   return R

