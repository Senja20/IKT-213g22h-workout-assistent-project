import matplotlib.dates  # type: ignore
import matplotlib.dates as mdates
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore

from datebase.connect import connect_to_db  # type: ignore

if __name__ == "__main__":
    cur, con = connect_to_db()

    date_points = []
    reps = []

    for row in cur.execute("SELECT * FROM logs"):
        date_points.append(pd.to_datetime(row[0]))
        reps.append(int(row[1]))

    dates = matplotlib.dates.date2num(date_points)

    plt.scatter(date_points, reps)
    plt.title("Push Ups")
    plt.xlabel("Dates")
    plt.ylabel("number of push ups")
    plt.gcf().autofmt_xdate()
    plt.tick_params(rotation=45)
    plt.show()
    plt.close()
