import redis
from migration_util import authorize_with_google, get_google_photos_service


r = redis.Redis(host='0.0.0.0', port=6379, db=0, decode_responses=True)


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


if __name__ == '__main__':
    creds = authorize_with_google()
    service = get_google_photos_service(creds)
    build_album_cache(service)
