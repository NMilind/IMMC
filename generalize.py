from datahandler import data as tzd;
from datahandler import time;
from geopy.geocoders import Nominatim;
from geopy.geocoders import GoogleV3;
from datetime import datetime;
from geopy.distance import vincenty;
import math;
import operator;
import random;
import csv;

C_EARTH = 24901;

members = {
    0: { "Address": "Boston, Massachusetts, United States of America" },
    1: { "Address": "Singapore, Republic of Singapore" },
    2: { "Address": "Beijing, China" },
    3: { "Address": "Hong Kong, China" },
    4: { "Address": "Moscow, Russia" },
    5: { "Address": "Utrecht, Netherlands" },
    6: { "Address": "Warsaw, Poland" },
    7: { "Address": "Copenhagen, Denmark" },
    8: { "Address": "Melbourne, Australia" }
};

members = {
    0: { "Address": "Monterey, California, United States" },
    1: { "Address": "Zutphen, Netherlands" },
    2: { "Address": "Melbourne, Australia" },
    3: { "Address": "Shanghai, China" },
    4: { "Address": "Hong Kong, China" },
    5: { "Address": "Moscow, Russia" }
};

histogram_data = dict();

def generate(members):

    locations = dict();
    rank_locations = dict();

    geolocator = Nominatim()
    googleAPI = GoogleV3(api_key="AIzaSyAUcTeRzAOEn5_Siu4YPvE1SPc0aVCgAGw");

    for key in members:
        location = geolocator.geocode(members[key]["Address"]);
        coordinates = (location.latitude, location.longitude);
        timezone = googleAPI.timezone(coordinates, at_time=time);
        date_at_location = datetime.now(timezone);
        utc = date_at_location.utcoffset().total_seconds() / 60 / 60;
        members[key]["Latitude"] = location.latitude;
        members[key]["Longitude"] = location.longitude;
        members[key]["Offset"] = utc;

    for key in tzd:
        conf_coordinates = (float(tzd[key]["Latitude"]), float(tzd[key]["Longitude"]));
        pSum = 0;
        dSum = 0;
        travelCost = 0;
        for mem_key in members:
            coordinates = (float(members[mem_key]["Latitude"]), float(members[mem_key]["Longitude"]));
            distance = vincenty(coordinates, conf_coordinates).miles;
            dJ = members[mem_key]["Offset"] - tzd[key]["Offset"];

            P = min(10, 10 + (6 * math.cos((math.pi * dJ / 12) - (math.pi / 24))));
            pSum += math.pow(P, 2);

            dSum += math.pow(distance, 2);

            travelCost += distance * 0.11 + 50;

        D = (C_EARTH * math.sqrt(len(members))) / (2 * math.sqrt(dSum));
        J = math.sqrt((1 / len(members)) * pSum);
        L = 450 * len(members);
        M = travelCost + L;
        K = J * D;

        locations[tzd[key]["Zone.Name"]] = [K, M];
        rank_locations[tzd[key]["Zone.Name"]] = M / K;

    ranked = sorted(rank_locations.items(), key=operator.itemgetter(1));
    for k in range(len(ranked)):
        histogram_data[ranked[k][0]] += k + 1;

if __name__ == "__main__":
    for key in tzd:
        histogram_data[tzd[key]["Zone.Name"]] = 0;

    iters = 350;
    i = 0;
    while i < iters:
        try:
            members = dict();
            for k in range(10):
                id = random.randint(0, 281);
                members[k] = dict();
                members[k]["Address"] = list(tzd.values())[id]["Address"]
            generate(members);
            i += 1;
            print(i);
        except:
            continue;

    with open("data/histogram.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key in histogram_data:
            writer.writerow([key, histogram_data[key]]);
