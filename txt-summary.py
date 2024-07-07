#Importing the libraries

import re 
import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest 

#creating a function that returns us the summarised document

def summary(input,per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(input)
    tokens=[token.text for token in doc]
    #creating a dictionary with the word and their frequencies
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS): #We are ignoring the stop words for this purpose, as we will calculate weight of every sentence, wrt to its importance
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency #Weighted frequencies of every word
        
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()] #Creating a sentence: weight score for every sentence
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary

st.title(':orange[Text Tummarization Using Transformer Algorithm] :notebook:')
st.write('By ESTHER IBNKUNOLUWA AWODOYIN 21D/47CS/01565, ABDULMUIZ ABDULGAFAR 20/47CS/01318, OLONADE AZEEZ LEKAN 21D/47CS/01543')
input = st.text_area('Enter text to summarize')
btn_enter_data = st.button("Summarize")
if(btn_enter_data):
    st.write(summary(input,0.5))
    
#We have the input, now we need to preprocess this data for it to make sense. \\
