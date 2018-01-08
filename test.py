import requests
import json

import os
import sys
import json
import musixmatch
import logging
from distutils.core import setup

import requests
from flask import Flask, request

# Takes the form of song name, artist name
def lyric_print(user_input):
	base_url = "http://api.musixmatch.com/ws/1.1/matcher.lyrics.get"

	holder = user_input
	# holder would return a string that is 
	# holder = root:song, artist
	# Remove unecessary characters from the string, root
	array = holder.replace("root:","")
	#Convert string array into a list/array named array by splitting by the comma
	#Therefore it becomes [Songname, artistname]
	array = array.split(",")
	#Dictionary consisting of the necessary parameter for the matcher.lyrics.get API method
	#apikey is set and is obtained from the registration for a musixmatch developers account 
	data = {
		"apikey":"APIKEY_PROVIDED_BY_MUSIXMATCH",
		"q_track":array[0],
		"q_artist":array[1],
		"format":"json"
		}
	#This sends a request to the musixmatch API, with the url base_url, with the parameters set at data
	response = requests.get(base_url, params = data)
	#Reponse.json() returns a multi-dimensional dictionary that consists of data such as username and etc....
	#String obtains the lyrics of the song name by accessing the value of the dictionary with a key of lyrics_body 
	string = response.json()['message']['body']['lyrics']['lyrics_body']

	#Musixmatch purposely included a message into each of their API requests, therefore this is to remove it
	lyrics = string.replace("******* This Lyrics is NOT for Commercial use *******(1409613705482)","")
	
	#Facebook limitis the number of characters to 640, hence divide lyrics into a substring 
	#with 640 substrings
	return lyrics[:640]
	


	









