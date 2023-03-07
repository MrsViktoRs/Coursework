import requests
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')


class Yandex:
    def __init__(self):
        self.token = config['Yandex']['token_yandex']
        self.url = r'https://cloud-api.yandex.net'
        self.name_folder = input('Введите имя папки в которую будут загруженны фото - ')

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
