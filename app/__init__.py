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
		print(data)

		try:
			if 'tweets' in data.keys():
				for tweet in data['tweets']:
					tweet.update(
						dict(
							sentiment=model.predict(tweet['text'])
						)
					)
				data.update(dict(status=200))

			elif 'text' in data.keys():
				data.update(
					dict(
						sentiment=model.predict(data['text']),
						status=200
					)
				)

			return jsonify(data)

		except Exception as e:
			print(e)
			return jsonify(
				status=500
			)

	return app

