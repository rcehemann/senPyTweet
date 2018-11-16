# mock sentiment "model"
# generates random sentiment given text
#
# rcehemann
########################################

import random

class MockSentimentModel(object):

	def __init__(self):
		""" randomly set the rng seed """
		seed = random.randint(0, int(1e6))
		self.generator = random.Random(seed)
		return None

	def predict(self, texts):
		""" random() gives a uniform random number between 0 and 1,
			which we shift in accordance to the -1 -> 1 sentiment 
			convention """
		if isinstance(texts, str):
			texts = [texts]
		return [2 * (self.generator.random() - 0.5) for _ in texts]