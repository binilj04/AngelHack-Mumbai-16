# This is the API from the HPE Haven OnDemand

from havenondemand.hodclient import *

hodClient = HODClient("f06a8c54-6bac-4080-b983-bb6b3e88ee82", "v1")
hodApp = ""


def asyncRequestCompleted(jobID, error, **context):
    if error is not None:
        for err in error.errors:
            print ("Error code: %d \nReason: %s \nDetails: %s\n" % (err.error,err.reason, err.detail))
    elif jobID is not None:
        hodClient.get_job_status(jobID, requestCompleted, **context)
        print("asd")

def requestCompleted(response, error, **context):
	resp = ""
	if error is not None:
		for err in error.errors:
			if err.error == ErrorCode.QUEUED:
				# wait for some time then call GetJobStatus or GetJobResult again with the same jobID from err.jobID
				print ("job is queued. Retry in 10 secs. jobID: " + err.jobID)
				time.sleep(10)
				hodClient.get_job_status(err.jobID, requestCompleted, **context)
				return
			elif err.error == ErrorCode.IN_PROGRESS:
				# wait for some time then call GetJobStatus or GetJobResult again with the same jobID from err.jobID
				print ("task is in progress. Retry in 60 secs. jobID: " + err.jobID)
				time.sleep(60)
				hodClient.get_job_status(err.jobID, requestCompleted, **context)
				return
			else:
				resp += "Error code: %d \nReason: %s \nDetails: %s\njobID: %s\n" % (err.error,err.reason, err.jobID)
	elif response is not None:
		documents = response["reference"]
		print(documents)
		print(response)

	

		
		
hodApp = HODApps.STORE_OBJECT
paramArr = {}
paramArr["file"] = "audio1.mp3"

context = {}
context["hodapp"] = hodApp

res=hodClient.post_request(paramArr, hodApp, async=True, callback=asyncRequestCompleted,**context)
