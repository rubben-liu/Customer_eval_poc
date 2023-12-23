#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import os

hasModel = False
for dirname, _, filenames in os.walk('.'):
    for filename in filenames:
        if(filename == 'insurance_model.pkl'):
            print('Already have insurance_model.pkl')
            hasModel = True


# In[2]:


df=pd.read_csv("./dataset/Insurance.csv")


# In[3]:


df.head()


# In[4]:


df.describe()


# In[5]:


df["sex"]=df['sex'].replace("female",1).replace("male",2)
df["smoker"]=df['smoker'].replace("yes",1).replace("no",0)
df.describe()
# df['Insulin']=df['Insulin'].replace(0,df['Insulin'].mean())
# df['SkinThickness']=df['SkinThickness'].replace(0,df['SkinThickness'].mean())
# df['BloodPressure']=df['BloodPressure'].replace(0,df['BloodPressure'].mean())
# df['Glucose']=df['Glucose'].replace(0,df['Glucose'].mean())
# df['DiabetesPedigreeFunction']=df['DiabetesPedigreeFunction'].replace(0,df['DiabetesPedigreeFunction'].mean())


# In[6]:


df.isnull().sum()


# In[7]:


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

import pickle


# In[8]:


x=df[['age', 'sex', 'bmi', 'smoker']]
y=df['charges']


# In[9]:


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=42)


# In[10]:


clf=DecisionTreeRegressor(random_state = 42)


# In[11]:


if not hasModel:
    clf.fit(x_train,y_train)
else:
    with open('insurance_model.pkl','rb') as f:
        clf = pickle.load(f)


# In[12]:


y_pred=clf.predict(x_test)


# In[13]:


mse = mean_squared_error(y_test, y_pred)
mse


# In[14]:


# import matplotlib.pyplot as plt

# plt.figure(figsize=(8, 4))
# plt.scatter(y_test, y_pred, color='green', label='Decision Tree')
# plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
# plt.title('Decision Tree: Actual vs. Predicted') 
# plt.xlabel('Actual')
# plt.ylabel('Predicted')
# plt.legend()
# plt.show()


# In[15]:


with open('insurance_model.pkl','wb') as f:
    pickle.dump(clf,f)


# In[16]:


print('Successfully imported insurance_model')

