# ----------------------------------------------------------------------------------------------------------------------#
# Written by : Christopher Perreault
# Date : 2022-09-25
# Description : This is the doctor's file
# Version : 0.3.0
# Contains :
#   - The doctor class
#   - The doctor's methods (can_zap)
# ----------------------------------------------------------------------------------------------------------------------#

class Doctor:
	def __init__(self, zap_count):
		self.zap_count = zap_count

	def can_zap(self):
		return bool(self.zap_count)
