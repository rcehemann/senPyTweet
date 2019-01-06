from app.sen_py import SenPy
import spacy

class SpaCy(SenPy):
  def __init__(self):
    return None

  def load(self):
    self._nlp = spacy.load("./app/models/spaCy")
    return self

  def predict(self, text):
    return (2 * self._nlp(text).cats['POSITIVE'] - 1)
