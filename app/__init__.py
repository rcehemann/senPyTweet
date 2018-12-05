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
	if 'spaCy' in path:
		import spacy
		nlp = spacy.load(path)

		def predict(tweet):
			return nlp(tweet).cats['POSITIVE']

		nlp.predict = predict

		return nlp

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
		if data is None:
			return jsonify(
				error='Content-Type must be application/json'
			), 403

		if 'tweets' not in data:
			return jsonify(
				error='Request data must contain "tweets"'
			), 400
		
		for tweet in data['tweets']:
			if len(tweet['text']) > 0:
				score = 2 * model.predict(tweet['text']) - 1
				tweet.update(
					dict(
						score = score,
						sentiment = 'positive' if score > 0 else 'negative'
					)
				)

		return jsonify(data), 200

	return app

