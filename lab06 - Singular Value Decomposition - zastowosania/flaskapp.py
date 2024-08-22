from flask import Flask, request, render_template, redirect, url_for
from lab6 import CreateTermByDocumentMatrix, PrzeglądarkaMain, initialize_svd
from lab6_websiteHandler import createBOWs, calculateIDFs, IndexUrls
import time

app = Flask(__name__)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# . .venv/bin/activate !!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Create the Term-By-Document Matrix (TBDM) and store it in the app configuration
app.config['TBDM'] = CreateTermByDocumentMatrix()


def process_links(resultList):
    links = []
    if resultList is None:
        return
    for link, sparseMatrixValue in resultList:
        link = {'url': link,
                'value': str(round(sparseMatrixValue*100, 2)) + '%'}
        links.append(link)
    return links


def is_integer_string(s):
    return s.isdigit()


@app.route('/', methods=['GET', 'POST'])
def index():
    #100: 57.73, 47.66
    #500: 64.93, 53.82
    #800: 66.14 ~54
    TBDM = app.config.get('TBDM')
    #initialize_svd(TBDM, 100)
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    # Retrieve the TBDM from the app configuration or initialize it if not present
    TBDM = app.config.get('TBDM')
    result = None
    time_taken = None
    k = 10
    use_svd = True
    if request.method == 'GET':
        query = request.args.get('q', '')
        k = request.args.get('outputSize', 10)
        if not is_integer_string(k):
            k = 10
        use_svd = request.args.get('use_svd') == 'on'
        start = time.time()
        result = PrzeglądarkaMain(TBDM, query, OutputSize=int(k), SVD=use_svd)
        end = time.time()
        time_taken = str(round(end-start, 4)) + "s"
    return render_template('search.html', links=process_links(result), input_string=query, response_time=time_taken, outputSize=k, use_svd=use_svd)


@app.route('/remakeDatabase')
def remakeDatabase():
    createBOWs()
    calculateIDFs()
    IndexUrls()
    app.config['TBDM'] = CreateTermByDocumentMatrix()
    TBDM = app.config.get('TBDM')
    initialize_svd(TBDM, 100)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
