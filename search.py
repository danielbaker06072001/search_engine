import get_index

# return the formatted top-5 docs by VSM ranking
def rank_by_VSM(query, doc_dict, tfidf_dict):
    # implement here
    # get the top 5 docs

    outputs = "Using VSM to rank...\n"

    # format the outputs
    outputs = get_index.vectorSpaceModel(query, doc_dict,tfidf_dict)

    return outputs

# return the formatted top-5 docs by BM25 ranking
def rank_by_BM25(query, doc_dict, tf_dict, clean_dict, df_dict, vocab):
    # implement here
    # get the top 5 docs


    outputs = "Using BM25 to rank...\n"

    # format the outputs
    bm25_dict = get_index.bm25(tf_dict, clean_dict, df_dict, vocab)
    outputs = get_index.BM25Model(query, doc_dict, bm25_dict)

    return outputs





