#!/usr/bin/python
from flask import Flask, render_template,request
import settings
from Disambiguator import disambiguate

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def Zvezda():
    found, text, meaning = '','',''
    word_meanings={}

    if request.method == "POST":
        text = request.form.get('text')
        found, meaning = disambiguate(text)


    return render_template('gif_maker.html',text=text,meaning=meaning,found=found)




if __name__ == '__main__':
    app.run(use_reloader=settings.use_reloader, debug=settings.debug, host=settings.host, port=settings.port)
