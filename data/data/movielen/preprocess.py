from email import header
import time
import os
import pandas as pd
from requests import head



def load_data(fileName):

    data = pd.read_csv(fileName, header=0,
                               sep=",").fillna(0)
    headers = data.columns.values.tolist()
    data = data.to_numpy().tolist()
    return headers,data


def getTime(timestamp):
    #转换成localtime
    time_local = time.localtime(timestamp)
    #转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt.split(" ")[0]


def gen_movies_table(headers,data):
    f = open("movies_table.csv","w")
    f.write(headers[0]+","+headers[1]+"\n")
    for item in data:
        f.write(str(item[0])+","+str(item[1]).replace(","," ")+"\n")
    f.close()


def gen_movieGenres_table(headers,data):
    f = open("movieGenres.csv","w")
    f.write(headers[0]+","+headers[2]+"\n")
    for item in data:
        for v in item[2].split("|"):
            f.write(str(item[0])+","+v+"\n")
    f.close()

def gen_ratings_table(headers,data):
    f = open("ratings_table.csv","w")
    f.write(",".join(list(map(str,headers))))
    for item in data:
        f.write(str(item[0])+","+str(item[1])+","+str(item[2])+","+getTime(float(item[3]))+"\n")
    f.close()


def gen_tags_table(headers,data):
    f = open("tags_table.csv", "w")
    f.write(",".join(list(map(str, headers))))
    for item in data:
        f.write(str(item[0])+","+str(item[1])+"," +
                str(item[2])+","+getTime(float(item[3]))+"\n")
    f.close()

if __name__ == '__main__':
    headers,data = load_data("movies.csv")
    gen_movies_table(headers,data)
    # gen_movieGenres_table(headers,data)
    # gen_ratings_table(headers,data)


