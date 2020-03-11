# import sqlalchemy
# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base  # we need this to import base class
# engine = create_engine('mysql+mysqlconnector://root:Welcome_123@localhost:3306/sakila')
# connection = engine.connect()
# metadata = sqlalchemy.MetaData()
# actor = sqlalchemy.Table('actor', metadata, autoload=True, autoload_with=engine)

from api_call import avg_word_length, avg_tweet_length, avg_follower_num, hashtag_percentage, \
mention_percentage, common_words_in_data, longest_word_in_data, shortest_word_in_data, \
most_tweet_num_user, avg_tweet_num_per_user \

import mysql.connector
from mysql.connector import errorcode



import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

cnx = mysql.connector.connect (user='root', password='Welcome_123',
                               host='127.0.0.1',
                               database='twitter')
cursor = cnx.cursor()

# # Write a script that stores the data returned from the Twitter API in a SQL database.
# # Then read that data from your database and use the code you wrote previously to analyze it.
# # And finally, also write the results to the database.
# # create schema twitter;

TABLES = {}
TABLES['twitter_stats'] = (
    "CREATE TABLE `twitter_stats` ("
    "  `id` SMALLINT NOT NULL AUTO_INCREMENT,"
    "  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  `avg_word_length` int(100) NOT NULL,"
    "  `avg_tweet_length` int(100) NOT NULL,"
    "  `hashtag_percentage` varchar(100) NOT NULL,"
    "  `mention_percentage` varchar(100) NOT NULL,"
    "  `longest_word_in_data` varchar(100) NOT NULL,"
    "  `shortest_word_in_data` varchar(100) NOT NULL,"
    "  `most_tweet_num_user` varchar(100) NOT NULL,"
    "  `avg_tweet_num_per_user` int(20) NOT NULL,"

    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['top_words'] = (
    "CREATE TABLE `top_words` ("
    "  `id` SMALLINT NOT NULL AUTO_INCREMENT,"
    "  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  `word` varchar(1000) NOT NULL,"
    "  `count` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

def create_table(cursor):
    for table_name in TABLES:
        table_description = TABLES[table_name]
    try:
        print ("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


create_table(cursor)

add_tweet = ("INSERT INTO twitter_stats "
             " (avg_word_length, avg_tweet_length, hashtag_percentage, "
             " mention_percentage, longest_word_in_data, shortest_word_in_data, "
             " most_tweet_num_user, avg_tweet_num_per_user)"
             "VALUES (%(avg_word_length)s, %(avg_tweet_length)s, %(hashtag_percentage)s, "
             " %(mention_percentage)s, %(longest_word_in_data)s, %(shortest_word_in_data)s, "
             " %(most_tweet_num_user)s, %(avg_tweet_num_per_user)s);")
# Insert tweet info
data_tweets = {
        'avg_word_length': avg_word_length(),
        'avg_tweet_length': avg_tweet_length(),
        'hashtag_percentage': hashtag_percentage(),
        'mention_percentage': mention_percentage(),
        'longest_word_in_data': longest_word_in_data(),
        'shortest_word_in_data': shortest_word_in_data(),
        'most_tweet_num_user': f"{most_tweet_num_user()}",
        'avg_tweet_num_per_user': avg_tweet_num_per_user()
    }

add_word = ("INSERT INTO top_words (word, count) VALUES (%(word)s, %(count)s);")


def insert_into_twitter_stats():
    print ("inserting into table twitter_stats", end='')
    cursor.execute(add_tweet, data_tweets)
    # Make sure data is committed to the database

def insert_into_top_words():
    d = {}
    s = common_words_in_data()

    for word, count in s:
        d["word"] = (word)
        d["count"] = (count)
        cursor.execute (add_word, d)
    print("inserting into table top words", end='')

insert_into_twitter_stats()
insert_into_top_words()

cnx.commit()


# sql_select_Query = "delete from twitter_stats"

# sql_select_Query = "select * from actor"
# cursor.execute(sql_select_Query)
#
# for one in cursor:
#   print(one)
# cnx.commit()
# cursor.close()
# cnx.close()

sql_select_Query = "select * from top_words"
cursor.execute(sql_select_Query)
table_rows = cursor.fetchall()
# print(table_rows)
df = pd.DataFrame(table_rows)
# Start with one review:
text = df[2].to_list()
text = " ".join(text)
print(text)
# Create and generate a word cloud image:
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
#
# # Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# cursor.close()
# cnx.close()
