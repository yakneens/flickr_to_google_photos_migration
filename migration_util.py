from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests
import urllib
from io import BytesIO
from pathlib import Path
import redis

r = redis.Redis(host='0.0.0.0', port=6379, db=0, decode_responses=True)


def authorize_with_google():
    store = file.Storage((Path().parent / "auth/google_token.json").resolve().as_posix())
    return store.get()


def get_google_photos_service(google_creds):
    return build('photoslibrary', 'v1',
                 http=google_creds.authorize(Http()),
                 cache_discovery=False)


def find_album_on_google(album_title):
    return r.get(album_title)


def build_album_cache(service):
    albums = service.albums()
    album_list_req = albums.list(pageSize=50, fields="nextPageToken,albums")
    while album_list_req is not None:
        album_list_resp = album_list_req.execute()
        album_list = album_list_resp.get('albums', [])
        for album in album_list:
            if r.get(album['title']) is None:
                r.set(album['title'], album['id'])

        album_list_req = albums.list_next(album_list_req, album_list_resp)


def create_album_on_google(service, album_title):
    albums = service.albums()
    new_album = albums.create(body={"album": {"title": album_title}}).execute()
    r.set(album_title, new_album.get('id', None))
    return new_album.get("id", None)


def upload_photo_to_google(google_auth, service, album_id, photo_data,
                           photo_title, photo_tags):
    media_items = service.mediaItems()

    url = 'https://photoslibrary.googleapis.com/v1/uploads'
    authorization = 'Bearer ' + google_auth.access_token
    headers = {
        "Authorization": authorization,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': photo_title,
        'X-Goog-Upload-Protocol': 'raw',
    }

    upload_response = requests.post(url, headers=headers, data=photo_data)
    upload_token = upload_response.text

    if upload_token is not None:
        payload = {
            "albumId": album_id,
            "newMediaItems": [{
                "description": photo_tags,
                "simpleMediaItem": {
                    "uploadToken": upload_token
                }
            }]
        }

        add_photo_req = media_items.batchCreate(body=payload)
        add_photo_resp = add_photo_req.execute()

        return add_photo_resp


def get_photo_from_flickr(photo_url):
    photo_url_obj = urllib.request.urlopen(photo_url)
    return BytesIO(photo_url_obj.read())


if __name__ == '__main__':
    creds = authorize_with_google()
    service = get_google_photos_service(creds)
    build_album_cache(service)
