from celery_migration_app import migrate_photo
import pickle
from pathlib import Path

with open((Path.cwd() / "photos_to_move.pickle").resolve(), "rb") as photo_tasks_file:
    my_photos = pickle.load(photo_tasks_file)

for photo in my_photos:
    migrate_photo.delay(photo['photoTitle'], photo['photoUrl'],photo['album'])

