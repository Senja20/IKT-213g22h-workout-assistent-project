import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates
import matplotlib.dates as mdates
import pandas as pd


from datetime import datetime

if __name__ == "__main__":
    con = sqlite3.connect("records.db")
    cur = con.cursor()

    date_points = []
    reps = []
    for row in cur.execute("SELECT * FROM logs"):
        print(row[0])
        print(row[1])

        #date_points.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').date())
        date_points.append(pd.to_datetime(row[0]))
        reps.append(int(row[1]))


    dates = matplotlib.dates.date2num(date_points)
    #matplotlib.pyplot.plot_date(dates, reps)

    plt.scatter(date_points, reps)
    plt.title("Data")
    plt.xlabel("dates")
    plt.ylabel("number of push ups")
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.show()
    plt.close()