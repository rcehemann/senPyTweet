------------------------------
 senPyTweet
------------------------------
### Sentiment API for twitter data

#### features
 * To use a custom model, add it to the `./senPy/models/` directory. spaCy-based custom models must be trained with a category `'POSITIVE'`. Models must support a `predict` method if they are not spaCy-based.

 * The default sentiment model uses spaCy v2's bloom-embedded CNN architecture, trained to the sentiment 140 dataset

#### dependencies:
 * python >= 3.7.0
 * Flask == 1.0.2
 * spaCy == 2.0.16 (for the default model)

#### setup
`make install`

#### display server options
`make help`

#### run development server
`make dev`

#### example request / response
```
$ curl --request POST \
	 --header "Content-Type: application/json" \
	 --data "{\"model\":\"spacy\",\"tweets\":[{\"text\":\"senPyTweet stinks\", \"tweet_id\":0}, {\"text\":\"crypto is the future\", \"tweet_id\":1}]}" \
	 http://localhost:5000/score

{
  "model": "spacy",
  "tweets": [
    {
      "score": -0.9475799947977066,
      "sentiment": "negative",
      "text": "senPyTweet stinks",
      "tweet_id": 0
    },
    {
      "score": 0.9649665355682373,
      "sentiment": "positive",
      "text": "crypto is the future",
      "tweet_id": 1
    }
  ]
}

```
