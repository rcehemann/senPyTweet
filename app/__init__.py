# senPyTweet web-layer API
#
# rcehemann
##########################

from flask import Flask, request, jsonify
from app.sen_py import SenPy, clean_tweet
from app.models.spaCy.train import main as train

def make_app():
	"""
	make a Flask object with defined endpoints and model
	"""
	app = Flask(__name__)
	loaded_models = {}

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

		if data['model'] in loaded_models:
			model = loaded_models[data['model']]
		else:
			model = SenPy.load_model(data['model'])
			model = model.load()
			loaded_models[data['model']] = model

		for tweet in data['tweets']:
			if len(tweet['text']) > 0:
				score = model.predict(clean_tweet(tweet['text']))
				tweet.update(
					dict(
						score = score,
						sentiment = 'positive' if score > 0 else 'negative'
					)
				)

		return jsonify(data), 200

	return app

