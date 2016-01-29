from django.apps import AppConfig

class MyAppConfig(AppConfig):
	name = 'links'

	def ready(self):
		import links.signals