------------------------------
      senPyTweet
------------------------------
### Sentiment API for twitter data

#### dependencies:
 * python >= 3.7.0
 * Flask >= 1.0.2
 * spaCy >= 2.0.16 (for default model)


#### setup
 * configurable port, host and models in yaml.

 * If the host is None, defaults to localhost.

 * To use a custom model, add it to the `./app/models/` directory and set `model: sub/path` in `config.yaml`. Models must support a `predict` method.

 * The default sentiment model uses spaCy v2's bloom-embedded CNN architecture, trained to the sentiment 140 dataset

#### run
send a `POST` request to http://host:port/score with a 'text' field to get sentiment.
```
pip install flask

python run.py

curl --request POST \
     --header "Content-Type: application/json" \
     --data "{\"text\":\"hello, world\"}" \
     http://localhost:1337/score

{
  "sentiment": [
    0.6753116103582357
  ],
  "status": 200
}
```
