#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cardiovascular_model
import diabete_model
import insurance_model
import insurance_product_generator

import os


# In[2]:


import pickle

with open('diabete_model.pkl','rb') as f:
    diab_clf = pickle.load(f)

with open('cardiovascular_model.pkl','rb') as f:
    card_clf = pickle.load(f)
    
with open('insurance_model.pkl','rb') as f:
    insu_clf = pickle.load(f)


# In[3]:


name = input('Name: ')
age = int(input('Age: '))
height = float(input('Height(cm): '))
weight = float(input('Weight(kg): '))

gender = 1 if input('Gender(F/M):') == 'F' else 2
smoke = 1 if input('Smoke(Y/N):') == 'Y' else 0

bmi = weight / height ** 2


# In[4]:


cardio = diab_clf.predict([[age, gender, bmi, smoke]])
diabete = card_clf.predict([[age, gender, bmi, smoke]])
insu_cost = insu_clf.predict([[age, gender, bmi, smoke]])[0]


# In[5]:


if(cardio == 1):
    print("Chance to have diabete")
if(diabete == 1):
    print("Chance to have cardiovascular disease")
    
print("Insurance cost estimate = " + '{:.2f}'.format(insu_cost))


# In[6]:


max = 0
product = ''

with open('./dataset/insurance_product.csv','r') as f:
    f.readline()
    for line in f:
        if float(line.split(',')[2]) < insu_cost and max < float(line.split(',')[2]):
            max = float(line.split(',')[2])
            product = line
            
    print('Recommand Product: \n' + \
          'id = ' + product.split(',')[0] + '\n' + \
          'product name = ' + product.split(',')[1] + '\n' + \
          'premium = ' + product.split(',')[2] + '\n' + \
          'limit = ' + product.split(',')[3] + '\n' + \
          'deductible = ' + product.split(',')[4] + '\n'
         )


# In[7]:


new_user = True if input('Record your info(Y/N): ') == 'Y' else False


# In[8]:


if not os.path.exists('./dataset/customer.csv'):
    with open('./dataset/customer.csv','w') as f:
        f.write(','.join(['id','name', 'age', 'height/cm', 'weight/kg', 'gender/F:M', 'smoke/Y:N', 'cardio/1:0', 'diabete/1:0', 'insu_cost/$', 'match_product_id' + '\n']))
        f.close()
        
with open('./dataset/customer.csv','r') as f:
    for line in f:
        if line.split(',')[1] == str(name) and \
        line.split(',')[2] == str(age) and \
        line.split(',')[3] == str(height) and \
        line.split(',')[4] == str(weight) and \
        line.split(',')[5] == ['F' if gender == 1 else 'M'][0] and \
        line.split(',')[6] == ['Y' if smoke == 1 else 'N'][0]:
            new_user = False
            break

if new_user:
    with open('./dataset/customer.csv','a+') as f:
        f.write(','.join([str(sum(1 for line in f) + 1), str(name), str(age), str(height), str(weight),\
                ['F' if gender == 1 else 'M'][0], ['Y' if smoke == 1 else 'N'][0], str(cardio[0]), str(diabete[0]), str(insu_cost), str(product.split(',')[0]) + '\n']))
    print('Recorded!')


# In[ ]:




