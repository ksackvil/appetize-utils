
import json

def parseTxt(inputFile):
    try:
        with open(inputFile) as f:
            lineCount = 0
            names = []
            locations = []
            radius = []

            # read initial line
            line = f.readline()
            while line:
                if(line[0] != '#'):
                    tempName = ''
                    tempLoc = ''
                    tempRad = ''

                    line = line.strip()
                    tempName, tempLoc, tempRad = line.split('|')

                    names.append(tempName)
                    locations.append(tempLoc)
                    radius.append(tempRad)

                    lineCount+=1
                
                # Read next line
                line = f.readline()
            
            if(unitTestTxt(names, locations, radius)):
                return(names, locations, radius)
            else:
                print('ERROR: input text data mutated')
    except:
        print("ERROR: unable to open file.")

def parseJson(inputFile):
    parsedList = []

    try:
        with open(inputFile) as f:
            data = json.load(f)

            for obj in data:
                tempObj = {}
                tempObj['photo_reference'] = []
                tempObj['google_id'] = obj['google_id']

                for photo in obj['photos']:
                    tempObj['photo_reference'].append(photo['photo_reference'])

                parsedList.append(tempObj)

        return(parsedList)
    except:
        print("ERROR: unable to open file.")

def unitTestTxt(n, l, r):
    array_length_test = False
    final_result = False

    if(len(n) == len(l) == len(r)):
        array_length_test = True

    if(array_length_test):
        final_result = True

    return(final_result)