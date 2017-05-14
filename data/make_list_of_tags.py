"""
Make a list of all tags in videos.
"""
import json, re

with open('database.json', 'r', encoding='utf-8') as f:
    database=json.load(f)

arr=[]
for entry in database:
    arr.extend(database[entry]["tags"])
arr=list(set(arr))

with open('taglist.txt', 'w', encoding='utf-8') as f:
    for tag in arr:
        tag=tag.lower()
        tag=re.sub('^ ', '', tag)
        if tag!='':
            f.write(tag+'\n')