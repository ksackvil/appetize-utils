import firebase as fb
import scraper
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
from data_parser import parseTxt
import threading
import time
import queue

# Global variables
global PROCESS_ALIVE

OUTFILE_FOLDER = './output_data/'
OUTFILE_EXT = '.json'
INPUT_FOLDER = './input_data'
DEVELOPER_LOGS = True               # controls console output
OVERWITE_EXISTING = False           # if true exiting output files will be overwritten, default false (skips existing files)
PROCESS_ALIVE = True                # controls if scrapping process is alive

BUF_SIZE = 100                      # max number of elements in the queue
q = queue.Queue(BUF_SIZE)           # data queue connecting producer and consumer

class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        global PROCESS_ALIVE

        # Iterate through each input file in INPUT_FOLDER location
        for filename in os.listdir(INPUT_FOLDER):
            subfolder = filename.split('.')[0]+'/'

            outfile_name, location, radius = parseTxt(INPUT_FOLDER+'/'+filename)
            if DEVELOPER_LOGS: print('>> '+' ----- '+filename+' ----- ')

            # Iterate each valid line of input file
            for index in range(0, len(outfile_name)):

                # create output subfolder if it DNE
                if not os.path.exists(OUTFILE_FOLDER):
                    if DEVELOPER_LOGS: print('>> ALERT: '+OUTFILE_FOLDER+' does not exits. Creating folder.')
                    os.mkdir(OUTFILE_FOLDER)

                # create output subfolder if it DNE
                if not os.path.exists(OUTFILE_FOLDER+subfolder):
                    if DEVELOPER_LOGS: print('>> ALERT: '+subfolder+' does not exits in ' + OUTFILE_FOLDER+'. Creating folder.')
                    os.mkdir(OUTFILE_FOLDER+subfolder)
                    
                # Clean existing files
                if os.path.exists(OUTFILE_FOLDER+subfolder+outfile_name[index]+OUTFILE_EXT):
                    if OVERWITE_EXISTING:
                        if DEVELOPER_LOGS: print('>> ALERT: '+outfile_name[index]+OUTFILE_EXT+' exits in' + OUTFILE_FOLDER+'. Removing file.')
                        os.remove(OUTFILE_FOLDER+subfolder+outfile_name[index]+OUTFILE_EXT)
                    else:
                        if DEVELOPER_LOGS: print('>> ALERT: '+outfile_name[index]+OUTFILE_EXT+' exits in' + OUTFILE_FOLDER+'. Skipping file.')
                        continue
                
                # get the restaurant list from scraper.py
                if DEVELOPER_LOGS: print('>> '+outfile_name[index]+' | '+ location[index]+' | '+radius[index])
                restaurants = scraper.getData(location[index], radius[index])

                # Write each result to json file
                with open(OUTFILE_FOLDER+subfolder+outfile_name[index]+OUTFILE_EXT, 'a+') as f:
                    # counter for for loop
                    count = 0
                    f.write('[')

                    for restaurant in restaurants:
                        if(count != 0):
                            f.write(',')

                        json.dump(restaurants[count].to_dict(), f)
                        count += 1

                    f.write(']')
                    
                    if DEVELOPER_LOGS: print('>> '+'Wrote '+str(count)+' places to '+outfile_name[index]+OUTFILE_EXT)
                    f.close()
                    
                    # count for full queue exception
                    timeoutCount = 0

                    # if queue is full pause thread.
                    while q.full():
                        if DEVELOPER_LOGS: print('>> '+'Data queue is full, pausing producer thread for 30 seconds.')

                        if(timeoutCount > 120):
                            if DEVELOPER_LOGS: print('>> '+'ERROR: Producer timed out, queue has been full for 1 hour.')
                            PROCESS_ALIVE = False
                            return

                        time.sleep(30)

                    # add newley edited output file to queue for consumer
                    q.put(OUTFILE_FOLDER+subfolder+outfile_name[index]+OUTFILE_EXT)
                
        PROCESS_ALIVE = False
        return

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        global PROCESS_ALIVE
        while True:
            if not q.empty():
                inFile = q.get()

                if DEVELOPER_LOGS: print('>> '+'Fetching images for'+inFile)
                photoCount = scraper.getImages(inFile)
                if DEVELOPER_LOGS: print('>> '+str(photoCount)+' photos fetched for '+inFile)

            elif not PROCESS_ALIVE:
                break
        return

def main():
    # Welcome message
    print('\n')
    print('(c) Google Places Scraper, Developed by Kai Sackville-Hii.')
    print('Program initialized with the following parameters:')
    print('\tOUTFILE_FOLDER = '+OUTFILE_FOLDER)
    print('\tOUTFILE_EXT = '+OUTFILE_EXT)
    print('\tDEVELOPER_LOGS = '+str(DEVELOPER_LOGS))
    print('\tOVERWITE_EXISTING = '+str(OVERWITE_EXISTING))
    print('\n')

    # threaded class'
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    #  start thread classes
    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)

if __name__ == "__main__":
    main()