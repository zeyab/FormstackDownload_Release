import urllib;
import urllib.request as urllib2
import json;

class APIBase:
	def __init__(self, configuration):
		self.config = configuration;

	def getData(self):
		raise NotImplementedError("getData is not implemented");
		

	def _getHttp(self):
		url = "https://" + self.config["baseurl"] + self.config["endpoint"];
		headers = self.config["headers"];
		
		req = urllib2.Request(url, headers=headers);

		res = urllib2.urlopen(req);
		res = res.read().decode('utf-8');
		return json.loads(res);
		