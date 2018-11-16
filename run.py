# senPyTweet application runner
#
# rcehemann
################################

import yaml
import os
from app import make_app

cwd = os.getcwd()

settings = yaml.load(open(cwd + '/config.yaml', 'r'))
app_settings   = settings.pop('app_settings', {})
model_settings = settings.pop('model_settings', None)

if not model_settings:
	model_settings = {
		'path':'mock'
	}

elif not os.path.exists(cwd + '/app/models/' + model_settings['path']):
	raise NameError(model_settings['path'] + ' ' + \
		"not found in " + cwd + "/app/models/")

if __name__ == '__main__':
	app = make_app(**model_settings)
	app.run(**app_settings)