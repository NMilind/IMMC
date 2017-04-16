import csv;
import os.path;
from geopy.geocoders import Nominatim;
from geopy.geocoders import GoogleV3;
from datetime import datetime;
from geopy.distance import vincenty;

time = datetime.strptime("Jan 1 2017", "%b %d %Y");

data = dict()

if not os.path.isfile("data/processed.zone.csv"):
    with  open("data/zone.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"');
        for row in reader:
            data[int(row[0])] = dict();
            data[int(row[0])]["Zone.ID"] = int(row[0])
            data[int(row[0])]["Zone.Abbr"] = row[1]
            data[int(row[0])]["Zone.Name"] = row[2]
            data[int(row[0])]["Address"] = row[2].split("/")[1] + ", " + row[2].split("/")[0];

    geolocator = Nominatim()
    googleAPI = GoogleV3(api_key="AIzaSyAUcTeRzAOEn5_Siu4YPvE1SPc0aVCgAGw");

    for key in data:
        print(data[key]);
        try:
            addr = data[key]["Address"];
            location = geolocator.geocode(addr);
            coordinates = (location.latitude, location.longitude);
            timezone = googleAPI.timezone(coordinates, at_time=time);
            date_at_location = datetime.now(timezone);
            dJ = date_at_location.utcoffset().total_seconds() / 60 / 60;

            data[key]["Latitude"] = location.latitude;
            data[key]["Longitude"] = location.longitude;
            data[key]["Offset"] = dJ;
        except:
            continue;


    with open("data/processed.zone.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key in data:
            try:
                writer.writerow([
                    data[key]["Zone.ID"],
                    data[key]["Zone.Abbr"],
                    data[key]["Zone.Name"],
                    data[key]["Address"],
                    data[key]["Latitude"],
                    data[key]["Longitude"],
                    data[key]["Offset"]
                ]);
            except:
                continue;

else:
    with  open("data/processed.zone.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"');
        for row in reader:
            data[int(row[0])] = dict();
            data[int(row[0])]["Zone.ID"] = int(row[0])
            data[int(row[0])]["Zone.Abbr"] = row[1]
            data[int(row[0])]["Zone.Name"] = row[2]
            data[int(row[0])]["Address"] = row[3]
            data[int(row[0])]["Latitude"] = float(row[4])
            data[int(row[0])]["Longitude"] = float(row[5])
            data[int(row[0])]["Offset"] = float(row[6])

#with open("data/processed.timezone.csv", newline='') as csvfile:
#    reader = csv.reader(csvfile, delimiter=',', quotechar='"');
#    for row in reader:
#        if (row[0] == "zone.id"):
#            continue;
#        timezone[row[4]] = list();
#with open("data/processed.timezone.csv", newline='') as csvfile:
#    reader = csv.reader(csvfile, delimiter=',', quotechar='"');
#    for row in reader:
#        if (row[0] == "zone.id"):
#            continue;
#        row_add = dict();
#        row_add["Zone.ID"] = int(row[0]);
#        row_add["Time.Standard"] = row[1];
#        row_add["GMT.Offset"] = int(row[2]) / 60 / 60;
#        row_add["DST"] = bool(row[3]);
#        timezone[row[4]].append(row_add);

print("Loaded Timezone Data");
