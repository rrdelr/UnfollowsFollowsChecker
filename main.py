import time
import datetime
import tweepy
import csv
import sys
import os

# Authenticate to twitter
auth = tweepy.OAuthHandler('###', '###')
auth.set_access_token('###', '###')

def get_followers(user_name):
    api = tweepy.API(auth)
    followers = []
    for page in tweepy.Cursor(api.followers, screen_name=user_name, wait_on_rate_limit=True,count=200).pages():
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return followers


def save_followers_to_csv(user_name, data):
    with open("./data/" + user_name + "_followers.csv", 'w+',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        for profile_data in data:
            profile = []
            profile.append(profile_data._json["screen_name"])
            csv_writer.writerow(profile)


def get_followers_list_file(user_name):
    with open("./data/" + user_name + "_followers.csv", 'r+' ,encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        data = list(filter(None, data))
        # data = tuple(data)

    flattened = []
    for sublist in data:
        for val in sublist:
            flattened.append(val)
    # print(flattened)
    return flattened


def listToString(list):
    # initialize an empty string
    string = ""

    # traverse in the string
    for ele in list:
        string += ele
        string += ' '
        # return string
    return string

if __name__ == '__main__':
    user = str(sys.argv[1])
    prev = 0
    #
    if os.path.isfile("./data/" + user + "_followers.csv"):
        print('file exists')
        oldData = get_followers_list_file(user)
        prev = 1

    followers = get_followers(user)
    save_followers_to_csv(user, followers)

    if prev == 1:
        newData = get_followers_list_file(user)
        s = set(newData)
        u = set(oldData)

        diffData = [x for x in oldData if x not in s]
        diffData = listToString(diffData)

        diffDataN = [x for x in newData if x not in u]
        diffDataN = listToString(diffDataN)

        print(diffData)

        f = open("./data/" + user + "_log.txt", "a+")
        datetime_object = str(datetime.datetime.now())
        f.write("[" + datetime_object + "] \n")
        f.write("unfollowed: \n")
        f.write(diffData + "\n")
        f.write("followed: \n")
        f.write(diffDataN + "\n")
        f.write("\n")
        f.close()

