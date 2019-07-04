import json
from pathlib import Path
from shutil import move

results = []

# find errant messages

p = Path.cwd() / "celery" / "results"
file_list = list(p.rglob("celery-task-meta-*"))

for cur_file in file_list:
    with open(cur_file) as fp:
        cur_res = json.load(fp)
        results.append({
            "meta": cur_res,
            "filename": cur_file
        })

failed_tasks = [x["meta"]['task_id'] for x in results if x["meta"]['status'] == 'FAILURE']
print(f"found {len(failed_tasks)} failed tasks")

if len(failed_tasks) == 0:
    exit(0)

# put messages back

print("putting failed messages back")

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

# remove errant messages

failed_files = [x["filename"] for x in results if x["meta"]['status'] == 'FAILURE']
print(f"removing {len(failed_files)} failed messages from celery/results")

for file in failed_files:
    file.unlink()
