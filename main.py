import requests
import json
from datetime import datetime
from token_vk import token_vk
from token_yandex import token_yandex
from time import sleep
from tqdm import tqdm
import os


class VK:
    def __init__(self, id_number):
        self.token = str(token_vk)
        self.url = r'https://api.vk.com/method'
        self.id = id_number
        self.id_album = id_album

    def write_json(self, data):
        with open('all_photos_info', 'w') as file:
            json.dump(data, file, indent=2)

    def get_json(self):
        params = {
            'owner_id': self.id,
            'access_token': self.token,
            'album_id': self.id_album,
            'extended': '1',
            'v': '5.131'
        }
        spell_url = '/photos.get'
        final_url = self.url + spell_url
        response = requests.get(final_url, params)
        data = response.json()
        return data['response']

    def repeat(self, list_values):
        counter = []
        dict_num = {}
        for elem in list_values:
            if elem in list_values:
                dict_num[elem] = dict_num.get(elem, 0) + 1
            if dict_num[elem] > 1:
                counter.append(elem)
        return counter

    def converter_date(self, date):
        return str(datetime.utcfromtimestamp(date).strftime('%d.%m.%Y'))

    def largest(self, size_list):
        return size_list['width']

    def creat_folder(self):
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
            os.chdir(folder_name)
        else:
            os.chdir(folder_name)

    def download(self, url, name_file):
        res = requests.get(url)
        with open(name_file, 'wb') as file:
            file.write(res.content)

    def __file_info(self):
        data_dict = self.get_json()
        count_like = []
        file_info = {}
        for like in data_dict['items']:
            count_like.append(like['likes']['count'])
        repeat_like = self.repeat(count_like)
        for photo in tqdm(data_dict['items']):
            size = photo['sizes']
            file_info['url'] = max(size, key=self.largest)['url']
            file_info['size'] = max(size, key=self.largest)['type']
            if photo['likes']['count'] in repeat_like:
                file_info['name_file'] = str(photo['likes']['count']) + '-' + self.converter_date(photo['date']) + '.jpg'
            else:
                file_info['name_file'] = str(photo['likes']['count']) + '.jpg'
            sleep(0.1)
            yield file_info

    def uploading_saved(self):
        data_photo = []
        if response == 'yes':
            self.creat_folder()
        for x in self.__file_info():
            upload.upload_file(x['url'], x['name_file'])
            data_photo.append({'file_name': x['name_file'], 'size': x['size']})
            user.write_json(data_photo)
            if response == 'yes':
                self.download(x['url'], x['name_file'])


class Yandex:
    def __init__(self, name_folder):
        self.token = str(token_yandex)
        self.url = r'https://cloud-api.yandex.net'
        self.name_folder = name_folder

    def create_folder(self, name_folder):
        headers = {"Content-Type": "application/json",
                   "Authorization": self.token}
        params = {'path': name_folder}
        spell_url = r'/v1/disk/resources'
        method_url = self.url + spell_url
        requests.put(method_url, params=params, headers=headers)

    def upload_file(self, url, file_name):
        self.create_folder(self.name_folder)
        headers = {"Content-Type": "application/json",
                   "Authorization": self.token}
        params = {'path': f'{self.name_folder}/{file_name}',
                  'url': url,
                  'disable_redirects': False}
        spell_url = r'/v1/disk/resources/upload'
        final_url = self.url + spell_url
        res = requests.post(final_url, params=params, headers=headers)
        if res.status_code == 202:
            return
        else:
            print(f"Упс, что-то пошло не по плану код ошибки: {res.status_code}")


id_album = 'profile'
id_vk = input('Введите id пользователя - ')
album_select = input('Вы хотите сохранить фото из конкретного альбома?(Yes/No) - ').lower()
if album_select == 'yes':
    id_album = str(input('Введите id альбома - '))
folder_name = input('Введите имя папки в которую будут загруженны фото - ')
response = input('Сохранить фото на этом компьютере?(Yes/No) - ').lower()
if __name__ == '__main__':
    user = VK(id_vk)
    upload = Yandex(folder_name)
    user.uploading_saved()

