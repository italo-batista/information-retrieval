# # Pegando sentimento com TextBlob
from textblob import TextBlob

def get_polarity(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity < 0:
        return 'neg'
    else:
        return 'pos'

classificando_com_text_blob = tweets[['id', 'text']]

classificando_com_text_blob['sentiment'] = classificando_com_text_blob.text.apply(get_polarity)

num_negs = classificando_com_text_blob[classificando_com_text_blob["sentiment"] == "neg"].count()
num_poss = classificando_com_text_blob[classificando_com_text_blob["sentiment"] == "pos"].count()
print("Número de tweets negs:", num_negs)
print("Número de tweets posss:", num_negs)

classificando_com_text_blob.to_csv('tweets_labeled.csv')