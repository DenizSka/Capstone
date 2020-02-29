import os
import tweepy
import json
import pprint

api_key = os.environ.get('MY_API_KEY')
secret_api = os.environ['MY_SECRET_API_KEY']
access_token = os.environ['ACCESS_TOKEN']
secret_access_token = os.environ['SECRET_ACCESS_TOKEN']

# pprint.pprint(dict(os.environ), width=1)

# authenticate to the service we're accessing
auth = tweepy.OAuthHandler(api_key, secret_api)
auth.set_access_token(access_token, secret_access_token)

api = tweepy.API(auth)
handle = 'twitter'  # for example purposes; prop any handle you want!

# For example, we can read our own timeline (i.e. our Twitter homepage) with:
public_tweets = api.home_timeline()
user = api.get_user(handle)

# you could just print out the JSON, one tweet per line:
# def process_or_store(tweet):
#     print(json.dumps(tweet))
#
#
# for tweet in public_tweets:
#     process_or_store(tweet.text)
#
# num_friends = user.friends_count

# pprint.pprint(dict(user._json), width=2)
# print(user.screen_name)
# print(user.followers_count)

# for friend in user.friends():
#     print(friend.screen_name)

# list of all tweets
# for tweet in tweepy.Cursor(api.user_timeline).items():
#     process_or_store(tweet._json)

# python_tweets = tweepy.Cursor(api.search,
#                               q="istanbul",
#                               lang="en",
#                               since=2020 - 1 - 30).items(2)

# lets live stream tweets:
# class MyStreamListener(tweepy.StreamListener):
#
#     def on_status(self, status):
#         print(status.text)
#
#     def on_error(self, status_code):
#         if status_code == 420:
#             # returning False in on_error disconnects the stream
#             return False


# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
#
# # Streams do not terminate unless the connection is closed, blocking the thread. Tweepy offers a convenient is_async
# # parameter on filter so the stream will run on a new thread.
# myStream.filter(locations=[-74,40,-73,41], is_async=True)
#
# print(myStream)

# ny_tweets = api.search(geocode="40.712772,-74.006058,600mi", granularity="country")


def dump_to_json(tweets):
    tweet_list = []
    for tweet in tweets:
        tweet_list.append(tweet._json)

    with open('api_tweet_data.json', 'w') as f:
        json.dump(tweet_list, f, indent=2)

    return tweet_list


# print(dump_to_json(ny_tweets))

tweet_stats_list = []


def get_one_user():
    # opening the json file and parsing it to a dictionary
    with open('api_tweet_data.json', 'r') as f:
        json_ = json.load(f)
        user = json_[0]["user"]
        text = json_[0]["text"]
        date = json_[0]["created_at"]
        return f"This is user '{user['name']}' and tweet '{text}' and the date '{date}'"


# print(get_one_user())


# The average length of tweets (counting words).
def ave_word_length():
    tweet_counts = []
    with open('api_tweet_data.json', 'r') as f:
        for tweet in json.load(f):
            list_text = tweet['text'].split(' ')
            tweet_counts.append(len(list_text))
        tweet_stats_list.append(f"this is average length of words in a tweet {sum(tweet_counts) / len(tweet_counts)} \n")
        # return f"this is average length of words in a tweet {sum(tweet_counts) / len(tweet_counts)}"


# The average length of tweets (counting characters).
def ave_tweet_length():
    tweet_counts = []
    with open('api_tweet_data.json', 'r') as f:
        for tweet in json.load(f):
            tweet_counts.append(len(tweet['text']))
        tweet_stats_list.append(f"this is average length of characters in tweet {sum(tweet_counts) / len(tweet_counts)} \n")
        # return f"this is average length of characters in tweet {sum(tweet_counts) / len(tweet_counts)}"


# The average number of followers.
def ave_follower_num():
    list_followers = []
    with open('api_tweet_data.json', 'r') as f:
        for one in json.load(f):
            list_followers.append(one['user']['followers_count'])
        tweet_stats_list.append(f"this is average follower number {sum(list_followers) / len(list_followers)} \n")
        # return f"this is average follower number {sum(list_followers) / len(list_followers)}"


# The percentage of tweets that have a hashtag (#).
def hashtag_percentage():
    tweet_count = 0
    tweets_with_hashtag = 0
    with open('api_tweet_data.json', 'r') as f:
        for one in json.load(f):
            tweet_count += 1
            if '#' in one['text']:
                tweets_with_hashtag += 1
        tweet_stats_list.append(f"percentage of hashtag {100 * tweets_with_hashtag / tweet_count} % \n")
        # return f"percentage of hashtag {100 * tweets_with_hashtag / tweet_count} %"


# The percentage of tweets that have a mention (@).
def mention_percentage():
    tweet_count = 0
    tweets_with_mentions = 0
    with open('api_tweet_data.json', 'r') as f:
        for one in json.load(f):
            tweet_count += 1
            if '@' in one['text']:
                tweets_with_mentions += 1
        tweet_stats_list.append(f"percentage of mentions {100 * tweets_with_mentions / tweet_count} % \n")
        # return f"percentage of mentions {100 * tweets_with_mentions / tweet_count} %"


# The 100 most common words.
def common_words_in_data():
    words = []
    top100 = {}
    # add all the words to a list
    # if any of the words already exist than add that new work as a dictionary with its number value
    with open('api_tweet_data.json', 'r') as f:
        for one in json.load(f):
            list_text = one['text'].split(' ')
            for word in list_text:
                if word not in words:
                    words.append(word)
                elif word in words:
                    top100[word] = list_text.count(word)
        sorted_dict = sorted(top100.items(), key=lambda x: x[1], reverse=True)
        tweet_stats_list.append(f"there are to used common words {sorted_dict}\n")
        # return f"there are to used common words {sorted_dict}"


# The 100 most common symbols.
def common_symbols_in_data():
    symbols = []
    letters = 'abcdefghijklmnopqrstuvwxyz'
    alphabet = list(letters)
    top100 = {}
    # list_letters = []
    # add all the words to a list
    # if any of the words already exist than add that new work as a dictionary with its number value
    with open('api_tweet_data.json', 'r') as f:
        for one in json.load(f):
            list_text = one['text'].split(' ')
            # print(list_text)
            for i in range(0, len(alphabet)):
                for word in list_text:
                    # print(word)
                    if alphabet[i] in list(word):
                        # print("z" in ["a","b"])
                        symbols.append(word)
                        # print(symbols)
                    # elif word in symbols:
                    #     top100[word] = list_text.count(word)
                # print(word)
                # for letter in word:
                #     list_letters.append(letter)
                #     if letter not in alphabet:
                #         symbols.append(letter)
                #     elif letter in symbols:
                #         top100[letter] = list_text.count(list_letters)
        # sorted_dict = sorted(top100.items(), key=lambda x: x[1], reverse=True)
        # return f"there are to used common symbols {sorted_dict}"


print(common_symbols_in_data())

# Percentage of tweets that use punctuation.


# The longest word in a tweet.
def longest_word_in_data():
    longest_word = ''
    with open('api_tweet_data.json', 'r') as f:
        for one in json.load(f):
            list_text = one['text'].split(' ')
            for word in list_text:
                if 'http' not in word and "@" not in word:
                    if len(longest_word) < len(word):
                        longest_word = word
        tweet_stats_list.append(f"this is longest word '{longest_word}' \n")
        # return f"this is longest word {longest_word}"


# Shortest word in a tweet.
def shortest_word_in_data():
    shortest_word = 'longestwordever'
    with open('api_tweet_data.json', 'r') as f:
        for one in json.load(f):
            list_text = one['text'].split(' ')
            for word in list_text:
                if 'http' not in word and "@" not in word:
                    if len(shortest_word) > len(word):
                        shortest_word = word
        tweet_stats_list.append(f"this is shortest word '{shortest_word}' \n")
        # return f"this is shortest word {shortest_word}"


# What user has the most tweets in the dataset?
def most_tweet_num_user():
    tweets_count = 0
    with open('api_tweet_data.json', 'r') as f:
        for one in json.load(f):
            if int(one['user']['statuses_count']) > tweets_count:
                tweets_count = int(one['user']['statuses_count'])
                user = one['user']["name"]
        tweet_stats_list.append(f"this is the user {user} with most tweets {tweets_count}\n")
        # return f"this is the user {user} with most tweets {tweets_count}"


# The average number of tweets from an individual user.
def ave_tweet_num():
    tweets_counts = []
    with open('api_tweet_data.json', 'r') as f:
        for one in json.load(f):
            tweets_counts.append(one['user']['statuses_count'])
        tweet_stats_list.append(f"this is average follower number {sum(tweets_counts) / len(tweets_counts)}\n")
        # return f"this is average follower number {sum(tweets_counts) / len(tweets_counts)}"


# The hour with the greatest number of tweets.
# Write your results to a new text file.

def write_to_file():
    ave_word_length()
    ave_tweet_length()
    ave_follower_num()
    hashtag_percentage()
    mention_percentage()
    common_words_in_data()
    longest_word_in_data()
    shortest_word_in_data()
    most_tweet_num_user()
    ave_tweet_num()
    with open("./tweet_stats.json", "w") as file_:
        for one in tweet_stats_list:
            file_.write(one)


write_to_file()
