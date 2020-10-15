import re
import nltk
from nltk import Tree, FreqDist
from nltk.stem.porter import PorterStemmer
from nltk.corpus import treebank, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.chat import eliza_chat, rude_chat, suntsu_chat, zen_chat, iesha_chat
from string import punctuation
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import twitter_samples
import random




# Pattern validations
word_pattern = re.compile("\w+[']?\w+")
url_pattern = re.compile("(\w+://)?\w+\.(\w+\.?)+")


# List of raw tweets stored as corpus by nltk
tweets = twitter_samples.strings()


def validate_token(token):
    if word_pattern.fullmatch(token) and not url_pattern.fullmatch(token):
        return True
    return False


def tokenize_words(sentence):
    """
        Turn to lowercase all the word and then
        return a list of the tokenized words
    """
    valid_tokens = []
    for token in sentence.split():
        if validate_token(token):
            valid_tokens.append(token)
    return valid_tokens


def stem_sentence(sentence_token):
    """
        Receives as input a list of sentence tokens 
        and returns a dict with keys as words and
        items as stems
    """
    stemmer = PorterStemmer()
    sentence_stems = {}

    for token in sentence_token:
        if validate_token(token):
            sentence_stems[token] = stemmer.stem(token)

    return sentence_stems


def pos_tags_sentence(sentence_token):
    tags = {}
    for token, pos_tag in nltk.pos_tag(sentence_token):
        tags[token] = pos_tag
    return tags


def lemmatize_sentence(sentence_token):
    lemma = []
    word_lemmatizer = WordNetLemmatizer()
    for token in sentence_token:
        lemma.append({
            f"{token}": word_lemmatizer.lemmatize(token)
        })
    return lemma


def get_word_freequencies(sentence):
    return nltk.FreqDist(sentence)


def remove_stop_words(sentence):
    stop_words = stopwords.words("english")
    new_sentence = []
    for word in tokenize_words(sentence):
        if word not in stop_words and word not in punctuation:
            new_sentence.append(word)
    return new_sentence


def get_sentiment_score(sentence):
    analyser = SentimentIntensityAnalyzer()
    _, _, _, score = analyser.polarity_scores(sentence).values()
    if score >= 0.05:
        return 1
    elif score <= -0.05:
        return -1
    else:
        return 0



def chat_bot(name):
    bot = ""
    if name == "eliza":
        bot = nltk.chat.eliza.eliza_chatbot
    elif name == "iesha":
        bot = nltk.chat.iesha.iesha_chatbot
    elif name == "rude":
        bot = nltk.chat.rude.rude_chatbot
    elif name == "suntsu":
        bot = nltk.chat.suntsu.suntsu_chatbot
    elif name == "zen":
        bot = nltk.chat.zen.zen_chatbot
    return bot



def random_tweet():
    return random.choice(tweets)