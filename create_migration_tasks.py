from celery_migration_app import migrate_photo
import pickle
import os

for file in os.listdir("photosets/"):
    if file.endswith(".pickle"):

        with open(f"photosets/{file}", "rb") as photo_tasks_file:
            my_photos = pickle.load(photo_tasks_file)

        for photo in my_photos:
            migrate_photo.delay(
                photo['photoTitle'],
                photo['photoUrl'],
                photo['album'],
                photo['photoTags'] or photo['photoTitle'],
            )

