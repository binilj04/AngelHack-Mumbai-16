import MySQLdb
import subprocess
from havenondemand.hodclient import *

# Open database connection
db = MySQLdb.connect("localhost", "root", "codio", "TESTDB")
cursor = db.cursor()
# Prepare SQL query to INSERT a record into the database.
sql = """SELECT * FROM MainTable WHERE touch=0"""
try:
   # Execute the SQL command

    cursor.execute(sql)


   # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    cursor.close()
    print results[0][0]

    jobid = results[0][0]
    filepath = results[0][1]
    touch = results[0][2]
    url = results[0][3]
    refid = results[0][4]
    jobstat = results[0][5]
    ofpath = results[0][6]
    # Now print fetched result
    # print "44"
    print "jobid=%s,filepath=%s,touch=%d,url=%s,refid=%s,jobstat=%s,ofpath=%s" % (jobid, filepath, touch, url, refid, jobstat, ofpath)
    
except:
    print "Error: unable to fetch Initial data"
    exit


sql="UPDATE MainTable SET touch = 1  WHERE jobid = '%s'" % (jobid)



cursor = db.cursor()

try:
   # Execute the SQL command

    
    cursor.execute(sql)
    cursor.close()
    db.commit()
   
    print "Successfully updated Touch"
except:
    print "Error: unable Touch"




##check if the reference exists. If not then we will have to uploadto hpeand record the reference

if refid in ['0',None]:  # download the video from the url and update the filename and upload and update with a reference
	print "The file has no reference"



	subprocess.Popen(["rm test.mp4"], stdout=subprocess.PIPE, shell=True)  #removing the mp4

	st="youtube-dl -o 'test.mp4' %s" % url
	proc = subprocess.Popen([st], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	print "program output:", out," any error", err

	proc = subprocess.Popen(["ls test.mp4"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()


	dn_flag=0
	if 'test.mp4' in out:
		print "#SUCCESS"
		dn_flag=1
	else:
		print "#Failed to download"
		dn_flag=0

	##extract the audio   ./ffmpeg -i ~/Desktop/video/My\ 30\ second\ elevator\ pitch-08FX8TbL5g0.mp4 
	##-ab 160k -ac 2 -ar 11025 -vn ~/Desktop/video/audio1.mp3
	proc=subprocess.Popen(["rm audio1.mp3"], stdout=subprocess.PIPE, shell=True)  #removing the mp4
	(out, err) = proc.communicate()
	proc=subprocess.Popen(["./ffmpeg -i test.mp4 -ab 160k -ac 2 -ar 11025 -vn audio1.mp3"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()




	##now upload to the HPE for reference 





	hodClient = HODClient("f06a8c54-6bac-4080-b983-bb6b3e88ee82", "v1")
	hodApp = ""


	def asyncRequestCompleted(jobID, error, **context):
	    if error is not None:
	        for err in error.errors:
	            print ("Error code: %d \nReason: %s \nDetails: %s\n" % (err.error,err.reason, err.detail))
	    elif jobID is not None:
	        hodClient.get_job_status(jobID, requestCompleted, **context)
	        

	def requestCompleted(response, error, **context):
		global ref_val
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
			ref_val = response["reference"]
			#print(documents)
			

		

			
			
	hodApp = HODApps.STORE_OBJECT
	paramArr = {}
	paramArr["file"] = "audio1.mp3"

	context = {}
	context["hodapp"] = hodApp
	ref_val =''
	res=hodClient.post_request(paramArr, hodApp, async=True, callback=asyncRequestCompleted,**context)

	print(ref_val)


	## insert the reference
	#UPDATE tutorials_tbl  SET tutorial_title='Learning JAVA'  WHERE tutorial_id=3


	sql="UPDATE MainTable SET refid = '%s'  WHERE jobid = '%s'" % (ref_val,jobid)



	cursor = db.cursor()

	try:
	   # Execute the SQL command

	    
	    cursor.execute(sql)
	    cursor.close()
	    db.commit()
	    refid=ref_val
	    print "Successfully updated reference"
	except:
	    print "Error: unable to update reference"
	    
	# rename video file to the reference
	st="youtube-dl -o 'test.mp4' %s" % url

	st="mv test.mp4 %s.mp4 " % refid
	proc = subprocess.Popen([st], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()

	filename=ref_val+".mp4"
	sql="UPDATE MainTable SET filepath = '%s'  WHERE jobid = '%s'" % (filename,jobid)

	print sql

	cursor = db.cursor()

	try:
	   # Execute the SQL command

	    
	    cursor.execute(sql)
	    cursor.close()
	    db.commit()
	    
	    print "Successfully updated reference"
	except:
	    print "Error: unable to update reference"



else :
	print "The file has reference"
# disconnect from server
db.close()
