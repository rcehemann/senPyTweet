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
