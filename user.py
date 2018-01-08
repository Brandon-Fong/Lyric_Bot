class User(object):

	sender_id = ""
	lyric_request = {"":""}

	def __init__(self, sender_id, lyric_request):
		self.sender_id = sender_id
		self.lyric_request = lyric_request

	def song(self):
		return self.lyric_request
	def senderid(self):
		return self.sender_id




	