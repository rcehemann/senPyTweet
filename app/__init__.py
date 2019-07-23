# senPyTweet web-layer API

from flask import Flask, request, jsonify
from app.sen_py import SenPy

def make_app():
	app = Flask(__name__)
	loaded_models = {}

	@app.route('/score', methods=["POST"])
	def score():
		data = request.get_json(silent=True, cache=False)

		if data is None:
			return jsonify(error="Forbidden", reason="Accepts application/json"), 403
		elif 'model' not in data or 'tweets' not in data:
			return jsonify(error="Forbidden", reason="Invalid request format"), 403
		else:
			model = load_model(loaded_models, data['model'])
			tweets = predict_tweets(model, data['tweets'])
			return jsonify(model=model.__module__, tweets=tweets), 200

	def load_model(loaded_models, requested_model):
		if requested_model in loaded_models:
			return loaded_models[requested_model]
		else:
			model = SenPy.load_model(requested_model)
			model = model.load()
			loaded_models[requested_model] = model
			return model

	def predict_tweets(model, tweets):
		for tweet in tweets:
			score = model.predict(tweet['text'])
			tweet['score'] = score
			tweet['sentiment'] = 'positive' if score > 0 else 'negative'
		return tweets

	return app

