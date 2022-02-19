import tweepy # tweepy module to interact with Twitter
import pandas as pd # Pandas library to create dataframes
from tweepy import OAuthHandler # Used for authentication
from tweepy import Cursor # Used to perform pagination
import sys

"""
Twitter Authentification Credentials
Please update with your own credentials
"""
cons_key = 'Ff23P2N0WBTzooJj8c0WGd3EA'
cons_secret = 'Pxp1PFy5egg7dUkyqPQjmhINX6mq6WYNjUGNSYMVcBWjcYhOH2'
acc_token = '1492059996183568384-xirWGMXDaJgCVgkC5X0UfIcSJLiufi'
acc_secret = 'ImgxsVOoDSt9ZtLOMWxVtaLD34lZAWcvHQfpanB0MgCJr'

number = 100 #quanti tweet vuoi che ti vengano stampati a video
nome = 'Fedez'
nome_parola = 'Ferragni' #inserire la prima lettera sempre in maiuscolo


# (1). Athentication Function
def get_twitter_auth():
    """
    @return:
        - the authentification to Twitter
    """
    try:
        consumer_key = cons_key
        consumer_secret = cons_secret
        access_token = acc_token
        access_secret = acc_secret

    except KeyError:
        sys.stderr.write("Twitter Environment Variable not Set\n")
        sys.exit(1)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    return auth


# (2). Client function to access the authentication API
def get_twitter_client():
    """
    @return:
        - the client to access the authentification API
    """
    auth = get_twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client


# (3). Function creating final dataframe
def get_tweets_from_user(twitter_user_name, page_limit=16, count_tweet=200):
    """
    @params:
        - twitter_user_name: the twitter username of a user (company, etc.)
        - page_limit: the total number of pages (max=16)
        - count_tweet: maximum number to be retrieved from a page

    @return
        - all the tweets from the user twitter_user_name
    """
    client = get_twitter_client()

    all_tweets = []

    for page in Cursor(client.user_timeline,
                       screen_name=twitter_user_name,
                       count=count_tweet).pages(page_limit):
        for tweet in page:
            parsed_tweet = {}
            parsed_tweet['date'] = tweet.created_at
            parsed_tweet['author'] = tweet.user.name
            parsed_tweet['twitter_name'] = tweet.user.screen_name
            parsed_tweet['text'] = tweet.text
            parsed_tweet['number_of_likes'] = tweet.favorite_count
            parsed_tweet['number_of_retweets'] = tweet.retweet_count

            all_tweets.append(parsed_tweet)

    # Create dataframe
    df = pd.DataFrame(all_tweets)

    # Revome duplicates if there are any
    df = df.drop_duplicates("text", keep='first')

    return df

googleAI = get_tweets_from_user(nome)
print("Data Shape: {}".format(googleAI.shape))
lista = []
biglista = []
for j in range(number):
    lista = []
    for key in googleAI.keys():
        lista.append(googleAI[key].iloc[j])
    biglista.append(lista[3])
    print(lista)
lista2 = []
conto = 0
for element in biglista:
    if nome_parola.lower() in element or nome_parola in element:
        conto += 1
        lista2.append(element)
print(conto)
if conto > 0:
    risposta = input('Sei interessato a vedere in quali tweet compare la parola da te indicata? ')
    if 's' in risposta:
        print(lista2)

