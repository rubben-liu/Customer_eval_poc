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


from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext


# In[4]:


def receive_input():
    global name, age, height, weight, gender, smoke, bmi
    global gender_combobox
    name = name_entry.get()
    age = int(age_entry.get())
    height = float(height_entry.get())
    weight = float(weight_entry.get())
    
    gender = 1 if gender_combobox.current() == 0 else 2
    smoke = 1 if smoke_combobox.current() == 0 else 0

    bmi = weight / ((height / 100) ** 2)


# In[5]:


def calc():
    global cardio, diabete, insu_cost
    cardio = diab_clf.predict([[age, gender, bmi, smoke]])
    diabete = card_clf.predict([[age, gender, bmi, smoke]])
    insu_cost = insu_clf.predict([[age, gender, bmi, smoke]])[0]


# In[6]:


def display_result():
    global cardio, diabete, insu_cost

    if(cardio == 1):
        res.insert(INSERT, "Chance to have diabete\n")
    if(diabete == 1):
        res.insert(INSERT, "Chance to have cardiovascular disease\n")

    res.insert(INSERT, "Insurance cost estimate = " + '{:.2f}'.format(insu_cost) + '\n')


# In[7]:


def recommand_product():
    max = 0

    with open('./dataset/insurance_product.csv','r') as f:
        f.readline()
        for line in f:
            if float(line.split(',')[2]) < insu_cost and max < float(line.split(',')[2]):
                max = float(line.split(',')[2])
                product = line

        res.insert(INSERT, 'Recommand Product: \n' + \
              'id = ' + product.split(',')[0] + '\n' + \
              'product name = ' + product.split(',')[1] + '\n' + \
              'premium = ' + product.split(',')[2] + '\n' + \
              'limit = ' + product.split(',')[3] + '\n' + \
              'deductible = ' + product.split(',')[4] + '\n'
             )


# In[8]:


def save_user():
    new_user = record_var.get()
    
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
        res.insert(INSERT, 'Recorded!')


# In[9]:


def eval_customer():
    res.config(state = NORMAL)
    res.delete(1.0, END)
    
    receive_input()
    calc()
    display_result()
    recommand_product()
    save_user()


# In[10]:


if __name__ == '__main__':
    root = Tk()
    root.geometry('800x600+300+200')
    root.title('Customer_Eval')
    
    record_var = BooleanVar()
    record_var.set(True)
    name = ''
    age = 0
    height = 0.0
    weight = 0.0
    gender = 1
    smoke = 0
    bmi = 0.0
    cardio = 0
    diabete = 0
    insu_cost = 0.0
    product = ''

    name_label = Label(root, text = 'Name:')
    name_label.place(x = 100, y = 50)

    name_entry = Entry(root, width = 20)
    name_entry.place(x = 200, y = 50)

    age_label = Label(root, text = 'Age:')
    age_label.place(x = 400, y = 50)

    age_entry = Entry(root, width = 20)
    age_entry.place(x = 500, y = 50)

    height_label = Label(root, text = 'Height(cm):')
    height_label.place(x = 100, y = 100)

    height_entry = Entry(root, width = 20)
    height_entry.place(x = 200, y = 100)

    weight_label = Label(root, text = 'Weight(kg):')
    weight_label.place(x = 400, y = 100)

    weight_entry = Entry(root, width = 20)
    weight_entry.place(x = 500, y = 100)

    gender_label = Label(root, text = 'Gender(F/M):')
    gender_label.place(x = 100, y = 150)

    gender_combobox = ttk.Combobox(root, height = 3, values = ('Female', 'Male'), state = 'readonly')
    gender_combobox.set('Female')
    gender_combobox.place(x = 200, y = 150)

    smoke_label = Label(root, text = 'Smoke(Y/N):')
    smoke_label.place(x = 400, y = 150)

    smoke_combobox = ttk.Combobox(root, height = 3, values = ('Yes', 'No'), state = 'readonly')
    smoke_combobox.set('No')
    smoke_combobox.place(x = 500, y = 150)

    record_checkbutton = Checkbutton(root, text = 'Record your info(Y/N): ', variable = record_var)
    record_checkbutton.place(x = 200, y = 200)

    submit_button = Button(root, text = 'Submit', command = eval_customer)
    submit_button.place(x = 400, y = 200)

    res = scrolledtext.ScrolledText(root, width = 75, height = 10)
    res.place(x = 100, y = 300)
    
    root.attributes("-topmost", 1)
    root.update()
    root.attributes("-topmost", 0)

    root.mainloop()


# In[ ]:




