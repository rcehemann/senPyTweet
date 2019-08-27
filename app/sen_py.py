import re

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

def clean_tweet(text):
    # remove links, replace with LINK token
    urls = r'((http|ftp|https):\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)'
    text = re.sub(urls, '/LINK/', text.lower())

    # remove non alphanumerics/spaces
    text = re.sub('[^\w\d\s]', '', text)

    # replace numbers with the token 'NUMBER'
    text = re.sub('\d+[\,?\d]*', '/NUMBER/', text)

    # replace characters repeated more than twice with
    # just two occurrences
    text = re.sub(r'(.)\1{2,}', "\\1\\1", text)

    # replace duplicate whitespace with single whitespace
    text = re.sub(r'\s{2}', ' ', text)

    return text.strip() # remove preceding and trailing whitespace
