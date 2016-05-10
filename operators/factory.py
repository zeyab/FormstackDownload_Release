from .WILPSubmissions import WILPSubmissions
class Factory:
	@staticmethod
	def getObject(name, config):
		if(name.lower() == "wilpsubmissions"):
			return WILPSubmissions(config);
		else:
			raise ValueError("Invalid name provided: " + name);