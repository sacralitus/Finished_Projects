# СКРИПТ ТРЕБУЕТ НАЛИЧИЯ МОДЕЛИ FASTTEXT, которую следует предварительно скачать и поместить в папку со скриптом (ссылка на модель - http://files.deeppavlov.ai/embeddings/ft_native_300_ru_twitter_nltk_word_tokenize.bin)

import pandas as pd
import fasttext
import torch
from sklearn.metrics.pairwise import cosine_similarity
from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsNERTagger,
    Doc
)
import warnings
warnings.filterwarnings('ignore')

segmenter = Segmenter()
emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)

#recapitization-repunctuation model
model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                           model='silero_te')
# fasttext model
ft = fasttext.load_model('ft_native_300_ru_twitter_nltk_word_tokenize.bin')


# Data reading and preprocessing 

df = pd.read_csv("test_data.csv")

df.text = df.text.str.lower() # lowering before recapitalization
df.loc[df.role == "manager", "text_prepr"] = df[df.role == "manager"].text.apply(lambda x: apply_te(x, lan="ru")) # recapitalization + repunctuation
df.loc[df.role=="manager",  "text_prepr"] = df.text_prepr.str.replace("компани", ", Компани") # to make companies visible to Natasha NER
df["insight"] = ""


# Dict to contain the final info (manager name, company name, is requirement satisfied for each dialogue)
info_dict = {"dialogue_id":df.dlg_id.unique().tolist(),
 "manager_name":["-" for _ in range(df.dlg_id.nunique())],
 "company_name":["-" for _ in range(df.dlg_id.nunique())],
 "requirement_satisfied":[False for _ in range(df.dlg_id.nunique())]}


# Script body
for dial_id in df.dlg_id.unique():
    
    is_greeting, is_farewell = 0, 0 # will count whether greeting&farewell are in stock 
    
    manager_dlg_df = df[(df.role == "manager") & (df.dlg_id == dial_id)]
    
    #greetings identification (treshhold>0.67)
    for ind, text in manager_dlg_df.text_prepr[:5].items():
        
        if cosine_similarity(ft.get_sentence_vector(text).reshape(1,-1),
                             ft.get_sentence_vector("здравствуйте приветствую добрый день").reshape(1,-1))[0][0] > 0.67:
            df.loc[ind, "insight"] = "greeting"
            is_greeting = 1 #maybe two or more greetings
            
    
    
    #farewell indentification (treshhold>0.73)
    for ind, text in manager_dlg_df.text_prepr[-5:].items():
        if cosine_similarity(ft.get_sentence_vector(text).reshape(1,-1),
                             ft.get_sentence_vector("до свидания всего хорошего").reshape(1,-1))[0][0] > 0.73:
            df.loc[ind, "insight"] = "farewell"
            is_farewell = 1 
    
    # introduction + manager_name + company_name + requirement satisfied
    for ind, text in manager_dlg_df.text_prepr[:5].items():
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)

        for span in doc.spans:
            
            # introduction + manager name
            if span.type == "PER" and any(i in text.lower() for i in ['меня', 'зовут', 'это']) and span.text != "Угу":

                df.loc[ind, "insight"] = "introduction" if df.loc[ind, "insight"] == "" else df.loc[ind, "insight"]+"_introduction"
                info_dic8t['manager_name'][dial_id]=span.text
            
            # company name
            if span.type == "ORG":
                info_dict['company_name'][dial_id]=span.text
            
    # is requirement satisfied
   
    if is_greeting == is_farewell == 1:
        info_dict["requirement_satisfied"][dial_id] = True

        
# конечный csv, для каждого диалога содержащий информацию об имени менеджера, названии компании, а также булевое значение выполнения требования к менеджеру
pd.DataFrame(info_dict).to_csv("info_dict.csv", index=False)

# исходный файл, дополненный колонкой "insight", которая может содержать классификацию реплики: introduction, greeting, greeting_introduction, farewell
df.drop(columns=['text_prepr']).to_csv("test_data_preprocesssed.csv")