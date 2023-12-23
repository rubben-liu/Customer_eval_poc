#!/usr/bin/env python
# coding: utf-8

# In[10]:


import random
import os

random.seed(42)

if not os.path.exists('./dataset/insurance_product.csv'):
    with open('./dataset/insurance_product.csv', 'w') as f:
        f.write(','.join(['id','product_name', 'premium', 'limit', 'deductible' + '\n']))
        f.close()
        
insurance_type = ['AH', 'Home', 'Auto', 'Life', 'Travel']
f_length = 100

row = 0
with open('./dataset/insurance_product.csv','r') as f:
    f.readline() # remove header
    for line in f:
        row+=1

with open('./dataset/insurance_product.csv','a+') as f:
    for i in range(row, f_length):
        premium = random.randint(1000, 100000)
        limit = int(premium * random.randint(10, 100) / 100) * 100
        deductible = int(premium / random.randint(2, 10) / 10) * 10
        f.write(','.join([str(i), insurance_type[random.randint(0, len(insurance_type) - 1)], 
                      str(premium), str(limit), str(deductible) + '\n']))


# In[ ]:





# In[ ]:




