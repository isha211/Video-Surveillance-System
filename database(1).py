import pymysql
import random
from datetime import datetime,timedelta

#Uses config database to access video links
def getVideoLinks():
    con1 = pymysql.connect(
        host="localhost",
        user="crowdcounter",
        password="counting",
        database="config",
    )
    with con1:
        cur = con1.cursor()
        query = "select ip,username,passwd,port_no,dbname from camera_config"
        cur.execute(query)
        rows = cur.fetchall()
        linkarray = []
        for row in rows:
            print(row)
            temp = "rtsp://{}:{}@{}:{}/Streaming/Channels/102".format(row[1], row[2], row[0],
                                                                      row[3])
            linkarray.append(temp)
        return linkarray

class db:
    #Initialses using the name of the database
    def __init__(self,_str):
        self.con=pymysql.connect(
            host="localhost",
            user="crowdcounter",
            password="counting",
            database=_str,
        )

    #Function used to insert data
    def InsertData(self):
        basedate = datetime(2020, 1, 5, 0, 0, 0)

        with self.con:
            cur=self.con.cursor()
            while True:
                count = random.randint(1, 15)
                datestr = str(basedate)
                cur.execute("Insert into recorded_counts(timestamp,count_discrete) values(%s,%s)",(datestr,str(count)))
                basedate = basedate + timedelta(minutes=30)
                if basedate.month == 5:
                    break

    #Returns hourly data between two dates
    def hourlyCount(self,date1,date2):
        with self.con:
            cur=self.con.cursor()
            query='select sum(count_discrete), DATE_FORMAT(timestamp,"%d %H:00") from recorded_counts where DATE(timestamp) between'+date1+'and'+date2+'group by DATE_FORMAT(timestamp, "%d %H:00") ;'
            cur.execute(query)
            rows=cur.fetchall()
            hourlist=[]
            for row in rows:
                hourlist.append(row)
            return hourlist

    #Returns monthly data between two dates
    def monthlyCount(self,date1,date2):
        with self.con:
            cur = self.con.cursor()
            query = 'select sum(count_discrete),DATE_FORMAT(timestamp,"%Y-%m") from recorded_counts where DATE(timestamp) between ' + date1 + 'and ' + date2 + 'group by DATE_FORMAT(timestamp, "%Y-%m");'
            cur.execute(query)
            rows = cur.fetchall()
            daylist = []
            for row in rows:
                daylist.append(row)
            return daylist

    # Returns weekly data between two dates
    def weeklyCount(self,date1,date2):
        with self.con:
            cur=self.con.cursor()
            query='select sum(count_discrete),DATE_FORMAT(timestamp,"%Y-%m-%d") from recorded_counts where DATE(timestamp) between ' + date1 + 'and '+date2+ 'group by DATE_FORMAT(timestamp, "%Y-%m-%d");'
            cur.execute(query)
            rows=cur.fetchall()
            daylist=[]
            for row in rows:
                daylist.append(row)
            return daylist

    # Returns data for current date
    def currentdata(self):
        with self.con:
            cur=self.con.cursor()
            query='select sum(count_discrete), DATE_FORMAT(timestamp,"%d %H:00") from recorded_counts where DATE(timestamp) = curdate() group by DATE_FORMAT(timestamp, "%d %H:00") ;'
            cur.execute(query)
            rows=cur.fetchall()
            hourlist=[]
            for row in rows:
                hourlist.append(row)
            return hourlist

    #Returns data for the week of that particular date
    def weekdata(self,date):
        with self.con:
            cur = self.con.cursor()
            query = 'select sum(count_discrete),DATE_FORMAT(timestamp,"%Y-%m-%d") from recorded_counts where weekofyear(date(timestamp)) = weekofyear('+date+ ') group by DATE_FORMAT(timestamp, "%Y-%m-%d");'
            cur.execute(query)
            rows = cur.fetchall()
            hourlist = []
            for row in rows:
                hourlist.append(row)
            return hourlist

    # Returns data for the month of that particular date
    def monthdata(self,date):
        with self.con:
            cur = self.con.cursor()
            query = 'select sum(count_discrete),DATE_FORMAT(timestamp,"%Y-%m-%d") from recorded_counts where year(date(timestamp)) = year('+date+ ') and month(date(timestamp))=month(' +date+')group by DATE_FORMAT(timestamp, "%Y-%m-%d");'
            cur.execute(query)
            rows = cur.fetchall()
            hourlist = []
            for row in rows:
                hourlist.append(row)
            return hourlist