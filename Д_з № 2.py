#!/usr/bin/env python
# coding: utf-8

# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с сайта HH. Приложение должно анализировать все страницы сайта. Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

# In[1]:


import requests as req
from bs4 import BeautifulSoup as bs
import json
import lxml
import csv
import pandas as pd
import urllib.parse


# In[2]:


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'
}


# In[3]:


URL = 'https://hh.ru/search/vacancy'


# In[4]:


def get_html(url, params=''):
    html = req.get(url, headers=HEADERS, params=params)
    return html


# In[5]:


def get_hh_content(html):
    soup = bs(html, 'lxml')
    items = soup.find_all('div', class_='vacancy-serp-item')
    vacancy = []

    for item in items:
        vacancy.append(
            {
                'site': 'HeadHanter', # Название сайта
                'title': item.find('div', class_='vacancy-serp-item__info').get_text(), # Название вакансии
                'link': item.find('div', class_='vacancy-serp-item__info').find('a').get('href'), # Ссылка на вакансию
                'salary': item.find('div', class_='vacancy-serp-item__sidebar').get_text(), # Зарплата
                'city': item.find('span', class_='vacancy-serp-item__meta-info').get_text(), # Город
                'organization': item.find('div', class_='vacancy-serp-item__meta-info-company').get_text(), # Название компании
                'note': item.find('div', class_='vacancy-label') # Примечание
            }
        )      
    # Приведем данные к нормальному виду
    for i in vacancy:
        # Salary
        if i['salary']:
            salary_list = i['salary'].split(' ')
            if salary_list[0] == 'от':
                i['salary_min'] = salary_list[1]
                i['salary_max'] = None
            elif salary_list[0] == 'до':
                i['salary_min'] = None
                i['salary_max'] = salary_list[1]
            else:
                i['salary_min'] = salary_list[0]   
                i['salary_max'] = salary_list[2]     
            i['salary_currency'] = salary_list[-1]
        else:
            i['salary_min'] = None  
            i['salary_max'] = None
            i['salary_currency'] = None
        i.pop('salary')
        # note
        if i['note'] != None:
            i['note'] = i['note'].get_text()
        # City
        if i['city']:
            city_list = i['city'].split(',')
            i['city'] = city_list[0]
    return vacancy


# In[6]:


def main_parsing():
    HH_URL = 'https://hh.ru/search/vacancy'
    
    
    POST = str(input('Введите название вакансии для парсинга: '))
    PAGES = int(input('Количество страниц для парсинга: '))
    HH_HTML = get_html(HH_URL)
    
    
    if HH_HTML.status_code == 200:
        vacancy = []
        for page in range(1, PAGES+1):
            print(f'Парсятся страницы {page}')
            hh = get_html(HH_URL, params={'text': POST, 'page': page})
            vacancy.extend(get_hh_content(hh.text))
        result = pd.DataFrame(vacancy)
    else:
        print('error')
    return result


# In[7]:


df = main_parsing()
df


# In[8]:


df.to_csv('09082021', index=False)

