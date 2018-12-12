------------------------------
 senPyTweet
------------------------------
### Sentiment API for twitter data

#### dependencies:
 * python >= 3.7.0
 * Flask >= 1.0.2
 * spaCy >= 2.0.16 (for the default model)


#### features
 * configurable port, host and models in yaml.

 * If the host is None, defaults to localhost.

 * To use a custom model, add it to the `./app/models/` directory and set `model: sub/path` in `config.yaml`. spaCy-based custom models must be trained with a category `'POSITIVE'`. Models must support a `predict` method if they are not spaCy-based.

 * The default sentiment model uses spaCy v2's bloom-embedded CNN architecture, trained to the sentiment 140 dataset

#### setup
`pip install -r requirements.txt`

#### run
send a POST request to http://host:port/score get sentiment.

```
python run.py

curl --request POST \
	 --header "Content-Type: application/json" \
	 --data "{\"model\":\"mock\",\"tweets\":[{\"text\":\"senPyTweet stinks\", \"tweet_id\":0}, {\"text\":\"crypto is the future\", \"tweet_id\":1}]}" \
	 http://localhost:1337/score

{
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
