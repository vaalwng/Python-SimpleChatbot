# Author: Val Evander M. Wong (vmw170030) & Troi Megan Guichard (tmg180000)
# Assignment: Homework 07 - ChatBot
# Class: CS 4395.001
# Date: 11/14/2021

import nltk
import re
import random
import wikipedia as wp
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings('ignore')

# System Actions and Phrases
thank_you = ['thanks', 'thank you']
thank_you_resp = ['You are very welcome.', 'no problem.']
greeting = ['hey', 'hi', 'hello', 'nice to meet you,']
exit_cmd = ['exit', 'quit']

def process_kb(text):
    word_tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemma_list = []
    word_tokens = [w for w in word_tokens if w]

    for w, tag in nltk.pos_tag(word_tokens):
        lemma = lemmatizer.lemmatize(w)
        lemma_list.append(lemma)

    kb_file.close()
    out_file.close()

    return lemma_list


def generate_BotResponse(user_response):

    for w in user_response.split():
        if user_resp in greeting:
            return 'PokeBot: ' + random.choice(greeting).capitalize() + ' ' + name + '.'
        elif user_resp in thank_you:
            return 'PokeBot: ' + random.choice(thank_you_resp).capitalize() + ' ' + name + '.'
        else:
            tfidfvect = TfidfVectorizer(tokenizer=process_kb, stop_words='english')
            tfidf = tfidfvect.fit_transform(sent_tokens)
            cos_sim = cosine_similarity(tfidf[-1], tfidf)
            index = cos_sim.argsort()[0][-2]
            cos_sim_flat = cos_sim.flatten()
            cos_sim_flat.sort()
            req_tfidf = cos_sim_flat[-2]

            bot_response = ''
            if req_tfidf == 0:
                wiki_bool = input("It's not within my knowledge base. Would you like me to search it on Wikipedia?\n")
                if wiki_bool:
                    topic = input("Please enter the one word TOPIC of your question.\n")
                    wiki = wp.summary(topic, sentences=1)
                    return wiki
                else:
                    return
            else:
                bot_response = bot_response + sent_tokens[index]
                return bot_response


# main
if __name__ == '__main__':

    print('Greetings! I am PokeBot. A chatbot with information regarding the wonderful world of Pokemon.\n')

    # get user's name
    name = input('What is your name, user? \n').lower()
    if(name.lower() in exit_cmd):
        exit(0)

    name = name.capitalize()

    print("\nHello " + name + ", what would you like to talk about?")

    kb_file = open('pokekb_raw.txt', 'r', errors='ignore')
    raw_text = kb_file.read().lower()

    processed_text1 = re.sub(r'[\[\]<>{}?!,:;()_\-\n\d]', ' ', raw_text.lower())
    sent_tokens = sent_tokenize(processed_text1)
    word_tokens = word_tokenize(processed_text1)
    out_file = open('pokekb.txt', 'w')
    for line in sent_tokens:
        out_file.write('{}\n'.format(line))


    # create a file for each unique user and log the history
    user_file1 = open(name + '_chat_log.txt', 'w+')
    user_file2 = open(name + '_personal_log.txt', 'w+')

    user_file1.write('User: ' + name + '\n')

    # open processed knowledge base
    kb_file = open('pokekb.txt', 'r')
    kb = kb_file.read()

    # conversation Loop
    cont_conv = True

    while cont_conv:

        gen_resp = True

        user_resp = input().lower()

        for w in user_resp.split():
            if w in ['like', 'dislike', 'favorite', 'hate']:
                user_file2.write(user_resp + '\n')
                gen_resp = False
                break

        user_file1.write(user_resp + '\n')

        lines = user_file1.readlines()
        line_list = []
        for l in lines:
            print(l)
            line_list.append(l)

        if user_resp in exit_cmd:
            print('PokeBot: Good Bye, ' + name + '. Thanks for chatting!')
            cont_conv = False
            break

        sent_tokens.append(user_resp)
        word_tokens = word_tokens + nltk.word_tokenize(user_resp)
        final_words = list(set(word_tokens))
        if gen_resp is True:
            print(generate_BotResponse(user_resp), '\n')
        sent_tokens.remove(user_resp)

        print('PokeBot: How may I help you today?')
        # print('PokeBot: Would you like to know more about \'', random.choice(line_list))

    print('Terminating. . .')
    user_file1.close()
    user_file2.close()
    exit(0)