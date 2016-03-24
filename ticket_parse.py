import xml.etree.ElementTree as ET

data = """<jobreport>
    <description>Archive plan 'Manual' archiving 'Audio'</description>
    <startdate>30.01.2016</startdate>
    <enddate>31.12.1969</enddate>
    <starttime>16:32:33</starttime>
    <endtime>19:00:00</endtime>
    <command>JobMgr archive 10003 -client localhost -dirlist /Users/szumlins/Desktop/media/Footage/Audio -indexRoot /Users/szumlins/Desktop/media/Footage -meta {description {}}</command>
    <result>failure</result>
    <report></report>
</jobreport>"""

root = ET.fromstring(data)

job_list = dict(job='job',
				description=root.findall('description')[0].text,
				startdate=root.findall('startdate')[0].text,
				enddate=root.findall('enddate')[0].text,
				starttime=root.findall('starttime')[0].text,
				endtime=root.findall('endtime')[0].text,
				result=root.findall('result')[0].text,
				report=root.findall('report')[0].text)

print job_list

	


