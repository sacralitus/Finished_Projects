def disambiguate(s):
    import re
    from Scraper_txt import scrape_txt
    from Zvezda import define_microcontext
    s = s.lower()

    s = re.sub(r'[?.,]', '', s)
    s = s.replace('- ','')
    s = s.replace('– ', '')

    word_meanings = scrape_txt()

    found,context = define_microcontext(s)

    # print(word_meanings)
    # print(context, found)

    word_meanings = list(word_meanings.items())
    # print(word_meanings)

    global success
    success = 0 #cчётчик, показывающий, что слова из микроконтекста найдены в списке контекста значений -> 1 - омонимия снята, 0 - не снята

    found_words = {}

    for k in range(len(word_meanings)):
        if any('рок' in i for i in context) or 'рок' in found:
            success = 1
            return "Найденная словоформа: {}".format(found), 'Лемма принадлежит к значению "Знаменитость"'

        sp1 = []
        if any(i in word_meanings[k][1].keys() for i in context):
            # print(list(word_meanings[k][1].keys()))
            success = 1
            for i in context:

                if i in word_meanings[k][1]:

                    sp1.append(i+':'+str(word_meanings[k][1][i]))

            found_words[word_meanings[k][0]]=sp1
            #print('found words:',found_words)


    if success == 0:
            return 'Найденная словоформа: {}'.format(found), 'Омонимия не снята :( Обратитесь к макроконтексту'
    else:
        if len(found_words.keys())==1:
            return 'Найденная словоформа: {}'.format(found), 'Лемма принадлежит к значению "{}"'.format(list(found_words.keys())[0])
        else: #Когда слова из микроконтекста были отнесены к нескольким значениям. Max. Likehood Est.
            # print('found words:', found_words)


            for i in range(len(found_words.values())):
                coef = 0
                for k in list(found_words.values())[i]:

                    coef += float(k.split(':')[1])

                found_words.update({list(found_words.keys())[i]:coef})

        print(found_words)
        coef_sp = [found_words[i] for i in found_words]

        global final_meaning


        for i in range(len(list(found_words.values()))+1):

            if str(max(coef_sp)) in str(list(found_words.values())[i]):

                final_meaning = list(found_words.keys())[i]
            else:
                continue


            return 'Найденная словоформа: {}'.format(found), 'Лемма принадлежит к значению "{}"'.format(final_meaning)


#print(disambiguate('Звезда моих ночей, услышь меня!'))


