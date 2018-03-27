import json
from pprint import pprint  #  essential for debugging

'''
S2
All customers details should be saved together (names, phone number, email address, DoB) Customer ID will be the key and then the details will be attached as subheadings in the file.
S6
Sorting and searching needs to be quick enough to not cause any loss to the company's efficiency, if the file is too large then use a quicksort.
I4
ID will be automatically entered to avoid errors
P2
When adding anything to files it will be given a new ID if it doesn't have one already. This will involve adding one to the current maximum ID and then this being added to the JSON files.
P10
Searching a listview will use a linear/binary search.
'''

class fileHandling():

    def __init__(self,filePath):
        #  on class initialisation
        #  filepath holds name to the json file
        self.filePath = filePath
        
        #  file holds the json object/ json file content
        self.file = []
        
        #  opens the file on start
        self.openFile()

    def newID(self):
		'''
		I4
		ID will be automatically entered to avoid errors
		'''
		'''
		P2
		When adding anything to files it will be given a new ID if it doesn't have one already. This will involve adding one to the current maximum ID and then this being added to the JSON files.
		'''
        #  newID generates a new ID for a new field
        try:
            return len(self.readFile()['data'])
        except:
            return 0

    def openFile(self):
        #  openFile loads the file/ refreshes the file
        #  if the file doesn't exist then it's made
        #  module to open file as json
        #  loads json file
        try:
            with open(self.filePath) as jsonFile:
                self.file = json.load(jsonFile)
                
        except json.decoder.JSONDecodeError:
            with open(self.filePath, 'w') as jsonFile:
                data = {'data': []}
                json.dump(data, jsonFile, sort_keys=False, indent=4)

        self.file = json.load(open(self.filePath))
                
    def readFile(self):
        self.openFile()
        #  this is a good debug point
        #  print(self.file)

        return self.file

    def writeToFile(self, dictData):
		'''
		S2
		All customers details should be saved together (names, phone number, email address, DoB) Customer ID will be the key and then the details will be attached as subheadings in the file.
		'''
        #  writes a dictionary to the file by appending
        #  it to the current data
        data = self.readFile()
        data['data'].append(dictData)
        json.dump(data, open(self.filePath, 'w+'), sort_keys=False, indent=4)

    def editOneField(self, field, fieldID):
		'''
		S2
		All customers details should be saved together (names, phone number, email address, DoB) Customer ID will be the key and then the details will be attached as subheadings in the file.
		'''
        #  initialising variables
        self.openFile()
        tmplist = []
        data = {'data':[]}

        #  looping through the file till
        #  the desired ID
        for i in range(0, fieldID):
            tmplist.append(self.file['data'][i])

        #  appending the current data thats been edited
        tmplist.append(field)

        for i in range(fieldID + 1, len(self.file['data'])):
            tmplist.append(self.file['data'][i])

        data['data'] = tmplist
        json.dump(data, open(self.filePath, 'w+'), sort_keys=False, indent=4)
	
	'''
	S6
	Sorting and searching needs to be quick enough to not cause any loss to the company's efficiency, if the file is too large then use a quicksort.
	'''
	'''
	P10
	Searching a listview will use a linear/binary search.
	'''
    def quicksort(self, sortby):
        #  sortby is which dictionary key to sort the file by
        def partition(tmplist, first, last):
            pivot = tmplist[first]
            left = first + 1
            right = last

            finished = False

            while not finished:
                while left <= right and tmplist[left][str(list(tmplist[left].keys())[0])][sortby] <= (
                pivot[str(list(tmplist[first].keys())[0])][sortby]):
                    left += 1
                    
                while tmplist[right][str(list(tmplist[right].keys())[0])][sortby] >= (
                pivot[str(list(tmplist[first].keys())[0])][sortby]) and right >= left:
                    right -= 1

                if right < left:
                    finished = True

                else:
                    #  swapping the values
                    tmp = tmplist[left]
                    tmplist[left] = tmplist[right]
                    tmplist[right] = tmp

            #  swapping the values
            tmp = tmplist[first]
            tmplist[first] = tmplist[right]
            tmplist[right] = tmp

            return right
            
        def quickSorter(tmplist, first, last):
            if first < last:
                split = partition(tmplist, first, last)

                #  recursion
                quickSorter(tmplist, first, split - 1)
                quickSorter(tmplist, split + 1, last)

        self.openFile()
        tmplist = self.file['data']
        quickSorter(tmplist, 0, len(tmplist)-1)
        
        return tmplist

    def bubblesort(self, sortby):
        #  sortby is which dictionary key to sort the file by
        self.openFile()
        tmplist = self.file['data']
        
        for i in range(len(tmplist) - 1, 0, -1):        
            for j in range(i):
                lower = tmplist[j][str(list(tmplist[j].keys())[0])][sortby]
                upper = tmplist[j+1][str(list(tmplist[j+1].keys())[0])][sortby]

                if lower > upper:
                    #  swapping dictionaries
                    tmp = tmplist[j]
                    tmplist[j] = tmplist[j+1]
                    tmplist[j+1] = tmp
                    
        return tmplist
    
    def printFile(self):
        #  prints json file out using pretty print
        self.openFile()
        pprint(self.file)

    def binSearch(self, ary, elem, searchBy):
        #  recursive binary search
        def recurse(first, last):
            mid = int((first + last) / 2)
            lengthOfElem = len(elem)
            if first > last:
                return None
            elif (ary[mid][str(list(ary[mid].keys())[0])][searchBy])[0:lengthOfElem] < elem:
                return recurse(mid + 1, last)
            elif (ary[mid][str(list(ary[mid].keys())[0])][searchBy])[0:lengthOfElem] > elem:
                return recurse(first, mid - 1)
            else:
                return mid

        return recurse(0, len(ary) - 1)