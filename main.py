import json
import csv

with open('jmdict-eng-3.6.1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('readings-kanji.csv', 'r', newline='', encoding='utf-8') as rtxt:
    readings = list(csv.reader(rtxt, delimiter=' '))

ft = open('txt.csv', 'w', newline='', encoding='utf-8')
ftxt = csv.writer(ft)

if isinstance(data, dict):
    print(data.keys())


entries_1 = data['words'][:6]

entries_2 = entries_1[0]['sense'][0]['partOfSpeech']
# print(json.dumps(entries_1, indent=2)) a a a


for entry in data["words"]:
    if "sense" in entry and isinstance(entry["sense"], list) and entry["sense"]:
        if entry["kanji"]:
            word = entry["kanji"][0]["text"]
        else:
            word = entry["kana"][0]["text"]
        part_of_speech = entry["sense"][0].get("partOfSpeech", "N/A")
        for reading in readings:
            if word==reading[0]:
                # print(word, part_of_speech)
                ft.write(word + "," + ' '.join(part_of_speech) + '\n')

ft.close()

with open('txt.csv', 'r', newline='', encoding='utf-8') as ftcsv:
    print(ftcsv.read())
    ftcsv.seek(0)
    ftxtreader = csv.reader(ftcsv, delimiter=',')
    rows = list(ftxtreader)
    unique = set(tuple(row) for row in rows)
    print(unique)

fta = open('txt.csv', 'w', newline='', encoding='utf-8')
fta.seek(0)
ftxta = csv.writer(fta)

for entry in unique:
    print(entry)
    ftxta.writerow(entry)

fta.close()