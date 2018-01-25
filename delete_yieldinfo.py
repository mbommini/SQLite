import sqlite3
import sys
import datetime
import time

def main():
	try:
		db = None
		db = sqlite3.connect('cowinfo.db')
		cur = db.cursor()
				
		str='SELECT count(1) FROM sqlite_master WHERE type=\'table\' AND name='
		table_name = '\'yieldinfo\''
		str=str+table_name 
		cur.execute(str)
		data = cur.fetchone()
		if (data[0] == 0): 
			print ('Table %s does not exist. Run setupherdprofile program' %(table_name))
			sys.exit(1)

		# Query used to update the measured_date is 
		# update yieldinfo set measured_date = datetime(substr(measured_date, 7, 4) || '-' || substr(measured_date, 4, 2) || '-' ||substr(measured_date, 1, 2)) where measured_date not between '2017-12-21' and '2017-12-26'

		delete_all_from_daily_yield(cur)
		db.commit()	

	except ValueError:
		print ('Could not convert data to an integer.')

	finally:
		if db:
			db.close()



def delete_all_from_daily_yield(cur):
	str='DELETE FROM yieldinfo'
	print ('SQL string %s' %str)
	cur.execute(str)
		

if __name__== "__main__":
	main()


