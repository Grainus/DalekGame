# ----------------------------------------------------------------------------------------------------------------------#
# Written by : Christopher Perreault
# Date : 2022-09-17
# Description : This is the doctor's file
# Version : 0.2.0
# Contains : innit, can zap, teleport

# ----------------------------------------------------------------------------------------------------------------------#

class Doctor:
	def __init__(self, zap_count: int):
		self.zap_count = zap_count
		self.is_alive = True

		def can_zap(self) -> bool:
			return self.zap_count > 0

		def teleport(self):
			raise NotImplementedError
