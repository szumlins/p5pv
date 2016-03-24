from flask import Flask, render_template
from flask_restful import Api, Resource
import json
import subprocess
import os
import config
import datetime
import xml.etree.ElementTree as ET

#simple command to get errors
nsderr = [config.nsdchat,'-c',"geterror"]

#function to format P5 lists into python lists
def format_list(list):
	result = []
	new_list = list.split()
	for item in new_list:
		result.append(item.strip())
	return result

#simple function to run nsdchat commands and return strings OR errors
def run(cmd):
	try:
		result = subprocess.check_output(cmd)
	except:
		error = subprocess.check_output(nsderr)
		return error.strip()
	return	result.strip()

#return all running jobs as python list
def runningJobs():
	cmd = [config.nsdchat,'-c',"Job","running"]
	return format_list(run(cmd).strip())

#return all jobs completed in last 24 hours as python list	
def completedRecent():
	cmd = [config.nsdchat,'-c',"Job","completed","1"]
	return format_list(run(cmd).strip())
#return all jobs with warnings in last 24 hours as python list	
def warningRecent():
	cmd = [config.nsdchat,'-c',"Job","warning","1"]
	return format_list(run(cmd).strip())
#return all jobs failed in last 24 hours as python list	
def failedRecent():
	cmd = [config.nsdchat,'-c',"Job","failed","1"]
	return format_list(run(cmd).strip())
#get a P5 xmlticket formatted as json for a job	
def jsonTicket(job):
	cmd = [config.nsdchat,'-c',"Job",job,"xmlticket"]
	root = ET.fromstring(run(cmd))
	json_ticket = dict(job=str(job),
			description=root.findall('description')[0].text,
			startdate=root.findall('startdate')[0].text,
			enddate=root.findall('enddate')[0].text,
			starttime=root.findall('starttime')[0].text,
			endtime=root.findall('endtime')[0].text,
			result=root.findall('result')[0].text,
			report=root.findall('report')[0].text)
	cmd = [config.nsdchat,'-c',"Job",job,"label"]
	json_ticket['label'] = run(cmd).strip()
	cmd = [config.nsdchat,'-c',"Job",job,"status"]
	json_ticket['status'] = run(cmd).strip()			
	cmd = [config.nsdchat,'-c',"Job",job,"report"]
	json_ticket['report'] = repr(run(cmd).strip())	
	return json_ticket



#API class to return xmlticket P5 API call as JSON
class JSONTicket(Resource):
	def get(self, name):
		return jsonTicket(name)

#API class to return all current job info for viewing as JSON
class FullReport(Resource):
	def get(self):
		running = runningJobs()
		completed = completedRecent()
		failed = failedRecent()
		warning = warningRecent()
		report = []
		for job in running:
			this_report = jsonTicket(job)
			report.append(this_report)
		report_dict = dict(data=report)
		return report_dict

#get the server time
class getTime(Resource):
	def get(self):
		time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
		return time

				
#instantiate app		
app = Flask(__name__)
api = Api(app)

#add routes for API calls
api.add_resource(JSONTicket, '/job/<int:name>/jsonticket', endpoint='job.jsonticket')
api.add_resource(FullReport, '/job/fullreport', endpoint='job.fullreport')
api.add_resource(getTime, '/job/gettime', endpoint='job.gettime')

#add route for UI
@app.route('/')
def process_viewer():
	return render_template('process_viewer.html')

#start the app.  Change debug=False for production use
if __name__ == '__main__':
	app.run(debug=True)