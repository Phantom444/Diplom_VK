#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from tqdm import tqdm, tnrange, tqdm_gui
import json
from pprint import pprint
import os.path
from os import path
import time


token_yd = 'AQAAAAABkrcEAADLW4G7lGu5xkbXhUM3ojoBCnc'
token_vk = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
count = 5
url_cr_dir = 'https://cloud-api.yandex.net/v1/disk/resources?'
params_cr_dir = {'path': 'py_diplom_basic'}
headers_cr_dir = {'Content-Type': 'application/json',
                  'Authorization': token_yd}

url_vk = 'https://api.vk.com/method/photos.get?'
id = '552934290'
params_vk = {'owner_id': id,
          'album_id': 'profile',
          'extended': 1,
          'v': '5.131',
          'access_token': token_vk,
          'photo_sizes': 1,
          }
url_upl_photo = 'https://cloud-api.yandex.net/v1/disk/resources/upload?'


def create_directory(url_cr_dir,headers_cr_dir, params_cr_dir):
    res = requests.put(url_cr_dir, headers= headers_cr_dir, params=params_cr_dir)
create_directory(url_cr_dir, headers_cr_dir, params_cr_dir)


def pars_vk(url_vk, params_vk):
    result_vk = requests.get(url_vk, params=params_vk)
    if result_vk.status_code == 200 and 'error' not in result_vk.json().keys():
        return result_vk
    else:
        print('Плохой ответ от VK')
        return


def is_file(name):
    return path.isfile(name)


def is_not_empty(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        if data:
            return data
        else:
            return


def write_file_json(list_data):
    with open('Info file.json', 'w') as f:
        json.dump(list_data, f, ensure_ascii=False, indent=2,)


def read_file_json():
    with open('Info file.json', encoding='utf-8') as f:
        data = json.load(f)
        return data


def write_file(list_data):
    if is_file('Info file.json'):
        if is_not_empty('Info file.json'):
            data = read_file_json()
            data += list_data
            write_file_json(data)
        else:
            write_file_json(list_data)
    else:
        write_file_json(list_data)


def list_of_names():
    list_name = []
    if is_file('Info file.json'):
        if is_not_empty('Info file.json'):
            data = read_file_json()
            for d in data:
                list_name.append(d['file_name'].strip('.jpg'))
    return list_name


def upload_photo(url_vk, params,url_upl_photo):
    res = pars_vk(url_vk, params)
    if res:
        for item in tqdm(res.json()['response']['items'], desc='Photos uploading', unit=' photo'):
            list_data = []
            name = f"{item['likes']['count']}"
            if name in list_of_names():
                name += '_' + str(time.time())
            params_upl_photo = {'path': f"py_diplom_basic/{name}.jpg",
                                'url': item['sizes'][-1]['url']}
            response = requests.post(url_upl_photo, params=params_upl_photo, headers=headers_cr_dir)
            data = {
                'file_name': f'{name}.jpg',
                'size': item['sizes'][-1]['type'],
                'data_save': time.ctime(item['date']),
                'data_upload': time.ctime(),
                'status upload': response.status_code
            }
            list_data.append(data)
            write_file(list_data)
        else:
            return
upload_photo(url_vk, params_vk, url_upl_photo)