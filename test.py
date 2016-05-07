from havenondemand.hodclient import *
client = HODClient("f06a8c54-6bac-4080-b983-bb6b3e88ee82", version="v1")
params = {'text': 'I love Haven OnDemand!'}
response = client.get_request(params, HODApps.ANALYZE_SENTIMENT, async=False)
print response