#!/usr/bin/env python

import sys
import time
import threading
import multiprocessing
import concurrent.futures
import queue

JOBCOUNT = 10
WORKCOUNT = 10_000_000

def main():
  timed(serial)
  timed(thread)
  timed(threadpool)
  timed(process)
  timed(processpool)

def timed(func):
  print('-----------------')
  print(func.__name__)
  begin = time.time()
  func()
  end = time.time()
  print(func.__name__, end-begin)

def work(i):
  print(i, 'start')
  result = sum(range(i, WORKCOUNT * JOBCOUNT, JOBCOUNT))
  print(i, 'done')
  return (i, result)

def workresults(i, results):
  iresult = work(i)
  results.put(iresult)

def serial():
  for i in range(1, JOBCOUNT):
    i, result = work(i)
    print(i, result)

def thread():
  results = queue.Queue()
  jobs = []
  for i in range(1, JOBCOUNT):
    job  = threading.Thread(target=workresults, args=(i, results))
    job.start()
    jobs.append(job)
  for job in jobs:
    job.join()
    i, result = results.get()
    print(i, result)

def threadpool():
  with concurrent.futures.ThreadPoolExecutor() as executor:
     for i, result in executor.map(work, range(1, JOBCOUNT)):
       print(i, result)

def process():
  results = multiprocessing.Queue()
  jobs = []
  for i in range(1, JOBCOUNT):
    job  = multiprocessing.Process(target=workresults, args=(i, results))
    job.start()
    jobs.append(job)
  for job in jobs:
    job.join()
    i, result = results.get()
    print(i, result)

def processpool():
  with concurrent.futures.ProcessPoolExecutor() as executor:
     for i, result in executor.map(work, range(1, JOBCOUNT)):
       print(i, result)

if __name__ == '__main__':
  main()
