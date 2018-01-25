import sqlite3

def insert_dummy_data(cursor):
	#c.execute("insert into yieldinfo select cow_id, daily_yield + 1, date(measured_date, '+1 day') from yieldinfo where measured_date = date('2017-12-18')")
	#c.execute("insert into yieldinfo select cow_id, daily_yield + 1 as daily_yield, date('2017-12-18', 'start of day', '+1 days')  measured_date from yieldinfo where measured_date = '18-12-2017'");
	#c.execute("insert into yieldinfo select cow_id, daily_yield + 0.5 as daily_yield, date('2017-12-18', 'start of day', '+2 days')  measured_date from yieldinfo where measured_date = '18-12-2017'");
	#c.execute("insert into yieldinfo select cow_id, daily_yield + 0.25 as daily_yield, date('2017-12-18', 'start of day', '+3 days')  measured_date from yieldinfo where measured_date = '18-12-2017'");
	#c.execute("insert into yieldinfo select cow_id, daily_yield - 0.25 as daily_yield, date('2017-12-18', 'start of day', '+4 days')  measured_date from yieldinfo where measured_date = '18-12-2017'");
	#c.execute("insert into yieldinfo select cow_id, daily_yield - 0.5 as daily_yield, date('2017-12-18', 'start of day', '+5 days')  measured_date from yieldinfo where measured_date = '18-12-2017'");
	#c.execute("insert into yieldinfo select cow_id, daily_yield - 0.75 as daily_yield, date('2017-12-18', 'start of day', '+6 days')  measured_date from yieldinfo where measured_date = '18-12-2017'");
	#c.execute("insert into yieldinfo select cow_id, daily_yield - 0.15 as daily_yield, date('2017-12-18', 'start of day', '+7 days')  measured_date from yieldinfo where measured_date = '18-12-2017'");




if __name__ == '__main__':

    sqlite_file = 'cowinfo.db'
    table_name = 'yieldinfo'

    conn, c = connect(sqlite_file)


    insert_dummy_data(c)
    conn.commit()	 
    close(conn)