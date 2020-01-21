#данный скрипт выдаёт словарь со всеми значениями и контекстами к ним (training set)

def scrape_txt():
    from Zvezda import define_microcontext
    from collections import Counter

    with open("static/file.txt") as f:
        text = f.read()
        word_meanings = {}

    stopwords_r = open('static/stopwords_r.txt')
    stopwords_r = stopwords_r.read()
    stopwords_r = stopwords_r.split(', ')

    for item in text.split('\n\n'):
        text, meaning = item.split('значение: ')
        found, context = define_microcontext(text) #возвращается найденная лемма "звезда" и контекст

        context = list(filter(lambda x: x not in stopwords_r, context))#убираем стоп-слова из контекста

        text = context

        context = Counter(context) #Частотный словарь

        context = {k: round(v / len(text), 3) for k, v in context.items()} #Присвоение MLE-коэффицента каждому слову контекста

        word_meanings[meaning] = context

    return word_meanings


#for k,v in scrape_txt().items():
#     print(k+':',v)





