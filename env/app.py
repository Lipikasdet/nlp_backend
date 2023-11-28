from flask import Flask, jsonify,request
from PIL import Image
import pytesseract
from textblob import TextBlob
import spacy
import requests


nlp = spacy.load("en_core_web_sm")



api = Flask(__name__)

@api.route('/profile')
def my_profile():
    if(request.args.get('sentence') ):
        text=request.args.get('sentence')
    else:
        text='i'
    blob = TextBlob(text)
    words = blob.words
    # text2 = "Apple Inc. is located in Cupertino, California. It was founded by Steve Jobs."
    doc = nlp(text)
    noun_phrases = blob.noun_phrases
    sentiment_polarity = blob.sentiment.polarity
    tags = blob.tags
    correct_text = blob.correct()
    entity_dict = {}

    print(request.args.get('sentence'))
    for word in doc.ents:
   
        entity_dict[word.text] = word.label_
    
    response_body = {
        "text": text,
        "sentiment": sentiment_polarity,
        "words": words,
        "nounphrases": noun_phrases,
        "tags": tags,
        "named_conventions": entity_dict,
        "corrected_sentence":str(correct_text),
     
    }

    return jsonify(response_body)


@api.route('/upload', methods=['POST','GET'])
def scan():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file in the request'})

        uploaded_file = request.files['file']

        # Check if the uploaded file is an image
        if uploaded_file.content_type.startswith('image'):
            img = Image.open(uploaded_file)
            text = pytesseract.image_to_string(img)
            return jsonify({'success': True, 'text': text})
        else:
            return jsonify({'success': False, 'error': 'Uploaded file is not an image'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})  

if __name__ == "__main__":
    api.run(debug=True)
