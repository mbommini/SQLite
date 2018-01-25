import sqlite3
import sys
from datetime import date, datetime
import datetime
# Refer the code at https://gist.github.com/liuyix/6019171

def main():
	try:
		db = None
		db = sqlite3.connect('cowinfo.db')
		cur = db.cursor()
		str='SELECT count(1) FROM sqlite_master WHERE type=\'table\' AND name='
		table_name = '\'herdprofile\''
		str=str+table_name 
		cur.execute(str)
		data = cur.fetchone()
		if (data[0] == 0): 
			print ('Table %s does not exist. Run setupherdprofile program' %(table_name))
			sys.exit(1)
				
		str='SELECT count(1) FROM sqlite_master WHERE type=\'table\' AND name='
		table_name = '\'yieldinfo\''
		str=str+table_name 
		cur.execute(str)
		data = cur.fetchone()
		if (data[0] == 0): 
			print ('Table %s does not exist. Run setupherdprofile program' %(table_name))
			sys.exit(1)

		str='SELECT count(1) FROM '
		table_name = 'herdprofile'
		str=str+table_name
		cur.execute(str)
		data = cur.fetchone()
		#print ('Record count in table %s is %s ' %(table_name, data[0]))
		if (data[0] == 0): 
			print ('Table %s does not have data. Run setupherdprofile program' %(table_name))
			sys.exit(1)

	
		# Get various cow_id from herdprofile 
		cow_id_list=get_cow_ids(cur)

		# Get the date for which data entry has to be done 
		date_str = get_day_of_yield(cur)

		verify_data_exists_for_this_date(cur, date_str)

		populate_daily_yield(cur, cow_id_list, date_str)
		db.commit()

	except ValueError as e:
		print (e)
	except sqlite3.IntegrityError:
		print ('Integrity Error')

	finally:
		if db:
			db.close()


def verify_data_exists_for_this_date(cur, date_str):
	# If the milk yield is existing in the table for the cow, then error is raised to avoid duplicates
	
	#Get already existing yieldinfo so that we can check before insert
	str='SELECT COUNT(1) FROM yieldinfo WHERE measured_date='
	str=str+'\''+date_str+'\''
	print(str)
	cur.execute(str)
	existing_cow_yield = cur.fetchone()
	exists = existing_cow_yield[0]
	if (exists > 0):
		print('Yield information is already existing. Hence exiting')
		sys.exit(1) 


def populate_daily_yield(cur, cow_id_list, date_str):
	# Program to insert the yield data into the table for a date and all cows in the herdprofile

	for cowid in (cow_id_list):
		print('Enter milk yield for cow ID %d ' %(cowid[0]))
		#cow_id = int(input("Enter cow id"))
		cow_id = cowid[0]

		yield1=float(input("Enter morning yield for cow in litres correct to one decimal place"))
		yield1 = round(yield1,1)
		yield2=float(input("Enter evening yield for cow in litres correct to one decimal place"))
		yield2 = round(yield2,1)
		daily_yield=yield1+yield2
		cowdata = (cow_id, daily_yield, date_str)
		str='''INSERT INTO yieldinfo(cow_id, daily_yield, measured_date) VALUES(?,?,?)'''
		cur.execute("INSERT INTO yieldinfo(cow_id, daily_yield, measured_date) VALUES(?,?,?)", cowdata)


def get_cow_ids(cur):
	#Get existing cow_id from herdprofile
	str='SELECT cow_id FROM herdprofile'
	cur.execute(str)

	# Cow_id_list in tuple
	cow_id_list = cur.fetchall()
	return cow_id_list	

def validate_date(date_text):
	try:
		datetime.datetime.strptime(date_text, '%Y-%m-%d')
	except ValueError:
		raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def get_day_of_yield(cur):
	today = date.today()
	date_str=str(input("Enter date of milk yield measure in YYYY-MM-DD format"))
	validate_date(date_str)
	if (date_str == None):
		print ('Invalid Date given. Exiting program')
		sys.exit(1)
	elif (len(date_str) != 10):	
		print ('Invalid Date, not in YYYY-MM-DD format')
		date_str = None
		get_day_of_yield(date_str)
	return date_str


if __name__== "__main__":
	main()


