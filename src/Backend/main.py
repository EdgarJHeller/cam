import requests
import json
from utils.es_requester import request_es, extract_sentences, request_es_ML, request_es_triple, request_context_sentences
from utils.sentence_clearer import clear_sentences, remove_questions
from utils.url_builder import set_index
from utils.objects import Argument, Aspect
from ml_approach.sentence_preparation_ML import prepare_sentence_DF
from ml_approach.classify import classify_sentences, evaluate
from marker_approach.object_comparer import find_winner

from flask import Flask, request, jsonify
from flask_cors import CORS
import sklearn


app = Flask(__name__)
CORS(app)


@app.route("/")
@app.route('/cam', methods=['GET'])
def cam():
    '''
    to be visited after a user clicked the 'compare' button.
    '''

    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
    set_index(config['index']['name'])

    fast_search = request.args.get('fs')
    obj_a = Argument(request.args.get('objectA').lower().strip())
    obj_b = Argument(request.args.get('objectB').lower().strip())
    aspects = extract_aspects(request)
    model = request.args.get('model')
    statusID = request.args.get('statusID')

    if model == 'default' or model is None:
        # json obj with all ES hits containing obj_a, obj_b and a marker.
        setStatus(statusID, 'Request ES')
        json_compl = request_es(fast_search, obj_a, obj_b)

        # list of all sentences containing obj_a, obj_b and a marker.
        setStatus(statusID, 'Extract sentences')
        all_sentences = extract_sentences(json_compl)

        # removing sentences that can't be properly analyzed
        setStatus(statusID, 'Clear sentences')
        all_sentences = clear_sentences(all_sentences, obj_a, obj_b)

        # find the winner of the two objects
        setStatus(statusID, 'Find winner')
        return jsonify(find_winner(all_sentences, obj_a, obj_b, aspects))

    else:
        setStatus(statusID, 'Request all sentences containing the objects')
        if aspects:
            json_compl_triples = request_es_triple(obj_a, obj_b, aspects)
        json_compl = request_es_ML(fast_search, obj_a, obj_b)

        setStatus(statusID, 'Extract sentences')
        if aspects:
            all_sentences = extract_sentences(json_compl_triples)
            all_sentences.update(extract_sentences(json_compl))
        else:
            all_sentences = extract_sentences(json_compl)

        if len(all_sentences) == 0:
            return jsonify(find_winner(all_sentences, obj_a, obj_b, aspects))

        remove_questions(all_sentences)

        setStatus(statusID, 'Prepare sentences for classification')
        prepared_sentences = prepare_sentence_DF(all_sentences, obj_a, obj_b)

        setStatus(statusID, 'Classify sentences')
        classification_results = classify_sentences(prepared_sentences, model)

        setStatus(statusID, 'Evaluate classified sentences; Find winner')
        return jsonify(evaluate(all_sentences, prepared_sentences, classification_results, obj_a, obj_b, aspects))


@app.route('/status', methods=['GET'])
@app.route('/cam/status', methods=['GET'])
def getStatus():
    statusID = request.args.get('statusID')
    return jsonify(status[statusID])


@app.route('/remove/status', methods=['DELETE'])
@app.route('/cam/remove/status', methods=['DELETE'])
def removeStatus():
    statusID = request.args.get('statusID')
    print('Remove registered:', statusID)
    del status[statusID]
    return jsonify(True)


@app.route('/register', methods=['GET'])
@app.route('/cam/register', methods=['GET'])
def register():
    statusID = str(len(status))
    setStatus(statusID, '')
    print('Register:', statusID)
    return jsonify(statusID)

@app.route('/context', methods=['GET'])
@app.route('/cam/context', methods=['GET'])
def get_context():
    # http://localhost:5000/cam/context?documentID=%27http://www.universetoday.com/36129/density-of-venus/%27&sentenceID=3&contextSize=2
    document_id = request.args.get('documentID')
    sentence_id = int(request.args.get('sentenceID'))
    context_size = int(request.args.get('contextSize'))
    context = request_context_sentences(document_id, sentence_id, context_size)
    context_sentences = extract_sentences(context)
    return jsonify(context_sentences)



def setStatus(statusID, statusText):
    if statusID != None:
        status[statusID] = statusText


def extract_aspects(request):
    aspects = []
    i = 1
    while i is not False:
        asp = 'aspect{}'.format(i)
        wght = 'weight{}'.format(i)
        inputasp = request.args.get(asp)
        inputwght = request.args.get(wght)
        if inputasp is not None and inputwght is not None:
            asp = Aspect(inputasp.lower(), int(inputwght))
            aspects.append(asp)
            i += 1
        else:
            i = False
    return aspects


if __name__ == "__main__":
    status = {}
    app.run(host="0.0.0.0", threaded=True)
