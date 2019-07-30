class SenPy:
  def __init__(self):
    self.loaded_models = {}
    return None

  def get_model(self, requested_model):
    if requested_model in self.loaded_models:
      return self.loaded_models[requested_model]
    else:
      model = self.load_model(requested_model)
      self.loaded_models[requested_model] = model
      return model

  def load_model(self, model):
    if model == 'mock':
      from .models.mock import Mock
      return Mock().load()
    elif model == 'spacy':
      from .models.spacy import SpaCy
      return SpaCy().load()
    elif 'scikit/' in model:
      from .models.scikit import SciKit
      return SciKit(model.split('scikit/')[-1]).load()
    else:
      raise ValueError(
        f"Invalid model file: {1}".format(model)
      )

  def predict_tweets(self, model, tweets):
    for tweet in tweets:
      score = model.predict(tweet['text'])
      tweet['score'] = score
      tweet['sentiment'] = 'positive' if score > 0 else 'negative'
    return tweets

  def load(self):
    raise NotImplementedError("base class")

  def predict(self):
    raise NotImplementedError("base class")
