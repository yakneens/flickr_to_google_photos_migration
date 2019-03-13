import json
from pathlib import Path
import pandas as pd
import pickle

results = []

p = Path.cwd() / "celery" / "results"
file_list = list(p.rglob("celery-task-meta-*"))

for cur_file in file_list:
    with open(cur_file) as fp:
        cur_res = json.load(fp)
        results.append(cur_res)

results_df = pd.DataFrame(results)
print(f"{results_df['status'].value_counts()}")

#Print failed task ids and error messages
# failed_results_df = results_df[results_df.status == 'FAILURE']
# print("Failed tasks")
# for x in map(lambda x: (x[1], x[0]['exc_message'][1]), failed_results_df[['result','task_id']].values):
#     print(x)

#Get photos that succeeded uploads
# with open((Path.cwd() / "photos_to_move.pickle").resolve(), "rb") as photo_tasks_file:
#     my_photos = pickle.load(photo_tasks_file)
#
# successes = [x['result']['newMediaItemResults'][0]['mediaItem']['filename'] for x in results if x['status'] == 'SUCCESS']
# in_successes = [x for x in my_photos if x['photoTitle'] in successes]
