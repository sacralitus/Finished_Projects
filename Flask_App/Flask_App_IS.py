from flask import Flask, render_template, request
import settings
from Info_search import *

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def Search():
    user_q = ''
    output_line, output_dict = '', {}
    docs_len = 0

    if request.method == "POST":
        user_q = request.form.get('text')

        dic, all_words = update_dict()

        vectorized_documents, idf = vectorize_docs(dic, all_words)

        vectorized_request = vectorize_request(user_q, all_words, idf)

        print('Список термов:\n', all_words)

        print('\nВектор запроса:', vectorized_request)

        output = to_range(vectorized_request, vectorized_documents)


        if type(output) == dict:
            #print('Итоги поиска:')
            output_dict = output
            docs_len = len(output_dict.keys())
            for k, v in output_dict.items():
                print(k + '\n' + v)
        else:
            output_line = output

    return render_template('gif_maker.html',output_dict=output_dict, output_line=output_line,
                           docs_len= docs_len,text=user_q)




if __name__ == '__main__':
    app.run(use_reloader=settings.use_reloader, debug=settings.debug, host=settings.host, port=settings.port)
