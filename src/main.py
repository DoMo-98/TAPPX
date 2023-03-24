# !python -m spacy download es_core_news_md
# !pip install nltk
# !pip install rake_nltk

from rake_nltk import Rake
import nltk
import string
import re
import json
import pandas as pd
import heapq
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

retdict = dict()

def remove_jinja2_tags(text, max_length):
    pattern = re.compile(r'\{\{.*?\}\}')
    
    for match in pattern.findall(text):
        if len(match) < max_length:
            text = text.replace(match, '')
    
    return text

def clean_text(text: str, nlp) -> str:
    """
    Clean the text
    """
    text_cleaned = remove_jinja2_tags(text, 40)
    text_cleaned = "".join([char if char not in string.punctuation and char != "-" else " " \
                            for char in text_cleaned])
    text_cleaned = re.sub(r'(?<!\w)-(?!\w)', ' ', text_cleaned)
    text_cleaned = re.sub(r'\b-\B|\B-\b', ' ', text_cleaned)
    text_cleaned: str = re.sub("\s+"," ", text_cleaned)

    doc = nlp(text_cleaned.lower())
    tokens = [token for token in doc if not token.is_stop and not token.is_space and not token.like_num]
    tokens = [token.lemma_ for token in tokens]

    return ' '.join(tokens)

def temp_comp(text1, text2, vectorizer):
  tfidf = vectorizer.fit_transform([text1, text2])
  cosine_similarities = cosine_similarity(tfidf[0:1], tfidf)

  return cosine_similarities[0][1]

def get_keywords2(text, nlp):
  rake_nltk_var = Rake()
  rake_nltk_var.extract_keywords_from_text(text)

  sorted_items = sorted(rake_nltk_var.get_word_degrees().items(), key=lambda x: x[1], reverse=True)
  size = len(sorted_items)
  size = size - 1 if size < 5 else size**(2/3)
  top_n_keys = [k for k, v in sorted_items[:int(size)]]

  return top_n_keys

def compare_topics(elem1, elem2):
  temp = 1
  for it1 in elem1:
    for it2 in elem2:
      if it2["class"] == it1["class"] and it2["class"] != "Uncategorized":
        temp *= 1.2
  return temp

def build_res(df_articles, df_videos):
  for article in df_articles.index:
    retdict[article] = {}
    for video in df_videos.index:
      retdict[article][video] = {"score" : 0}

def print_res():
  for article, i in retdict.items():
    print(article)
    for video, j in sorted(i.items(), key=lambda x: x[1]["score"], reverse=True):
      print("   ", video, ":", j)

def clean_res():
  for article, i in retdict.items():
    retdict[article] = {elem[0]: elem[1] for elem in sorted(i.items(), key=lambda x: x[1]["score"], reverse=True)[:3]}
    

def main():
    """
    Entry point of the program
    """
    nltk.download('stopwords')
    nltk.download('punkt')
    nlp = spacy.load('es_core_news_md')
    vectorizer = TfidfVectorizer()


    df_articles: pd.DataFrame = pd.read_json('articles.json', orient='index')
    df_videos: pd.DataFrame = pd.read_json('videos.json', orient='index')
    build_res(df_articles, df_videos)

    for i, elem in enumerate(df_articles['text']):
      df_articles['text'][i] = clean_text(elem, nlp)
    for i, elem in enumerate(df_videos['text']):
      df_videos['text'][i] = clean_text(elem, nlp)

    for i, elem in enumerate(df_articles['text']):
      kwords1 = get_keywords2(df_articles['text'][i], nlp)
      for j, elem2 in enumerate(df_videos['text']):
        kwords2 = get_keywords2(df_videos['text'][j], nlp)
        value = 1 * compare_topics(df_articles['categoriaIAB'][i], df_videos['categoriaIAB'][j])
        comp_val = temp_comp(elem, elem2, vectorizer) * value
        comp_val2 = temp_comp(' '.join(kwords1), elem2, vectorizer) * value
        comp_val3 = temp_comp(' '.join(kwords2), elem, vectorizer) * value
        
        retdict[df_articles['text'].index[i]][df_videos['text'].index[j]]["score"] = 0.4 * comp_val + 0.3 * comp_val2 + 0.3 * comp_val3
    clean_res()
    with open("tappx.json", "w") as write_file:
      json.dump(retdict, write_file, indent=4)
if __name__ == "__main__":
    main()