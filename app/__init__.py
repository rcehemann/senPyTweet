# senPyTweet web-layer API
#
# rcehemann
##########################

from flask import Flask, request, jsonify
from app.sen_py import SenPy

def make_app(**model_settings):
	"""
	make a Flask object with defined endpoints and model
	"""
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

		model = SenPy.load_model(data['model'])
		model = model.load()

		for tweet in data['tweets']:
			if len(tweet['text']) > 0:
				score = model.predict(tweet['text'])
				tweet.update(
					dict(
						score = score,
						sentiment = 'positive' if score > 0 else 'negative'
					)
				)

		return jsonify(data), 200

	return app

