import csv
import math
import random

def calculate_distance(x1, y1, x2, y2): # This function calculates the distance between two points
    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def keyReturner(dictionary, current_x, current_y): # This function will take the current dictionary as input, the cu
    #rrent x and y position and returns the key of the dictionary where the distance is minimunm
    # It ensures that the related data are in a same cluster.# It also returns the key of the cluster so that
    # later the data will be in the same cluster

    min_distance = 100000000
    min_key = None
    flag = 0

    for key, values in dictionary.items():
        for sublist in values:
            x_position = sublist[0]
            y_position = sublist[1]
        distance = calculate_distance(x_position, current_x, y_position, current_y)
        if(distance<=2):
            if(distance<=min_distance):
                min_distance = distance
                min_key = key
                flag = 1

    if(flag ==0): # It means there are no clusters or keys where the distance between the points is less tha  or equal to 2
        return None
    else:
        return min_key # returning the key value so that later they will be in a same list

def func1(current_timestamp, data_dictionary):
    cluster_id = 0
    for ts in data_dictionary: # Iterating through all the rows in the dictionary where the data is kept accoring to timestamp
        rows = data_dictionary[ts]
        cluster_dictionary = {} # Creating the clusters withini that data where the key will be clkuster_id and values are the lists of the related data points

        for row in rows:
            x, y, sens_id, uniq_id = row[0], row[1], row[2], row[3]
            print(x, y)
            if (bool(cluster_dictionary)==False): # means an empty dictionary. Initially for the empty dictionary just adding the data point without claculating the distance
                    cluster_dictionary[cluster_id] = []
                    cluster_dictionary[cluster_id].append([x, y, sens_id])
                    cluster_id = cluster_id + 1

            else:
                key = keyReturner(cluster_dictionary, x, y) # returns the key where we should keep the value
                if(key is not None):
                    cluster_dictionary[key].append([x, y, sens_id])
                else:# means key is None, so create a new cluster
                    cluster_dictionary[cluster_id] = []
                    cluster_dictionary[cluster_id].append([x,y,sens_id])
                    cluster_id = cluster_id + 1

    writeToFile(cluster_dictionary, current_timestamp) # Now writing these values in the file


def create_csv_file(file_path):
    # Create a new CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['f_timestamp_id', 'f_id', 'cluster_data'])  # Write header row


def append_data_to_csv(file_path, f_timestamp_id, f_id,  cluster_data):

    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f_timestamp_id, f_id, cluster_data])

# Create a csv file
def writeToFile(cluster_dictionary, current_timeStamp):
    # Ready the row
    file_path = 'data.csv'
    #create_csv_file(file_path)
    for key,values in cluster_dictionary.items():
        append_data_to_csv(file_path, current_timeStamp, key, values)





filePath = 'D:\\Sentics\\test_Data.csv'
data_dictionary = {} #Dictionary with key as sensor_id and values as a lists that contains all the data belonging to a particular sensor id
current_timeStamp = None
flag = 0

with open(filePath, 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
        timeStamp = row[0]
        sensor_id = row[1]
        id = row[2]
        x_position, y_position = row[3], row[4]
        unique_id = row[5]

        dot_index = timeStamp.rfind('.')
        timeStamp = timeStamp[:dot_index+2] # We are just reading the timestamp data till . and extra one character so that we have enough data to cluster in one go

        #In the data_dictionary all the values are stored according the timestamp values.
        if(flag==0 or timeStamp== current_timeStamp): # It means that either it is the first timestamp or the current timestamp that we are clustering is the same
            if(flag==0): # For the starting row of first timestamp
                flag = 1
                current_timeStamp = timeStamp
                data_dictionary = {} # Creating a dictionary with key as current_timeStamp and values as the rows that has those timestamps
                data_dictionary[timeStamp] = []

            data_dictionary[timeStamp].append([x_position,y_position, sensor_id, unique_id])

        else: # completed for a single timestamp
            print("The dictionary values for every timestamp", current_timeStamp)
            print(data_dictionary)
            func1(current_timeStamp, data_dictionary) # finding the clusters for the data in the data_dictionary and the  writing to the file

            # The starting point for another timestamp
            current_timeStamp = timeStamp
            data_dictionary = {} # Creating a dictionary with key as current_timeStamp and values as the rows that has those timestamps
            data_dictionary[timeStamp] = []
            data_dictionary[timeStamp].append([x_position,y_position, sensor_id, unique_id])




















