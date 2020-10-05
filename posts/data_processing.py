import re
import nltk
from nltk import Tree, FreqDist
from nltk.stem.porter import PorterStemmer
from nltk.corpus import treebank, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.chat import eliza_chat, rude_chat, suntsu_chat, zen_chat, iesha_chat
from string import punctuation



def validate_token(token):
    if re.fullmatch("[a-zA-Z]+", token):
        return True
    return False


def tokenize_words(sentence, valid_words=False):
    """
        Turn to lowercase all the word and then
        return a list of the tokenized words
    """
    valid_tokens = []
    for token in nltk.word_tokenize(sentence):
        if valid_words:
            if validate_token(token):
                valid_tokens.append(token)
        else:
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
        if validate_token(token):
            tags[token] = pos_tag
    return tags


def lemmatize_sentence(sentence_token):
    lemma = []
    word_lemmatizer = WordNetLemmatizer()
    for token in sentence_token:
        if validate_token(token):
            lemma.append({
                f"{token}": word_lemmatizer.lemmatize(token)
            })
    return lemma


def get_word_freequencies(sentence):
    return nltk.FreqDist(sentence)


def remove_stop_words(sentence):
    stop_words = stopwords.words("english")
    new_sentence = []
    for word in sentence.split():
        if word.lower() not in stop_words and word.lower() not in punctuation:
            new_sentence.append(word)
    return new_sentence


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