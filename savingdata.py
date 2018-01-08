import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string

from test import lyric_print
import song
import user


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('JSON_FILE_BY_GOOGLE', scope)
gc = gspread.authorize(credentials)
#Opening the fb_messenger_bot Sheet1
worksheet = gc.open("GOOGLESHEET_NAME").sheet1
#returns the value within that cell

#val = worksheet.acell('B1').value # With label
#if the cell is empty, it would return ""

#Write the same content for a range of cells
# values = [
#     [
#         # Cell values ...
#     ],
#     # Additional rows ...
# ]
# body = {
#   'values': values
# }
# result = service.spreadsheets().values().update(
#     spreadsheetId=spreadsheet_id, range=range_name,
#     valueInputOption=value_input_option, body=body).execute()



#Select which sheet to use
# >>> sht = client.open('Sample one')
# >>> worksheet = sht.worksheet('Annual bonuses')


#Array of all uppercase Letters
letters = list(string.ascii_uppercase)


#Helpful Source
#http://gspread.readthedocs.io/en/latest/oauth2.html
def newuser(sender_id):
	#pushing cell values to a dictionary 
		#Cell Values A1, A3
		#x is a dictionary of {Cell Coordinates: Facebook User ID}
	x = {}
	for i in range(0,26,2):
		x[letters[i]+"1"] = worksheet.acell(letters[i]+"1").value
	
	for i in range(0, 26,2):
		#check whether the user exists already
		if x[letters[i]+"1"] != sender_id:
			#If the cell is empty, input their facebook user ID into that cell
			if x[letters[i]+"1"] == "":
				worksheet.update_acell(letters[i]+"1", sender_id)
				break
			else:
				return "There is no space left in this database"
		else:
			return "you already have an account"
		


def olduser_savingdata(sender_id, song_request, lyrics):
	#pushing cell values to a dictionary 
		#Cell Values A1, A3
		#x is a dictionary of {Cell Coordinates: Facebook User ID}

	x = {}
	for i in range(0,26,2):
		x[letters[i]+"1"] = worksheet.acell(letters[i]+"1").value


	#check whether the song is already inputed into the google spreadsheet
	for i in range(0,26,2):
		#Checking whether the cell value has the same sender_id as the user
		if x[letters[i]+"1"] == sender_id:
			#Loop through all the columns
			for j in range(1,998):
				holder = str(j) 
				#Check whether the value in the cell is the same as the song requested by the user
				if worksheet.acell(letters[i]+holder).value == song_request.lower():
					#breaks the loop to avoid reptition of the songs archieved by Google Spreadsheet
					break

				elif worksheet.acell(letters[i]+holder).value == "":
					#Update the cell with the song name and artistname
					#Example Cell Values A#, C#, E#
					worksheet.update_acell(letters[i]+holder, song_request)
					#Update the cell with the lyrics to the song requested
					#Example Cell Values B# , D# , E#
					worksheet.update_acell(letters[i+1]+holder, lyrics)
					break
				else:
					"There is no space left in this database"
#works
def olduser_or_newuser(sender_id):
 	answer = ""
 	count = 0
 	#pushing cell values to a dictionary 
		#Cell Values A1, A3
		#x is a dictionary of {Cell Coordinates: Facebook User ID}

	x = {}
	for i in range(0,26):
		x[letters[i]+"1"] = worksheet.acell(letters[i]+"1").value

	for i in range(0, 26):
		#If the user ID is contained in the dictionary of past users
		if x[letters[i]+"1"] == sender_id:
			count += 1
		else:
			count = count
	if count >= 1:
		answer = "old"
	else:
		answer = "new"

	return answer


#Searching for whether the song is already in google spreadsheet
def search_song(song_request):
	object_storage = {}
	for i in range(0,26,2):
		#Checks whether cell's (A1, C1, E1.....) has users
		if worksheet.acell(letters[i]+"1").value == "":
			break
		else:
			#Loops down that row
			for j in range(2,998):
				string_j = str(j)
				#Checks whether cell's (A#. C#, E#....) has the users song requested stored inside
				if worksheet.acell(letters[i]+string_j).value == "":
					break
				else:
					#Appends to the object_storage dictionary with {songname/artistname : lyrics}
					object_storage.update({worksheet.acell(letters[i]+str(j)).value : worksheet.acell(letters[i+1]+str(j)).value})

	#Converts the key and value into an object
	song_object = []
	for key in object_storage:
		#Creates an instance of the Song Object(Songname, lyrics)
		objects = song.Song(key, object_storage[key])
		song_object.append(objects)


	#Creating User Objects with parameters (userID, an instance of a song object)
	user_storage = {}
	for i in range(0,26,2):
		if worksheet.acell(letters[i]+"1").value == "":
				break
		else:
			for j in range(0, len(song_object)):
				#Make a dictionary {songname, user_id}, since keys must have unique values
				user_storage.update({song_object[j] : worksheet.acell(letters[i]+"1").value })
	user_object = []
	for key in user_storage:
		#Creates an instance of the User Object(UserID, Song Object)
		objects = user.User(user_storage[key], key)
		user_object.append(objects)
#Objective:
	#Since the lyrics are next to the title
	#Search for the song_requested from the user inside the spreadsheet, return #Column + 1
#Only Need to search through Column's A,C,E.....
#Going through Each Column
	for i in range(0, len(song_object)):
	#If the song has been requested previously, then loop through the user, song song object to find the stored lyrics
		if song_object[i].songname() == song_request:
			return song_object[i].songlyrics()
			break
		else:
	#Not requested before, obtain the lyrics by making the API call
			return lyric_print(song_request)
			break

def user_song(user_id):
	object_storage = {}
	for i in range(0,26,2):
		#Checks whether cell's (A1, C1, E1.....) has users
		if worksheet.acell(letters[i]+"1").value == "":
			break
		else:
			#Loops down that row
			for j in range(2,998):
				string_j = str(j)
				#Checks whether cell's (A#. C#, E#....) has the users song requested stored inside
				if worksheet.acell(letters[i]+string_j).value == "":
					break
				else:
					#Appends to the object_storage dictionary with {songname/artistname : lyrics}
					object_storage.update({worksheet.acell(letters[i]+str(j)).value : worksheet.acell(letters[i+1]+str(j)).value})

	#Converts the key and value into an object
	song_object = []
	for key in object_storage:
		#Creates an instance of the Song Object(Songname, lyrics)
		objects = song.Song(key, object_storage[key])
		song_object.append(objects)


	#Creating User Objects with parameters (userID, an instance of a song object)
	user_storage = {}
	for i in range(0,26,2):
		if worksheet.acell(letters[i]+"1").value == "":
				break
		else:
			for j in range(0, len(song_object)):
				#Make a dictionary {songname, user_id}, since keys must have unique values
				user_storage.update({song_object[j] : worksheet.acell(letters[i]+"1").value })
	user_object = []
	for key in user_storage:
		#Creates an instance of the User Object(UserID, Song Object)
		objects = user.User(user_storage[key], key)
		user_object.append(objects)


	song_list = ""
	#Check whether the sender_id is inside the user_object
	if len(user_object) == 0:
		return "You have not requested any songs from here"
	else:
		for i in range(0, len(user_object)):
			if user_object[i].senderid() == user_id:
				song_list = song_list + "\n" + user_object[i].song().songname() 
		return song_list
#user_song("1317527604947223")
		








	


















