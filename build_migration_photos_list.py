from __future__ import print_function
import flickr_api
import urllib
import pickle
import os
from pathlib import Path

my_photos = []

flickr_api.set_keys(api_key=os.environ['FLICKR_API_KEY'], api_secret=os.environ['FLICKR_API_SECRET'])

counter = 0
flickr_api.set_auth_handler((Path().parent / "auth/flickr_auth_handler").resolve().as_posix())
user = flickr_api.test.login()
#photosets = user.getPhotosets()

photo_set_walker = flickr_api.Walker(user.getPhotosets)
for photo_set in photo_set_walker:
    print(photo_set)
    photo_walker = flickr_api.Walker(photo_set.getPhotos)
    for photo in photo_walker:
        counter += 1
        print(f"{counter} {photo}")
        try:
            photo_url = photo.getPhotoFile("Original")
        except flickr_api.flickrerrors.FlickrServerError as e:
            print(f"Couldn't get original size URL {e}. Skipping")
            continue

        my_photos.append({"album": photo_set['title'],
                          "photoId": photo['id'],
                          "photoTitle": photo['title'],
                          "photoUrl": photo_url,
                          "processed": False})
        # photo_url = urllib.request.urlopen(photo.getPhotoFile("Original"))
        # image_bytes = BytesIO(photo_url.read())
        # Image.open(image_bytes).show()
        pass

with open((Path().parent / "photos_to_move.pickle").resolve(), "wb") as photo_tasks_file:
    pickle.dump(my_photos, photo_tasks_file)




