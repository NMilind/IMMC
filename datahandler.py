import csv;

timezone = dict();

with open("data/processed.timezone.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"');
    for row in reader:
        if (row[0] == "zone.id"):
            continue;
        timezone[row[4]] = dict();
        timezone[row[4]]["Zone.ID"] = row[0];
        timezone[row[4]]["Time.Standard"] = row[1];
        timezone[row[4]]["GMT.Offset"] = row[2];
        timezone[row[4]]["DST"] = row[3];

print("Loaded Timezone Data");
