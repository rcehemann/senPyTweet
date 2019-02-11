from app.sen_py import SenPy
import pickle

class SciKit(SenPy):
  def __init__(self, mtype):
    self._path = "./app/models/scikit/{}.pckl".format(mtype)
    return None

  def load(self):
    with open(self._path, 'rb') as f:
      self._model = pickle.load(f)
    return self

  def predict(self, text):
    if isinstance(text, str):
      text = [text]

    # scikit models give an array containing all category
    # probabilities. the positive cat is the second column
    prob = self._model.predict_proba(text)[0,1]
    return (2 * prob - 1)
