import requests
import random
import string
import sqlite3
import time

def make_db(): # creates database
	db = "results.db"
	con = sqlite3.connect(db)
	cursor = con.cursor()

	cursor.execute("""CREATE TABLE IF NOT EXISTS students(uid INTEGER,
				sid INTEGER,
				yeargroup TEXT,
				title TEXT,
				firstname TEXT,
				surname TEXT,
				type TEXT,
				email TEXT,
				lastlogin FLOAT,
				totalpoints TeXT,
				totalpointsthisyear TEXT,
				numquestions INTEGER,
				numpracquestions INTEGER,
				topicmedals INTEGER,
				unsubscribed INTEGER,
				totalwatch INTEGER,
				googlesso,
				office365,
				ctext STRING,
				globalrank INTEGER,
				UNIQUE(uid))""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS teachers(
				uid INTEGER,
				sid INTEGER,
				title TEXT,
				firstname TEXT,
				surname TEXT,
				type TEXT,
				email TEXT,
				lastlogin FLOAT,
				totalpoints TEXT,
				totalpointsthisyear TEXT,
				numquestions INTEGER,
				numpracquestions INTEGER,
				topicmedals INTEGER,
				totalwatch INTEGER,
				ctext TEXT,
				globalrank INTEGER,
				acid,
				isExamBoard,
				useMarks,
				la,
				_school,
				classes,
				UNIQUE(uid))""")
	con.commit()
	con.close()
	return

def create_account_in_school(sid,class_id,session):
	# account_info = [firstname,surname,email]
	account_info = [f"{''.join(random.choices(string.ascii_lowercase, k=6))}",f"{''.join(random.choices(string.ascii_lowercase, k=9))}",f"{''.join(random.choices(string.ascii_letters, k=10))}@a.com"]
	url = "https://www.drfrost.org/api/auth/register/manual"
	payload = {"firstname":f"{account_info[0]}","surname":f"{account_info[1]}","email":f"{account_info[2]}","type":"teacher","cid":f"{class_id}","sid":sid}
	headers = {"Cookie":f"""hideCookieConsent=true; _gcl_au=1.1.408609082.1728459849; PHPSESSID={session}; GCLB=CIzHk6SoxvDF7wEQAw; ph_phc_wu5uBJqblldYE2xTOYYttsQaxd9dDHex41m4VV5QET2_posthog=%7B%22distinct_id%22%3A%2201918e72-ef93-7091-86aa-556f5d055c05%22%2C%22%24sesid%22%3A%5B1731418066926%2C%2201932053-a285-7cf1-814d-3d5c3e28d9a5%22%2C1731414172292%5D%7D"""}
	r = requests.post(url=url,headers=headers,json=payload)

	# if the school doesnt have a subscription
	if r.text.replace("\n", "") == """{    "message": "REQUIRE_SUBSCRIPTION",    "data": null}""":
		return False
	
	if r.status_code == 200:
		return account_info
	elif r.status_code == 500:
		return 500
	else:
		print(f"{r.status_code} recieved when creating account. Quitting...")
		print(r.text)
		quit()

def get_children(session):
	url = "https://www.drfrost.org/api/class/class/children"
	headers = {"Cookie":f"""hideCookieConsent=true; _gcl_au=1.1.408609082.1728459849; PHPSESSID={session}; GCLB=CIzHk6SoxvDF7wEQAw; ph_phc_wu5uBJqblldYE2xTOYYttsQaxd9dDHex41m4VV5QET2_posthog=%7B%22distinct_id%22%3A%2201918e72-ef93-7091-86aa-556f5d055c05%22%2C%22%24sesid%22%3A%5B1731418066926%2C%2201932053-a285-7cf1-814d-3d5c3e28d9a5%22%2C1731414172292%5D%7D"""}
	children = requests.get(url=url,headers=headers).json()["classGrouping"]["_students"]
	children_data = [f'{r["uid"]}|{r["firstname"]}|{r["surname"]}|{r["email"]}'.split("|") for r in children]
	c_uid_only = [r["uid"] for r in children]
	return children_data,c_uid_only

def activate_accounts(uid_list,session):
	url = "https://www.drfrost.org/api/users/activate"
	payload = {"uids":[uid for uid in uid_list]}
	headers = {"Cookie":f"""hideCookieConsent=true; _gcl_au=1.1.408609082.1728459849; PHPSESSID={session}; GCLB=CIzHk6SoxvDF7wEQAw; ph_phc_wu5uBJqblldYE2xTOYYttsQaxd9dDHex41m4VV5QET2_posthog=%7B%22distinct_id%22%3A%2201918e72-ef93-7091-86aa-556f5d055c05%22%2C%22%24sesid%22%3A%5B1731418066926%2C%2201932053-a285-7cf1-814d-3d5c3e28d9a5%22%2C1731414172292%5D%7D"""}
	r = requests.patch(url=url,json=payload,headers=headers)
	if r.status_code == 200:
		return
	else:
		print(f"{r.status_code} recieved when activating account. Quitting...")
		print(r.text)
		quit()

def delete_accounts(uid_list,session):
	url = "https://www.drfrost.org/api/users"
	payload = {"uids":[uid for uid in uid_list]}
	headers = {"Cookie":f"""hideCookieConsent=true; _gcl_au=1.1.408609082.1728459849; PHPSESSID={session}; GCLB=CIzHk6SoxvDF7wEQAw; ph_phc_wu5uBJqblldYE2xTOYYttsQaxd9dDHex41m4VV5QET2_posthog=%7B%22distinct_id%22%3A%2201918e72-ef93-7091-86aa-556f5d055c05%22%2C%22%24sesid%22%3A%5B1731418066926%2C%2201932053-a285-7cf1-814d-3d5c3e28d9a5%22%2C1731414172292%5D%7D"""}
	r = requests.delete(url=url,json=payload,headers=headers)
	if r.status_code == 200:
		return
	else:
		print(f"{r.status_code} recieved when deleting account. Quitting....")
		print(r.text)
		quit()


def login_and_get_session(email):
	url = "https://www.drfrost.org/api/auth/login/"
	payload = {"email": email, "password": "password"}
	r = requests.post(url=url,json=payload)
	heads = dict(r.headers)
	try:
		cookies = heads["Set-Cookie"].split(";")
		for i in cookies:
			if "PHPSESSID" in i:
				session = i.split("=")[1]
				return session
			else:
				pass
	except:
		return "Something failed when getting session."

def get_all_students(session):
	#gets all classes using teacher session in the school
	get_classes = "https://www.drfrost.org/api/class/get_school_classes?repeatUserClassGroups=true&_=1731535236919"
	headers = {"Cookie":f"""hideCookieConsent=true; _gcl_au=1.1.408609082.1728459849; PHPSESSID={session}; GCLB=CIzHk6SoxvDF7wEQAw; ph_phc_wu5uBJqblldYE2xTOYYttsQaxd9dDHex41m4VV5QET2_posthog=%7B%22distinct_id%22%3A%2201918e72-ef93-7091-86aa-556f5d055c05%22%2C%22%24sesid%22%3A%5B1731418066926%2C%2201932053-a285-7cf1-814d-3d5c3e28d9a5%22%2C1731414172292%5D%7D"""}
	rc = requests.get(url=get_classes,headers=headers).text
	#parses the classes to get all the class ids
	nrc = rc.replace("},{", "|").replace("cid:", "|").replace(',"', "|").split("|")
	class_ids = [cid.split(":")[1] for cid in nrc if '"cid"' in cid]
	class_ids = class_ids[1:]

	# connects to db
	con = sqlite3.connect("results.db")
	cur = con.cursor()

	#gets all records, then splits them into teachers and students, then adds most info to db.
	for cid in class_ids:
		class_url = f"https://www.drfrost.org/api/class/class/{cid}"
		try:
			class_req = requests.get(url=class_url,headers=headers).json()["classGrouping"]
		except KeyError:
			print("KeyError occured")
		students = class_req["_students"]
		teachers = class_req["_teachers"]
		wanted_keys_students = ["uid", "sid", "yeargroup", "title", "firstname", "surname", "type", "email", "lastlogin", "totalpoints", "totalpointsthisyear", "numquestions", "numpracquestions", "topicmedals", "unsubscribed", "totalwatch", "ctext", "globalrank"]
		wanted_keys_teachers = ["uid", "sid", "title", "firstname", "surname", "type", "email", "lastlogin", "totalpoints", "totalpointsthisyear", "numquestions", "numpracquestions", "topicmedals", "totalwatch", "ctext", "globalrank", "acid", "isExamBoard", "useMarks", "la", "_school", "classes"]
		for record in students:
			wanted_values = [record.get(i) for i in record.keys() if i in wanted_keys_students]
			wanted_values = ["None" if i==None else i for i in wanted_values]

			con.execute("INSERT OR IGNORE INTO students(uid, sid, yeargroup, title, firstname, surname, type, email, lastlogin, totalpoints, totalpointsthisyear, numquestions, numpracquestions, topicmedals, unsubscribed, totalwatch, ctext, globalrank) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",wanted_values)
			#print(f"Inserted student {record['firstname']} {record['surname']}")

		for record in teachers:
			wanted_values = [record.get(i) for i in record.keys() if i in wanted_keys_teachers]
			wanted_values = ["None" if i==None else i for i in wanted_values]

			con.execute("INSERT OR IGNORE INTO teachers(uid, sid, title, firstname, surname, type, email, lastlogin, totalpoints, totalpointsthisyear, numquestions, numpracquestions, topicmedals, totalwatch, ctext, globalrank, acid, isExamBoard, useMarks, la, _school, classes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",wanted_values)
			print(f"Inserted teacher {record['firstname']} {record['surname']}")

	con.commit()
	con.close()
	#uid, sid, yeargroup, title, firstname, surname, type, email, lastlogin, totalpoints, totalpointsthisyear, numquesions, numpracquestions, topicmedals, unsubscribed, totalwatch, ctext, globalrank 
	#students(uid,sid,yeargroup,title,firstname,surname,type,email,lastlogin,totalpoints,totalpointsthisyear,numquesions)
	#
	return



if __name__ == "__main__":

	# input your own CLASS ID and MAIN SESSION values!
	CLASS_ID = 391419
	MAIN_SESSION = "9l8lvvv9cv19ru75q80bj6u1cp"

	make_db()
	for i in range(0,36914):
		account_data = create_account_in_school(sid=i,class_id=CLASS_ID,session=MAIN_SESSION) #[firstname,surname,email]
		if account_data == False:
			continue
		elif account_data == 500:
			print("You have been rate limited! Sleeping 120 secconds...")
			time.sleep(120)
		all_children,child_uids = get_children(MAIN_SESSION)
		for child in all_children:
			if account_data[0] and account_data[1] not in child:
				pass
			else:
				cuid = child[0]
			activate_accounts(child_uids,MAIN_SESSION)
			child_session = login_and_get_session(account_data[2])
			get_all_students(child_session)
			delete_accounts(child_uids,MAIN_SESSION)
		print(f"School of id {i} has been scraped successfully.")
