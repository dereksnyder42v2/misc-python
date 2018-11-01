
import datetime
import time

input('Press ENTER to begin lunchbreak countdown.')

startTimeM = datetime.datetime.now().minute
startTimeH = datetime.datetime.now().hour

#endTimeM = (startTimeM + 30)% 60
endTimeM = (startTimeM + 10)% 60
endTimeH = (startTimeH) + (startTimeM + 30)//60
if endTimeH > 12:
    endTimeH -= 12

#print('Break is over at', str(endTimeH), ':', str(endTimeM) )
print('\nBreak is over at {:d}:{:02d}'.format(endTimeH, endTimeM))
time.sleep(30*60)
print('\nYou can clock in now.')
