from math import log
import numpy as np

def normalize(string):

    import re
    import pymorphy2
    from nltk.corpus import stopwords

    morph = pymorphy2.MorphAnalyzer()

    string = string.lower().strip()
    string = re.sub(r'''[–,@':;?.$%!()/*$#_&"-]''', "", string)  #punctuation
    string = re.sub(r"\s+", " ", string)  # multiple spaces
    string = string.split(' ') #tokenizing
    string = list(map(lambda x: morph.normal_forms(x)[0], string)) #lemmatization
    body = [word for word in string if word not in stopwords.words('russian')] #stop-words removal

    return body


def update_dict(): #просмотр всех документов, разделение их по name и body, создание словаря уникальных слов в алф. виде
    with open("static/data.txt", encoding='utf-8') as f:
        #print('Cобираю информацию...')
        d = {}
        for i in f.read().split('\n\n'):
            name, body = i.split('\n')
            body = normalize(body)
            d[name] = body

        all_words = set([k for i in d.values() for k in i if k]) # gathering unique words from all the documents
        all_words = list(all_words)
        all_words.sort() #sorting in alphabetic ordeк

        #print("Завершено.\n")

        return d, all_words


def vectorize_docs(input_,all_words):
        #print('Векторизирую документы...')
        #print(all_words)
        # CREATING IDF

        idf = []

        for i in all_words:

            doc_frequency = len([k for k in input_.keys() if i in input_[k]])
            idf_index = log(len(input_.keys())/doc_frequency, 10)

            idf.append(idf_index)


        vectorized_documents = {}
        tf = {}

        # CREATING TF

        for k in input_.keys():

            tf[k] = np.array([input_[k].count(i)/len(input_[k]) for i in all_words])

        for k in tf.keys():
            vectorized_documents[k] = idf * tf[k]

        #print("Завершено.\n")

        return vectorized_documents,idf


def vectorize_request(input_,all_words,idf):

    #print('Векторизирую запрос...')
    request = normalize(input_)

    tf = [request.count(i)/len(request) for i in all_words]


    vectorized_request = np.array(idf)*tf
    #print('Завершено, Ян ;)\n')
    return vectorized_request


def cosine_similiarity(a,b):

    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)

    if norma/normb != 0.0:
        cos = dot / (norma * normb)
    else:
       cos = 0.0

    return cos



def to_range(vectorized_request, vectorized_documents):

    with open("static/data.txt", encoding='utf-8') as f:

        d = {}
        for i in f.read().split('\n\n'):
            name, body = i.split('\n')
            d[name] = body


    list_of_similiarities = sorted([(k,cosine_similiarity(vectorized_request,v)) for k,v in vectorized_documents.items()], key=lambda x: x[1],reverse=True)


    list_of_similiarities = [i for i in list_of_similiarities if i[1]!=0.0] #чистка нулевых косинусов

    if len(list_of_similiarities) == 0:
        return 'Результаты отсутствуют'

    else:
        output_d = {i[0]+' '+'('+str(round(i[1],3))+')':d[i[0]] for i in list_of_similiarities}
        print('\nСписок значений схожести:',*list_of_similiarities, sep='\n')
        print('\n')

        return output_d




# dic, all_words = update_dict()
#
# vectorized_documents,idf = vectorize_docs(dic, all_words)
#
# vectorized_request = vectorize_request("человек", all_words, idf)
#
# print('Список термов:\n', all_words)
#
# print('\nВектор запроса:', vectorized_request)
#
# output = to_range(vectorized_request,vectorized_documents)


# if type(output)==dict:
#     print('Итоги поиска:')
#     for k,v in output.items():
#         print(k+'\n'+v)
# else:
#     print(output)