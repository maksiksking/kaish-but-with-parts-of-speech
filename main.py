import json
import csv

# Oh, look, Maksiks writing comments as if anyone ever is gonna read this. What an idiot.

# Opening the JMdict data json yoinked from https://github.com/scriptin/jmdict-simplified cause XML is ... DON'T
with open('jmdict-eng-3.6.1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Opening the kanji (and readings) taken from the .tsv (.csv) by exporting the .txt of the deck into google sheets
with open('readings-kanji.csv', 'r', newline='', encoding='utf-8') as rtxt:
    readings = list(csv.reader(rtxt, delimiter=' '))

# Opening the file this all wll go into
ft = open('txt.csv', 'w', newline='', encoding='utf-8')
ftxt = csv.writer(ft)

# Checking if the data works, I'd rather not remove this, to know if it does
if isinstance(data, dict):
    print(data.keys())

# Here is some more debug
# entries_1 = data['words'][:60]
#
# entries_2 = entries_1[0]['sense'][0]['partOfSpeech']
# print(json.dumps(entries_1, indent=2))

# The juice. Get words from data as a list.
for entry in data["words"]:
    # if exists
    if "sense" in entry and isinstance(entry["sense"], list) and entry["sense"]:
        # If has kanji then word = kanji, else kana or if kana is more common it's also kana
        if entry["kanji"] and "uk" not in entry["sense"][0]["misc"]:
            word = entry["kanji"][0]["text"]
        else:
            word = entry["kana"][0]["text"]

        # The actual part of speech is gotten here, N/A if else (there are no N/A's in the Kaishi words at least)
        part_of_speech = entry["sense"][0].get("partOfSpeech", "N/A")

        # The things that checks every word if it matches with Kaishi
        for reading in readings:
            if word==reading[0]:
                # And this adds it to the file
                ft.write(word + "," + ' '.join(part_of_speech) + '\n')

# Close the file to prevent nuclear explosion.
ft.close()

# Now open the same file but only for reading
with open('txt.csv', 'r', newline='', encoding='utf-8') as ftcsv:
    # Checks the final data for duplicates, JMdict may have some,
    # I might have fixed that by checking for kanji already but idk
    # I kept the code for safety anyways
    print(ftcsv.read())
    # Puts pointer at the start, super important
    ftcsv.seek(0)
    ftxtreader = csv.reader(ftcsv, delimiter=',')
    rows = list(ftxtreader)
    unique = set(tuple(row) for row in rows)
    print(unique)

# Yada yada opens for writing
fta = open('txt.csv', 'w', newline='', encoding='utf-8')
fta.seek(0)
ftxta = csv.writer(fta)

# Prints it so we can see it and finally writes it to the final dataset.
for entry in unique:
    print(entry)
    ftxta.writerow(entry)

# The end. Rate the movie from 1 to 10, I'm waiting.
fta.close()