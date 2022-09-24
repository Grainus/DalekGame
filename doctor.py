# ----------------------------------------------------------------------------------------------------------------------#
# Written by : Christopher Perreault
# Date : 2022-09-17
# Description : This is the doctor's file
# Version : 0.2.0
# Contains : innit, can zap, teleport

# ----------------------------------------------------------------------------------------------------------------------#

class Doctor:
	def __init__(self, zap_count):
		self.zap_count = zap_count
		self.is_alive = True

		def can_zap(self):
			return bool(self.zap_count)

		def teleport(self):
			pass
