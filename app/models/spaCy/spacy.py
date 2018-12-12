from app.sen_py import SenPy
import spacy

class SpaCy(SenPy):
  def __init__(self):
    return None

  def load(self):
    path = "/Users/thekeele/dev/senPyTweet/app/models/spaCy"
    nlp = spacy.load(path)
    def predict(text):
      return nlp(text).cats['POSITIVE']

    nlp.predict = predict

    return nlp

  def predict(self, text):
    return (2 * self.predict(text) - 1)
