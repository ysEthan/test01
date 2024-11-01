from datetime import datetime, timedelta
import pandas as pd 

def this_week(day):
    # day = datetime.strptime(str(day), "%Y/%m/%d")
    week=day.strftime('%W')
    date_range=datetime.strftime(day - timedelta(day.weekday()), "%m/%d")+datetime.strftime(day - timedelta(day.weekday()-6), "~%d")

    return 'WK'+week+'_'+date_range

if __name__ == '__main__':
	today = datetime.strptime('2023-04-08', "%Y-%m-%d")
	print(this_week(today))