from flask import Flask, render_template, request
import numpy as np
import json
import requests
from PIL import Image

app = Flask(__name__)

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
	if request.method == "POST":
		i = Image.open(request.files['file'].stream).convert('L')
		i = i.resize((28,28))
		img = np.array(i)
		img = img/255.0
		img = img.reshape(1,-1)
		test = json.dumps({'data':img.tolist()})
		headers = {'Content-Type':'application/json'}
		url = 'http://a390e8ba-0758-41c9-99f1-c0c646acf82c.westus.azurecontainer.io/score'
		r = requests.post(url, test, headers=headers)
		pred = r.text

		return render_template('predict.html', data=pred)

if __name__ == "__main__":
	app.debug = True
	app.run()