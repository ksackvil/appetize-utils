import json
import argparse

# Returns list loaded from json file
def jsonToList(inFile: str):
    ret = []

    with open(inFile, 'r') as file:
        nameList = json.load(file)

    for name in nameList:
        ret.append(name)

    return ret

# Writes tempList to json file specified in inFile
def listToJson(inFile: str, inList: list):
    with open(inFile, 'w') as file:
        json.dump(inList, file)

# Sorts input list alphabetically
def sortList(inList: list):
    inList.sort()

    return inList

if __name__ == "__main__":
    # ===== CONFIG VARS ===== #
    # JSON file to edit/read
    jsonFile = 'vantablacklist.json' 
    # ======================= #

    parser = argparse.ArgumentParser(description="Mutate data files based on provide action flags.")
    parser.add_argument("-s", "--sort", help="Sorts default json file in alphabetical order", action="store_true")
    
    args = parser.parse_args()

    if args.sort:
        listToJson(jsonFile, sortList(jsonToList(jsonFile)))
        print("'"+jsonFile+"' successfully sorted")
    else:
        print("No action invoked, run with -h flag to see available actions")



