from __future__ import print_function
import flickr_api
import pickle
import os
from pathlib import Path
import redis

r = redis.Redis(host='0.0.0.0', port=6379, db=0, decode_responses=True)
flickr_api.set_keys(api_key=os.environ['FLICKR_API_KEY'], api_secret=os.environ['FLICKR_API_SECRET'])

photoset_counter = 0
flickr_api.set_auth_handler((Path.cwd() / "auth" / "flickr_auth_handler").resolve().as_posix())
user = flickr_api.test.login()

photo_set_walker = flickr_api.Walker(user.getPhotosets)
for photo_set in photo_set_walker:
    my_photos = []

    print(f"photoset: {photo_set} {photoset_counter}")

    if r.get(photo_set['id']) is None:
        counter = 0

        photo_walker = flickr_api.Walker(photo_set.getPhotos)
        for photo in photo_walker:
            counter += 1
            print(f"{counter} {photo}")
            try:
                photo_url = photo.getPhotoFile("Original")
            except flickr_api.flickrerrors.FlickrServerError as e:
                print(f"Couldn't get original size URL {e}. Skipping")
                continue
            except flickr_api.flickrerrors.FlickrError as e:
                print(f"Couldn't get original size URL {e}. Skipping")
                continue

            my_photos.append({
                "album": photo_set['title'],
                "photoId": photo['id'],
                "photoTitle": photo['title'],
                "photoUrl": photo_url,
                "processed": False,
                "photoTags": ','.join([t['text'] for t in photo.getTags()]),
            })

        print(f"writing photoset {photoset_counter}")
        with open((Path.cwd() / f"photosets-queue/photoset-{photo_set['id']}-{counter}.pickle").resolve(), "wb") as photo_tasks_file:
            pickle.dump(my_photos, photo_tasks_file)

        r.set(photo_set['id'], len(my_photos))

    photoset_counter += 1



