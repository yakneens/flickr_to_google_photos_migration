import json
from pathlib import Path
from shutil import move

results = []

p = Path.cwd() / "celery" / "results"
file_list = list(p.rglob("celery-task-meta-*"))

for cur_file in file_list:
    with open(cur_file) as fp:
        cur_res = json.load(fp)
        results.append(cur_res)

failed_tasks = [x['task_id'] for x in results if x['status'] == 'FAILURE']

task_list = []
p2 = Path.cwd() / "celery" / "processed"
file_list = list(p2.rglob("*.celery.msg"))
for cur_file in file_list:
    with open(cur_file) as fp:
        cur_res = json.load(fp)
        task_list.append((cur_file, cur_res))

failed_task_files = [x[0] for x in task_list if x[1]['headers']['id'] in failed_tasks]

for task_file in failed_task_files:
    move(task_file.as_posix(), (Path.cwd() / "celery" / "out").as_posix())
