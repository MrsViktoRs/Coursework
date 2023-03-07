import VK
import Yandex
import json


def write_json(data):
    with open('all_photos_info', 'w') as file:
        json.dump(data, file, indent=2)


def uploading_saved():
    data_photo = []
    for x in user.file_info():
        upload.upload_file(x['url'], x['name_file'])
        data_photo.append({'file_name': x['name_file'], 'size': x['size']})
        write_json(data_photo)
    return


if __name__ == '__main__':
    user = VK.VK()
    upload = Yandex.Yandex()
    uploading_saved()
