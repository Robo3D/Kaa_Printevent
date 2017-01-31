# coding=utf-8
from __future__ import absolute_import
# ## (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import thread
from datetime import datetime
from . import kaa


# ##HELPER FUNCTIONS###################
def valid_event(event):
	"""
	Makes sure that kaa is valid for mixpanel. Returns booleans.
	"""
	return event in [
		'Error',
		'PrintStarted',
		'PrintFailed',
		'PrintDone',
		'PrintCancelled',
		'PrintPaused',
		'PrintResumed'
	]


class Kaa_printeventPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.EventHandlerPlugin, octoprint.plugin.SettingsPlugin):
	"""
	It responds to events, generates mixpanel data and registers it to mixpanel server
	"""

	def on_after_startup(self):

		self._logger.info("Generate Message queue on startup")

	def on_event(self, event, payload):

		if not valid_event(event):
			pass 

		else:
			thread.start_new_thread(kaa.send, (event,))

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			Kaa_Printevent=dict(
				displayName="Kaa_printevent Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="robo3d",
				repo="Kaa_Printevent",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/robo3d/Kaa_Printevent/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Kaa_printevent Plugin"


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Kaa_printeventPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
