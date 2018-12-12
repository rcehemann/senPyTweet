class SenPy:
  def __init__(self):
    return None

  def load(self):
    raise NotImplementedError("base class")

  def predict(self):
    raise NotImplementedError("base class")

  def load_model(model):
    if model == 'mock':
      from .models.mock.mock import Mock
      return Mock()
    elif model == 'spacy':
      from .models.spaCy.spacy import SpaCy
      return SpaCy()
