import urllib
import json
from http.client import HTTPSConnection

uri = 'westus.api.cognitive.microsoft.com'
accessKey = '940fd00ea36e44e89e09486ee3abd9c3'

def GetSentiment (documents):
    path = '/text/analytics/v2.0/sentiment'
    
    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = HTTPSConnection (uri)
    body = json.dumps (documents)
    conn.request ("POST", path, body, headers)
    response = conn.getresponse ()
    return response.read ()



##Sample##############################################################################
documents = { 'documents': [
    { 'id': '3085152', 'language': 'en', 'text': 'Thanks, we solve the memory problem. But we meet a new problem. About the network connection in windows phone 8 cocos2d-x. We didnt find curl or httpclient support for windows phone 8. How can we access the server side?' },
    { 'id': '10075507', 'language': 'en', 'text': 'It would be very helpful, if you could find specific steps to reproduce the crash including the image' }
]}
    
result = GetSentiment(documents)
sentiments = json.loads(result)["documents"]

print(sentiments)
######################################################################################

