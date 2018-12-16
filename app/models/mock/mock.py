# mock sentiment "model"
# generates random sentiment given text
#
# rcehemann
########################################

from app.sen_py import SenPy
import random

class Mock(SenPy):
	def __init__(self):
		return None

	def load(self):
		""" randomly set the rng seed """
		seed = random.randint(0, int(1e6))
		self.generator = random.Random(seed)
		return self

	def predict(self, text):
		""" random() gives a uniform random number between 0 and 1,
			which we shift in accordance to the -1 -> 1 sentiment
			convention """
		return (2 * self.generator.random() - 1)
