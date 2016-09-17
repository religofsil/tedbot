import codecs, json, re
f=codecs.open('database.json', 'r', 'utf-8')
database=json.load(f)
f.close()
arr=[]
for entry in database:
    arr.extend(database[entry]["tags"])
arr=list(set(arr))
f=codecs.open('taglist.txt', 'w', 'utf-8')
for tag in arr:
    tag=tag.lower()
    tag=re.sub('^ ', '', tag)
    if tag!='':
        f.write(tag+'\n')
f.close()