#!/usr/bin/python

import httplib
import xml.etree.ElementTree as ET
import json
import cgi

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
trip = form.getvalue('trip') or 'home'

if trip == 'home':
  title = 'Work->Home';
  rt_st = [ '44:11354', '31:9138' ]
elif trip == 'work':
  title = 'Home->Work';
  rt_st = [ '44:18090', '31:40075' ]
elif trip == 'home_dt':
  title = 'Home->DT';
  rt_st = [ '24:24380', '33:31190' ]
elif trip == 'dt_home':
  title = 'DT->Home';
  rt_st = [ '24:590', '33:590' ]  

#routestop = = form.getvalue('routestop') or rt_st

#route = "44"
#stop = "11354"
key = "24f81f56-b55a-4c1e-a1c7-a27d32342acd"
#title = "To Home"
card = {}


arrivals =[]
for rt in rt_st:
   rt_list = rt.split(':') 
   route = rt_list[0] 
   stop = rt_list[1]
   #print "RT: %s STOP: %s" % (route, stop)

   url = "/api/where/arrivals-and-departures-for-stop/1_" + stop  + ".xml?key=" + key

   conn = httplib.HTTPConnection("api.pugetsound.onebusaway.org")
   conn.request("GET", url)
   r1 = conn.getresponse()
   #print r1.status, r1.reason

   data1 = r1.read()

   #print data1


   root = ET.fromstring(data1)

   now = int(root.find('currentTime').text)
   stopname = root.find(".//name").text
   #stopname = "NW 54TH ST &amp; 30TH AVE NW"

   ads = root.findall(".//arrivalAndDeparture")
   arr_str = ""

   #print now


   arrival = []
   for child in ads:
     if route == child.find('routeShortName').text:
       #print child.find('predictedArrivalTime').text
       if int(child.find('predictedArrivalTime').text) != 0:
         when = int(child.find('predictedArrivalTime').text) - now     
	 #print "perdict"
	 #print str(int(round((when / 60000),1))) 
       else:
         when = int(child.find('scheduledArrivalTime').text) - now
	 #print "sched"
	 #print str(int(round((when / 60000),1))) 

       if when != 0:
         when_min = str(int(round((when / 60000),1)))
       else: 
         when_min = "NOW"

       arrival.append(when_min)




   for arr in arrival:
      arr_str = arr_str + ' ' + arr 
   rt_str = "%s:%s min" % (route,arr_str)  
   arrivals.append(rt_str[0:14] + '\n')

#########
arrs_str = "%s\n" % (title[0:14])
for arrs in arrivals:
    arrs_str = arrs_str + arrs 
      
card['content'] = arrs_str
card['refresh_frequency'] = 1

print "Content-Type: application/javascript"     # HTML is following
print                               		# blank line, end of headers
print json.dumps(card)

