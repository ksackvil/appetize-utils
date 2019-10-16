import firebase as fb
import scraper
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
from data_parser import parse

OUTFILE_FOLDER = './output_data/'
OUTFILE_EXT = '.json'
INPUT_FOLDER = './input_data'
DEVELOPER_LOGS = True
OVERWITE_EXISTING = False

print('\n')
print('(c) Google Places Scraper, Developed by Kai Sackville-Hii.')
print('Program initialized with the following parameters:')
print('\tOUTFILE_FOLDER = '+OUTFILE_FOLDER)
print('\tOUTFILE_EXT = '+OUTFILE_EXT)
print('\tDEVELOPER_LOGS = '+str(DEVELOPER_LOGS))
print('\tOVERWITE_EXISTING = '+str(OVERWITE_EXISTING))
print('\n')

for filename in os.listdir(INPUT_FOLDER):
    subfolder = filename.split('.')[0]+'/'

    outfile_name, location, radius = parse(INPUT_FOLDER+'/'+filename)
    if DEVELOPER_LOGS: print('>> '+' ----- '+filename+' ----- ')

    for index in range(0, len(outfile_name)):
        # create subfolder if it DNE
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