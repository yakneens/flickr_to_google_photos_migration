import pickle
import os
import json


def load_urls():
    urls = []
    for file in os.listdir("celery/processed/"):
        if file.endswith(".msg"):
            with open(f"celery/processed/{file}") as celery_msg:
                message = json.load(celery_msg)
                url = message['headers']['argsrepr'].split(',')[1].replace(' ','').replace("'","")
                urls.append(url)

    return urls


def check_photoset(urls: list):
    found = 0
    not_found = 0
    for file in os.listdir("photosets-complete/"):
        if file.endswith(".pickle"):

            with open(f"photosets-complete/{file}", "rb") as photo_tasks_file:
                my_photos = pickle.load(photo_tasks_file)

            photo_url = my_photos[0]['photoUrl']
            if photo_url in urls:
                found += 1
            else:
                print(f"mv ./photosets-complete/{file} ./photosets/.")
                not_found += 1

    print(f"found: {found}")
    print(f"not found: {not_found}")


if __name__ == '__main__':
    urls = load_urls()
    check_photoset(urls)
