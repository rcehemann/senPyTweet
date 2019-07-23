# senPyTweet web-layer API

from flask import Flask, request, jsonify
from app.sen_py import SenPy

def make_app():
	app = Flask(__name__)
	senpy = SenPy()

	@app.route('/score', methods=["POST"])
	def score():
		data = request.get_json(silent=True, cache=False)

		if data is None:
			return jsonify(error="Forbidden", reason="Accepts application/json"), 403
		elif 'model' not in data or 'tweets' not in data:
			return jsonify(error="Forbidden", reason="Invalid request format"), 403
		else:
			model = senpy.get_model(data['model'])
			tweets = senpy.predict_tweets(model, data['tweets'])
			return jsonify(model=model.__module__, tweets=tweets), 200

	return app

