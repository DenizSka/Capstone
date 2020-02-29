# The average length of tweets (in characters)
# The longest word in a single tweet
# The average number of followers that users have
import json


# opening the json file and parsing it to a dictionary
with open('./data.json') as f:
    data = json.load(f)


def ave_tweet_length():
    tweet_counts = []
    for tweet in data:
        tweet_counts.append(len(tweet['text']))
    return f"this is average length of a tweet {sum(tweet_counts) / len(tweet_counts)}"


print(ave_tweet_length())


def longest_word_in_tweet(tweet):
    str_ = tweet['text'].split(' ')
    sum_ = 0
    for one in str_:
        if 'http' not in one:
            if sum_ < len(one):
                sum_ = len(one)
    return f"this is longest word in a given tweet {sum_}"


print(longest_word_in_tweet(data[0]))


def longest_word_in_data():
    longest_word = ''
    for one in data:
        list_text = one['text'].split(' ')
        for word in list_text:
            if 'http' not in word:
                if len(longest_word) < len(word):
                    longest_word = word
    return f"this is longest word {longest_word}"


print(longest_word_in_data())


def ave_follower_num():
    list_followers = []
    for one in data:
        list_followers.append(one['user']['followers_count'])
    return sum(list_followers) / len(list_followers)


print(ave_follower_num())
