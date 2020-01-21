import re #скрипт определяет микроконтекст леммы "звезда" и возвращает микроконтекст одного значения в виде множества(set)
import pymorphy2

def define_microcontext(s):

    morph = pymorphy2.MorphAnalyzer()

    s = re.sub(r'[!]{1}\s|[.]\s{1}|[?]{1}\s','##',s)

    found = 'не найдено'
    sp = []

    for sent in s.split('##'): #работа с каждым предложением, его "отшлифовка" для последующего анализа
        sent = sent.lower()
        sent = re.sub(r'[!?.,]', '', sent)
        sent = sent.replace('- ','')
        sent = sent.replace('– ', '')
        sent = sent.replace('―', '')
        sent = sent.replace('«', '')
        sent = sent.replace('»', '')
        sent = sent.split(' ')

        for i in range(len(sent)): #Способ с regex. Правильно подобраный regex избавляет от составления списка словоформ леммы (в нашем случае "звезда")


            try:
                if re.match(r'"?(рок-)?(теле)?[зЗ]в[ёе]зд[а-мо-я]{0,3}"?$',sent[i]).group() == sent[i]: # находим слово "звезда"
                    found = sent[i]

                    # if any(slovo in i for slovo in ['Звёзды','звёзды','звезда','звезды','звезде','звезду']):  #Способ без regex: меньше строк, но нужно составлять список словоформ
                    #                                                                                             замена способу с regex - оператор in
                    #     print('найдено:',i)
                    if i > 0:  # левый контекст
                        k = 5
                        ind = 1
                        while k > 0:
                            d = i - ind
                            if d >= 0:
                                sp.append(morph.parse(sent[d])[0].normal_form)
                                k -= 1
                                ind += 1
                            else:
                                break

                    if len(sent) - 1 - i >= 5:  # правый контекст
                        k = 1
                        while k <= 5:
                            sp.append(morph.parse(sent[i + k])[0].normal_form)
                            k += 1
                    else:
                        ind = 1
                        while i + ind <= len(s) - 1:

                            sp.append(morph.parse(sent[i + ind])[0].normal_form)
                            ind += 1

            except:
                continue

    return found, sp

# found,sp = define_microcontext('К потерянным звёздам мы держим свой путь')
# print('found:',found, ' sp:',sp)

