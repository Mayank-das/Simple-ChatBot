from flask import Flask, request, render_template, jsonify
import BotResponse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    print("home page")
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    a = request.args.get("usr")
    
    return jsonify({'chat': BotResponse.predict_output(a)})

app.run(debug=True)