import markovify
import json

# Get raw text as string.
with open("api_tweet_data.json") as f:
    tweets = []
    for tweet in json.load(f):
        tweets.append(tweet['text'])
    # text = f.read()
print(tweets)
# Build the model.
text_model = markovify.Text(tweets)

# Print five randomly-generated sentences
for i in range(1):
    print(text_model.make_sentence())
