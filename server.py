#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 17:05:58 2022

@author: PersonalAccount
"""

from flask import Flask, request
import requests
import json

# TO create a Flask app
app = Flask(__name__)
  

#Pre process the response by filtering the posts that contain any of the tags
# in response tp ?tags=science,tech. So if any posts contain one of these two
# It will return those posts. It is an OR logic
def tags_present(tags,json_obj):
    plist =[]
    json_obj_res = {}
    tags = tags.split(',')
    lst = json_obj['posts']
    for i in range(0,len(lst)):
        ptags = lst[i]['tags']
        if any(x in ptags for x in tags):
            plist.append(lst[i])
    if(len(plist)!=0):        
      json_obj_res['posts'] = plist
    else:
      return({"error":"Probably the posts with the tag was not present!"})  
    return json_obj_res


#This function is to sort the posts by any one of the id,reads,likes or popularity.
#It throws the error Sort Parameter is Invalid if the parameter is wrong
def sort_json(sortBy,json_obj):
    lst = json_obj["posts"]
    json_obj_res = {}
    if(sortBy in ["id","reads","popularity","likes"]):
        sorted_posts = sorted(lst, key=lambda d: d[sortBy]) 
    else:
        return({"error":"Sort By Parameter is Invalid"})  
    json_obj_res['posts'] = sorted_posts    
    return json_obj_res

#This function is to respond to sort direction whether it is ascending or descending.
#So the array is just reversed after the default sort for descending.
#Did it in two functions for scaling if any mods are needed.
def sort_direction(sortBy,direction,json_obj):
    json_obj_res = {}
    lst = json_obj["posts"]
    if sortBy != None:
         if direction == "asc":
            json_obj_res["posts"] = lst
         if direction == "desc":
            sorted_posts = sorted(lst, key=lambda d: d[sortBy],reverse = True) 
            json_obj_res['posts'] = sorted_posts 
         if direction.strip() == "":
             json_obj_res["posts"] = lst
             
    return json_obj_res     
        
    
#The /api/posts return all posts. And the tags,sortBy and direction can be used together    
@app.route('/api/posts', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        tags  = request.args.get('tags')
        sortBy = request.args.get('sortBy')
        direction = request.args.get('direction')
        response = requests.get("https://api.hatchways.io/assessment/blog/posts?tag=tech")
        response_str = response.text
        json_object = json.loads(response_str)
        if(tags != None):
            if(len(tags.strip())==0):
                return ({"error":"Tags parameter is required","status code": 400})
            json_object = tags_present(tags,json_object)
        if(sortBy!=None):
            if 'posts' in json_object.keys():   
              json_object = sort_json(sortBy,json_object)
            else:
                return json_object 
        if(direction!=None):
            if 'posts' in json_object.keys():
                json_object = sort_direction(sortBy,direction,json_object)
            else:
                return json_object
        return json_object
  
#/api/ping This is to ping the api to detect if posts api is reaching the destination
#Did not add a check for empty posts as it can happen!
@app.route('/api/ping', methods = ['GET'])
def api_ping():
    if(request.method == 'GET'):
         response = requests.get("https://api.hatchways.io/assessment/blog/posts?tag=tech")
         response_str = response.text
         json_object = json.loads(response_str)
         if 'posts' in json_object.keys():
             return ({"success":"true","status code": 200})
        

  

  
  
# I used the port 7000 to avoid any conflict with other ports being used.
# Had some trouble in the beginning as the default ports were showing as used. Killing processes 
#didnt help for some reason.
if __name__ == '__main__':
    app.run(debug = True,port=7000)
  