from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests
import urllib
from io import BytesIO
from pathlib import Path

def authorize_with_google():
    # Setup the Photo v1 API
    SCOPES = 'https://www.googleapis.com/auth/photoslibrary https://www.googleapis.com/auth/photoslibrary.sharing'
    store = file.Storage((Path().parent / "auth/google_token.json").resolve().as_posix())
    creds = store.get()
    # creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets((Path().parent / "auth/google_credentials.json").resolve().as_posix(), SCOPES)
        creds = tools.run_flow(flow, store)

    return creds

def get_google_photos_service(google_creds):
    return build('photoslibrary', 'v1', http=google_creds.authorize(Http()))


def find_album_on_google(service, album_title):
    albums = service.albums()
    album_list_req = albums.list(pageSize=50, fields="nextPageToken,albums")

    while album_list_req is not None:
        album_list_resp = album_list_req.execute()

        album_list = album_list_resp.get('albums', [])
        for album in album_list:
            if album['title'] == album_title:
                return album['id']

        album_list_req = albums.list_next(album_list_req, album_list_resp)

    return None

def create_album_on_google(service, album_title):
    albums = service.albums()
    new_album = albums.create(body={"album": {"title": album_title}}).execute()
    return new_album.get("id", None)

def upload_photo_to_google(google_auth, service, album_id, photo_data, photo_title):
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
        payload = {"albumId": album_id,
                   "newMediaItems": [
                       {"description": "test",
                        "simpleMediaItem": {"uploadToken": upload_token}
                        }
                   ]}

        add_photo_req = media_items.batchCreate(body=payload)
        add_photo_resp = add_photo_req.execute()

        return add_photo_resp



def get_photo_from_flickr(photo_url):
    photo_url_obj = urllib.request.urlopen(photo_url)
    return BytesIO(photo_url_obj.read())


