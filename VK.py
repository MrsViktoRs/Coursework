import requests
import configparser
from datetime import datetime
from time import sleep
from tqdm import tqdm


config = configparser.ConfigParser()
config.read('settings.ini')


class VK:
    def __init__(self):
        self.token = config['VK']['token_vk']
        self.url = r'https://api.vk.com/method'
        self.id = self.get_info()['id']
        self.id_album = 'profile'
        self.name = self.get_info()['first_name']

    def get_info(self):
        params = {'access_token': self.token,
                  'v': '5.131'}
        method = '/account.getProfileInfo'
        final_url = self.url + method
        profile = requests.get(final_url, params)
        data = profile.json()
        return data['response']

    def get_photo(self):
        params = {
            'owner_id': self.id,
            'access_token': self.token,
            'album_id': self.id_album,
            'extended': '1',
            'count': input('Введите количество фото - '),
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


    # def download(self, url, name_file):
    #     res = requests.get(url)
    #     with open(name_file, 'wb') as file:
    #         file.write(res.content)

    def file_info(self):
        data_dict = self.get_photo()
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