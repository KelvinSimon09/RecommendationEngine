import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('books.csv')

df.head() # Let's take a look at our programming books dataset

# Text preprocessing

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('english')

# Set of stopwords to remove
stop = set(stop)

# Set of punctuation signs to remove
from string import punctuation


#small set of functions for text preprocessing:

import re

def lower(text):
    return text.lower()

def remove_punctuation(text):
    return text.translate(str.maketrans('','', punctuation))

def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in stop])

# Removing all words with digits and standalone digits
def remove_digits(text):
    return re.sub(r'\d+', '', text)

# One function to clean it all
def clean_text(text):
    text = lower(text)
    text = remove_punctuation(text)
    text = remove_stopwords(text)
    text = remove_digits(text)
    return text

# we'll create new columns with cleaned "Book_title" and "Description" texts:
df['clean_Book_title']=df['Book_title'].apply(clean_text)
df.head()

df['clean_Description']=df['Description'].apply(clean_text)
df.head()

#  Now, we need to transform text from "Book_title" to vectors array:
# Initializing vectorizer
vectorizer = TfidfVectorizer(analyzer='word', lowercase=False)
# Applying vectorized to clean text
X = vectorizer.fit_transform(df['clean_Book_title'])

# Getting array with vectorized titles
title_vectors = X.toarray()
title_vectors

# Let's do the same with "Description" column:
desc_vectorizer = TfidfVectorizer(analyzer='word', lowercase=False)
Y = desc_vectorizer.fit_transform(df['clean_Description'])
desc_vectors = Y.toarray()
desc_vectors

# Recommendation system
def get_recommendations(value_of_element, feature_locate, df, vectors_array, feature_show):
    """Returns DataFrame with particular feature of target and the same feature of five objects similar to it.

    value_of_element     - unique value of target object
    feature_locate       - name of the feature which this unique value belongs to
    df                   - DataFrame with feautures
    vectors_array        - array of vectorized text used to find similarity
    feature_show         - feature that will be shown in final DataFrame
    """
    
    # Locating target element by its specific value
    index_of_element = df[df[feature_locate]==value_of_element].index.values[0]
    
    # Finding its value to show
    show_value_of_element = df.iloc[index_of_element][feature_show]

    # Dropping target element from df
    df_without = df.drop(index_of_element).reset_index().drop(['index'], axis=1)

    # Dropping target element from vectors array
    vectors_array = list(vectors_array)
    target = vectors_array.pop(index_of_element).reshape(1,-1)
    vectors_array = np.array(vectors_array)

    # Finding cosine similarity between vectors
    most_similar_sklearn = cosine_similarity(target, vectors_array)[0]

    # Sorting coefs in desc order 
    idx = (-most_similar_sklearn).argsort()

    # Finding features of similar objects by index
    all_values = df_without[[feature_show]]
    for index in idx:
        simular = all_values.values[idx]
     
    recommendations_df = pd.DataFrame({feature_show: show_value_of_element,
                                    "rec_1": simular[0][0],
                                    "rec_2": simular[1][0],
                                    "rec_3": simular[2][0],
                                    "rec_4": simular[3][0],
                                    "rec_5": simular[4][0]}, index=[0])
    

    return recommendations_df

# Ok, let's find books similar to "Algorithms" book based on the title:

get_recommendations("Algorithms", 'Book_title', df, title_vectors, 'Book_title')

# based on the prices:

get_recommendations("Algorithms", 'Book_title', df, title_vectors, 'Price')

# based on the ratings:

get_recommendations("Algorithms", 'Book_title', df, title_vectors, 'Rating')

# based on the description:


get_recommendations("Algorithms", 'Book_title', df, desc_vectors, 'Book_title')

# As you can see, recommendations based on description are different from title-based recommendations in some ways.

get_recommendations("Unity in Action", 'Book_title', df, desc_vectors, 'Book_title')


get_recommendations("Unity in Action", 'Book_title', df, title_vectors, 'Book_title')


# We can also access some book by any unique value, for example, by number of reviwes (or, more logically, ID of the book, if there's some):


get_recommendations("1,406", 'Reviews',  df, title_vectors, 'Book_title')


get_recommendations("The Information: A History, a Theory, a Flood", 'Book_title', df, title_vectors, 'Book_title')

