import time
import datetime

def daysUntil(xDay):
    today = datetime.date.today()
    diff = xDay-today
    return diff.days

def main():
    print("{} days until freedom, SON!".format(daysUntil(datetime.date(2019,5,1))))
    time.sleep(60)
    exit(0)
	
if __name__ == "__main__":
    main()
