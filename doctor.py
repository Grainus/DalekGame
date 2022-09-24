class Doctor:
	def __init__(self, zap_count):
		self.zap_count = zap_count
		self.is_alive = True

		def can_zap(self):
			return bool(self.zap_count)

		def teleport(self):
			pass
