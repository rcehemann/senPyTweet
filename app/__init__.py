# senPyTweet web-layer API
#
# rcehemann
##########################

from flask import Flask, request, jsonify

def load_model(path=None, **kwargs):
	""" 
	load the sentiment model from path,
	passing other arguments onward
	"""
	if path == 'spaCy/default.pickle':
		import pickle
		return pickle.load(open(model_path, 'rb'))
	elif path == 'mock':
		from .models.mock.mock_sentiment import MockSentimentModel as MSM
		return MSM()
	else:
		# need to detect model type and/or use specifications from config.yaml
		return load_model(path='mock')

def make_app(**model_settings):
	"""
	make a Flask object with defined endpoints and model
	"""
	model = load_model(**model_settings)
	app   = Flask(__name__)

	@app.route('/score', methods=["POST"])
	def score():
		data = request.get_json()
		print(request)
		try:
			return jsonify(
				sentiment=model.predict(data['text']),
				status=200
			)
		except:
			return jsonify(
				status=500
			)

	return app

