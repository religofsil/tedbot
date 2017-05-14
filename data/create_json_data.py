import json

with open('database.tsv', 'r', encoding='utf-8') as f:
    d = {}
    talk_id = 1
    for line in f.readlines()[1:]:
        line = line.split('\t')
        d[talk_id] = {}
        d[talk_id]['URL'] = line[1]
        d[talk_id]['speaker_name'] = line[2]
        d[talk_id]['headline'] = line[3]
        d[talk_id]['description'] = line[4]
        d[talk_id]['event'] = line[5]
        d[talk_id]['duration'] = line[6]
        d[talk_id]['primary_language'] = line[7]
        d[talk_id]['published'] = line[8]
        d[talk_id]['tags'] = line[9].rstrip().split(',')
        talk_id += 1

with open('database.json', 'w', encoding='utf-8') as f2:
    json.dump(d, f2, indent=2)

