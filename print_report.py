import sqlite3
import sys

def total_rows(cursor, table_name, print_out=False):
    """ Returns the total number of rows in the database """
    c.execute('SELECT COUNT(*) FROM {}'.format(table_name))
    count = c.fetchall()
    if print_out:
        print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]

def table_col_info(cursor, table_name, print_out=False):
    """ Returns a list of tuples with column informations:
        (id, name, type, notnull, default_value, primary_key)
    """
    c.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = c.fetchall()

    if print_out:
        print("\nColumn Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for col in info:
            print(col)
    return info

def values_in_col(cursor, table_name, print_out=True):
    """ Returns a dictionary with columns as keys and the number of not-null
        entries as associated values.
    """
    c.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = c.fetchall()
    col_dict = dict()
    for col in info:
        col_dict[col[1]] = 0
    for col in col_dict:
        c.execute('SELECT ({0}) FROM {1} WHERE {0} IS NOT NULL'.format(col, table_name))
        # In my case this approach resulted in a better performance than using COUNT
        number_rows = len(c.fetchall())
        col_dict[col] = number_rows
    if print_out:
        print("\nNumber of entries per column:")
        for i in col_dict.items():
            print('{}: {}'.format(i[0], i[1]))
    return col_dict

def report_data(c):
	#Total yield per week - sum of yield for all cows
	#select strftime('%W', measured_date) WeekNumber, max(date(measured_date, 'weekday 0', '-7 day')) WeekStart, max(date(measured_date, 'weekday 0', '-1 day')) WeekEnd, sum(daily_yield) as WeeklyYield, count(*) as GroupedValues from yieldinfo group by WeekNumber order by WeekNumber

	str ="select strftime('%W', measured_date) as WeekNumber, max(date(measured_date, 'weekday 0', '-7 day')) as WeekStart, "
	str = str+ "max(date(measured_date, 'weekday 0', '-1 day')) as WeekEnd, sum(daily_yield) as WeeklyYield "
	str = str+" from yieldinfo group by WeekNumber order by WeekStart desc"
	print (str)
	c.execute(str)
	d = c.description
	if not d:
		return "### NO RESULTS ###"
	print ('\nPer weekly yield\n') 
	print ("%s %s  %-10s %s" %(d[0][0],d[1][0], d[2][0], d[3][0]))
	info = c.fetchall()
	for WeekNumber, WeekStart, WeekEnd, WeeklyYield in info:
		print ("%10s %s %s %f\n" %(WeekNumber, WeekStart, WeekEnd, WeeklyYield))


	#Cow giving maximum yield per week
	#select strftime('%W', measured_date) WeekNumber, max(date(measured_date, 'weekday 0', '-7 day')) WeekStart, max(date(measured_date, 'weekday 0', '-1 day')) WeekEnd, max(daily_yield) as WeeklyYield, cow_id as Cow_ID from yieldinfo group by WeekNumber order by WeekStart desc, cow_id

	str="select strftime('%W', measured_date) WeekNumber, max(date(measured_date, 'weekday 0', '-7 day')) WeekStart, "
	str=str+"max(date(measured_date, 'weekday 0', '-1 day')) WeekEnd, max(daily_yield) as WeeklyYield, cow_id as cow_id "
	str=str+" from yieldinfo group by WeekNumber order by WeekStart desc, cow_id "
	c.execute(str)
	info = c.fetchall()

	d = c.description
	if not d:
		return "### NO RESULTS ###"
	print ('\nCow with highest Yield\n') 
	print ("%s %s  %-10s %s %s" %(d[0][0],d[1][0], d[2][0], d[3][0], d[4][0]))
	for WeekNumber, WeekStart, WeekEnd, WeeklyYield, CowID in info:
		print ("%10s %s %s %-11s %s\n" %(WeekNumber, WeekStart, WeekEnd, WeeklyYield, CowID))


	#Cow giving minumum yield per week
	str="select strftime('%W', measured_date) WeekNumber, max(date(measured_date, 'weekday 0', '-7 day')) WeekStart, "
	str=str+"max(date(measured_date, 'weekday 0', '-1 day')) WeekEnd, min(daily_yield) as WeeklyYield, cow_id as cow_id "
	str=str+" from yieldinfo group by WeekNumber order by WeekNumber desc, cow_id "
	c.execute(str)
	info = c.fetchall()
	d = c.description
	if not d:
		return "### NO RESULTS ###"
	print ('\nCow with lowest Yield\n')
	#print(info)
	print ("%s %s  %-10s %s %s" %(d[0][0],d[1][0], d[2][0], d[3][0], d[4][0]))
	for WeekNumber, WeekStart, WeekEnd, WeeklyYield, CowID in info:
		print ("%10s %s %s %-11s %s\n" %(WeekNumber, WeekStart, WeekEnd, WeeklyYield, CowID))

	#Cow giving yield less than 11 litres per day for more than 4 days in a week 
	#select strftime('%W', measured_date) WeekNumber, max(date(measured_date, 'weekday 0', '-7 day')) WeekStart, max(date(measured_date, 'weekday 0', '-1 day')) WeekEnd, sum(daily_yield), cow_id as cow_id from yieldinfo group by WeekNumber, cow_id having sum(daily_yield) < 45

	str="select strftime('%W', measured_date) WeekNumber, max(date(measured_date, 'weekday 0', '-7 day')) WeekStart, "
	str=str+"max(date(measured_date, 'weekday 0', '-1 day')) WeekEnd, sum(daily_yield) as WeeklyYield, cow_id as cow_id from yieldinfo "
	str=str+"group by WeekNumber, cow_id having sum(daily_yield) < 44"
	c.execute(str)
	info = c.fetchall()
	print ('\nCow with Yield less than 44 litres per week \n')
	#print(info)
	d = c.description
	if not d:
		return "### NO RESULTS ###"
	print ("%s %s  %-10s %s %s" %(d[0][0],d[1][0], d[2][0], d[3][0], d[4][0]))
	for WeekNumber, WeekStart, WeekEnd, WeeklyYield, CowID in info:
		print ("%10s %s %s %-11s %s\n" %(WeekNumber, WeekStart, WeekEnd, WeeklyYield, CowID))



def main():
	sqlite_file = 'cowinfo.db'


	db = sqlite3.connect(sqlite_file)
	c = db.cursor()
	
	#total_rows(c, table_name, print_out=True)
	#table_col_info(c, table_name, print_out=True)
	#values_in_col(c, table_name, print_out=True)
	report_data(c) 
	db.close()

if __name__ == '__main__':
	main()

