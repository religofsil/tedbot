import codecs, json
f=codecs.open('database.tsv', 'r', 'utf-8')
d={}
id=1
for line in f:
    d[id]={}
    line=line.split('\t')
    d[id]['URL']=line[2]
    d[id]['speaker_name']=line[3]
    d[id]['headline']=line[4]
    d[id]['description']=line[5]
    d[id]['date given']=line[6]
    d[id]['event']=line[7]
    d[id]['duration']=line[8]
    d[id]['date published']=line[9]
    d[id]['tags']=line[10].split(',')
    id+=1
f.close()
f2=codecs.open('database.json', 'w', 'utf-8')
json.dump(d, f2, indent=2)
f2.close()