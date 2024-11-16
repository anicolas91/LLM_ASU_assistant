'''
Main ASU online assistant app.

to run this app simply do:

gunicorn --bind=0.0.0.0:9696 api.app:app

and then you can query.

'''
import os
import sys
import uuid
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv() 

sys.path.append(os.path.dirname(__file__))

from rag import rag


# import db


app = Flask(__name__)


@app.route("/question", methods=["POST"])
def handle_question():
    ''' 
    This function gets the user question and gets as result
    a conversation id, the question, and the RAG answer from our
    pretrained RAG.
    '''
    data = request.json
    question = data["question"]

    if not question:
        return jsonify({"error": "No question provided"}), 400

    conversation_id = str(uuid.uuid4())

    answer = rag(question)

    result = {
        "conversation_id": conversation_id,
        "question": question,
        "answer": answer,
    }

    # db.save_conversation(
    #     conversation_id=conversation_id,
    #     question=question,
    #     answer_data=answer_data,
    # )

    return jsonify(result)


@app.route("/feedback", methods=["POST"])
def handle_feedback():
    ''' 
    This function handles any user feedback of thumbs up/down
    and stores it on a db.
    '''
    data = request.json
    conversation_id = data["conversation_id"]
    feedback = data["feedback"]

    if not conversation_id or feedback not in [1, -1]:
        return jsonify({"error": "Invalid input"}), 400

    # db.save_feedback(
    #     conversation_id=conversation_id,
    #     feedback=feedback,
    # )

    result = {
        "message": f"Feedback received for conversation {conversation_id}: {feedback}"
    }
    return jsonify(result)


if __name__ == "__main__":
    port_num = os.getenv('PORT', '9696')
    app.run(debug=True, host = '0.0.0.0', port=int(port_num)) 

