from app.sen_py import SenPy
import spacy

class SpaCy(SenPy):
  def __init__(self):
    return None

  def load(self):
    nlp = spacy.load("./app/models/spaCy")

    def predict(text):
      return nlp(text).cats['POSITIVE']

    nlp.predict = predict

    return nlp

  def predict(self, text):
    return (2 * self.predict(text) - 1)
