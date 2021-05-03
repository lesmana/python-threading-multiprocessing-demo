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
  serial()
  thread()
  threadpool()
  process()
  processpool()

def work(i):
  print(i, 'start')
  result = sum(range(i, WORKCOUNT * JOBCOUNT, JOBCOUNT))
  print(i, 'done')
  return (i, result)

def workresults(i, results):
  iresult = work(i)
  results.put(iresult)

def serial():
  print('-----------------')
  print('serial')
  begin = time.time()
  for i in range(1, JOBCOUNT):
    i, result = work(i)
    print(i, result)
  end = time.time()
  print('serial: ', end-begin)

def thread():
  print('-----------------')
  print('thread')
  begin = time.time()
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
  end = time.time()
  print('thread: ', end-begin)

def threadpool():
  print('-----------------')
  print('threadpool')
  begin = time.time()
  with concurrent.futures.ThreadPoolExecutor() as executor:
     for i, result in executor.map(work, range(1, JOBCOUNT)):
       print(i, result)
  end = time.time()
  print('threadpool: ', end-begin)

def process():
  print('-----------------')
  print('process')
  begin = time.time()
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
  end = time.time()
  print('process: ', end-begin)

def processpool():
  print('-----------------')
  print('processpool')
  begin = time.time()
  with concurrent.futures.ProcessPoolExecutor() as executor:
     for i, result in executor.map(work, range(1, JOBCOUNT)):
       print(i, result)
  end = time.time()
  print('processpool: ', end-begin)

if __name__ == '__main__':
  main()
