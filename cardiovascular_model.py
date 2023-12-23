#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import os

hasModel = False
for dirname, _, filenames in os.walk('.'):
    for filename in filenames:
        if(filename == 'cardiovascular_model.pkl'):
            print('Already have cardiovascular_model.pkl')
            hasModel = True


# In[2]:


df=pd.read_csv("./dataset/Cardiovascular.csv", delimiter=';')


# In[3]:


df.head()


# In[4]:


df.describe()


# In[5]:


df['BMI'] = df['weight'] / df['height'] ** 2
# df["BMI"]=df['BMI'].replace(0,df['BMI'].mean())
# df['Insulin']=df['Insulin'].replace(0,df['Insulin'].mean())
# df['SkinThickness']=df['SkinThickness'].replace(0,df['SkinThickness'].mean())
# df['BloodPressure']=df['BloodPressure'].replace(0,df['BloodPressure'].mean())
# df['Glucose']=df['Glucose'].replace(0,df['Glucose'].mean())
# df['DiabetesPedigreeFunction']=df['DiabetesPedigreeFunction'].replace(0,df['DiabetesPedigreeFunction'].mean())


# In[6]:


df.isnull().sum()


# In[7]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score,confusion_matrix

import pickle


# In[8]:


x=df[['age', 'gender', 'BMI', 'smoke']]
y=df['cardio']


# In[9]:


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=42)


# In[10]:


log_ref=LogisticRegression(random_state = 42)


# In[11]:


log_ref.fit(x_train,y_train)


# In[12]:


parameters={
    'penalty':['l1', 'l2', 'elasticnet', None],
    'C':np.logspace(-3,3,7),
    'solver':['newton-cg','lbfgs','liblinear']
}
import warnings
warnings.filterwarnings('ignore')


# In[13]:


if not hasModel:
    clf=GridSearchCV(
        log_ref,param_grid=parameters,
        scoring='accuracy',
        cv=10
    )
    clf.fit(x_train,y_train)
else:
    with open('cardiovascular_model.pkl','rb') as f:
        clf = pickle.load(f)


# In[14]:


y_pred=clf.predict(x_test)


# In[15]:


conf_mat=confusion_matrix(y_test,y_pred)
conf_mat


# In[16]:


accuracy=accuracy_score(y_test,y_pred)
accuracy


# In[17]:


with open('cardiovascular_model.pkl','wb') as f:
    pickle.dump(clf,f)


# In[18]:


print('Successfully imported cardiovascular_model')

