import re

class SenPy:
  def __init__(self):
    return None

  def load(self):
    raise NotImplementedError("base class")

  def predict(self):
    raise NotImplementedError("base class")

  def load_model(model):
    if model == 'mock':
      from .models.mock import Mock
      return Mock()
    elif model == 'spacy':
      from .models.spacy import SpaCy
      return SpaCy()
    elif 'scikit/' in model:
      from .models.scikit import SciKit
      return SciKit(model.split('scikit/')[-1])
    else:
      raise ValueError(
        f"Invalid model file: {1}".format(model)
      )

def clean_tweet(text):
    # remove links, replace with LINK token
    urls = r'((http|ftp|https):\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)'
    text = re.sub(urls, '/LINK/', text.lower())

    # remove non alphanumerics/spaces
    #text = re.sub('[^\w\d\s]', '', text)

    # replace numbers with the token 'NUMBER'
    text = re.sub('\d+[\,?\d]*', '/NUMBER/', text)

    # replace characters repeated more than twice with
    # just two occurrences
    text = re.sub(r'(.)\1{2,}', "\\1\\1", text)

    # replace duplicate whitespace with single whitespace
    text = re.sub(r'\s{2}', ' ', text)

    return text.strip() # remove preceding and trailing whitespace
