
import schedule
import time

txt=[1,2,3]
def job(t):
    print ("I'm working...", t)

def nob():
    print("ZZZ")

def abc():
    print("abc")

def add():
    print(txt)

runtime = "05:48"
schedule.every().day.at(runtime).do(job,'It is 05:04')
schedule.every().day.at(runtime).do(nob)
schedule.every().day.at(runtime).do(abc)
schedule.every().day.at(runtime).do(add)

while True:
    schedule.run_pending()
    time.sleep(10) # wait one minute