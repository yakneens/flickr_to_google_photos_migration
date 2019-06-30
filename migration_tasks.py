from celery_migration_app import app
from migration_util import authorize_with_google, get_google_photos_service, \
    find_album_on_google, create_album_on_google, get_photo_from_flickr, \
    upload_photo_to_google


@app.task
def migrate_photo(photo_title, photo_url, album_title):
    google_creds = authorize_with_google()
    service = get_google_photos_service(google_creds)

    album_id = find_album_on_google(service, album_title)

    if album_id is None:
        album_id = create_album_on_google(service, album_title)

    photo_data = get_photo_from_flickr(photo_url)

    return upload_photo_to_google(google_creds, service, album_id, photo_data, photo_title)
