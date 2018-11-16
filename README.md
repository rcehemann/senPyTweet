* ------------------------------
* 			senPyTweet
* ------------------------------
* Sentiment API for twitter data

* dependencies:
- python >= 3.7.0
- Flask >= 1.0.2
- spaCy >= 2.0.16 (for default model)

configurable port, host and models in yaml.

If the host is None, defaults to localhost.

To use a custom model, add it to the `./app/models/` directory and set `model: sub/path` in `config.yaml`. Models must support a `predict` method.

The default sentiment model uses spaCy v2's bloom-embedded CNN architecture, trained to the sentiment 140 dataset

use:
``` python run.py ```

send a `POST` request to http://host:port/score with a 'text' field to get sentiment.