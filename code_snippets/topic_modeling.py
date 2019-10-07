import gensim
from nltk.stem.porter import *
import pandas as pd
from utils import *

def get_bow_corpus(docs):
    """ Get the bag-of-word form and dictionary from the document corpus.
        --------------------
        Parameter:
            docs: document corpus

        Return:
            (bow corpus, dictionary)
    """
    # Tokenize documents:
    tokenized_docs = [gensim.utils.simple_preprocess(doc) for doc in docs]

    # Create a dictionary from 'docs' containing
    # the number of times a word appears in the training set
    # using gensim.corpora.Dictionary and call it 'dictionary':
    dictionary = gensim.corpora.Dictionary(tokenized_docs)

    # Create the Bag-of-words model for each document i.e for
    # each document we create a dictionary reporting how many
    # words and how many times those words appear. Save this to 'bow_corpus'
    bow_corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]
    return bow_corpus, dictionary

def topic_modeling(num_topics, passes, num_cores,
        start_year, end_year, companies=['']):
    """ Use DA topic modeling to extract topic dictribution
        of documents over years.
        --------------------
        Parameter:
            start_year: starting year of interest
            end_year: ending year of interest
            companies (list of str): list of interested companies
            num_topics: fixed number of topics to be extracted
            passes: number of passes through document data in training
            num_cores: number of processors used in training

        Return:
            (pd.DataFrame, lda_model)
    """
    # Query desired reports for tf-idf.
    docs = query_docs(start_year, end_year, companies)

    # Get Bag-of-Words format for the docs.
    bow_corpus, dictionary = get_bow_corpus(docs)

    # Train lda model using gensim.models.LdaMulticore and save it to 'lda_model'
    lda_model =  gensim.models.LdaMulticore(bow_corpus,
                                            num_topics = num_topics,
                                            id2word = dictionary,
                                            passes = passes,
                                            workers = num_cores)

    # Get the topic distribution for all of the docs.
    probabilities = []
    for i in range(len(bow_corpus)):
        topic_vec = lda_model.get_document_topics(bow_corpus[i],
                                                  minimum_probability=0.0)
        topic_probs = [p[1] for p in topic_vec]
        probabilities.append(topic_probs)

    # Get the year range to serve as indices for the return dataframe.
    years = range(start_year, end_year)

    # Return dataframe of topic distribution over years.
    return (pd.DataFrame(probabilities, index=years).T, lda_model)






















