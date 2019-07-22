#!/usr/bin/env python

##############
# USER CONFIG
##############
# Base URL to SABnzbd like localhost:8080
baseUrl=""
# Your API key
apiKey=""


###############
# Start Script
###############
import json 

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import quote_plus

# check if url is set and if not get it from user
while baseUrl == "":
  baseUrl = input("What is the URL to your SABNZBD instance (for example: localhost:8080) ")

# check if apikey is present or get if from user
while apiKey == "":
  apiKey = input("Please provide your API key: ")

# add slash to end of url if it doesn't exist
if baseUrl[:-1] != '/':
  baseUrl = baseUrl + '/'


# write api statement
baseUrl=baseUrl+"sabnzbd/api?output=json"
api="&apikey=" + apiKey
stmt=baseUrl + api 

# test api connection

req = Request(stmt)

# get html response from server to verify the connection works
try:
    response = urlopen(req) 
except HTTPError as e:
    # print error if website not found or server error
    print('Error code: ', e.code)
    exit('Please check the setting and try again: ' + stmt)
except URLError as e:
    # 
    print('Reason: ', e.reason)
    exit('Please check the setting and try again: ' + stmt)
else:
    # do something
    data = json.loads(response.read().decode("utf-8"))

    try:
      err = data['error'].lower()
    except:
      print('Connection could not be established')

if 'err' in locals():
  if err == 'api key incorrect':
    exit('The API key could not be validated. Please check and try again.')
  elif err != 'not implemented':
    exit('An error occurred while verifying the API connection. Please check values and try again.')


# build the rest of the query
mode="mode=history"

# get the search string from the user and encode it to comply with url encoding rules
searchString=''
while searchString == '':
  user = searchString=quote_plus(input("What are you looking for? "))

search="search=" + searchString

opt="start=1&limit=100"

# build search statement
stmtSearch=stmt + "&" + mode + "&" + search + "&" + opt
print(stmtSearch)

# get result from server and parse to get file name and id
with urlopen(stmtSearch) as url:
  data = json.loads(url.read().decode())

  i=0
  user=''
  ids=[]
  while user !='n' and user !='y':
    for item in data['history']['slots']:
      print (item['nzb_name'])
      ids.append( (item['nzo_id'], item['nzb_name']) )
      i += 1

    # check if user really wants to delete all the matches from the history
    if i >= 1:
      user = input("Are you sure you want to remove " +str(i)+ " entries? (y/n): ")[:1].lower()
    else:
      exit('nothing to delete')

    # go through list of elements to delete and delete them from history
    if user == 'y':  
      for id in ids:
        print('attempting to delete from list: ' + id[1])

        stmtDelete=stmt + "&" + mode + "&name=delete&value=" + id[0]
        with urlopen(stmtDelete) as url:
          res = json.loads(url.read().decode())
          print('status: ' + str(res['status']) )
          
    else: # if the user entered n for no (do not delete)
      print('User action: abort')
