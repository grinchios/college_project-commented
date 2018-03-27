import re

class validate():
    def valPassword(password, password2):
        #  password validation module

        #  double entry validation
        if password != password2:
            return 'Passwords need to match'
            
        #  length check
        if len(password) < 8:
            return 'Password needs to be longer than 8 characters'
            
        intAmount = 0
        symAmount = 0
        
        #  checking for two ints and one symbol
        for i in password:
            if i.isdigit():
                intAmount += 1
                
            if i in "[$&+,:;=?@#|'<>.-^*()%!]":
                symAmount += 1
                
        if intAmount < 2:
            return 'Password must contain at least 2 numbers'
            
        if symAmount == 0:
            return 'Password must contain at least 1 symbol'
            
        return True

    def usernameExists(username, fileContents):
        #  checks file for the password
        fileContent = fileContents['data']

        for i in range(len(fileContent)):            
            #  loops through the file for each ID
            if username == fileContent[i][str(list(fileContent[i].keys())[0])]['username']:
            
                #  triggers if a username matches
                return 'Username already exists'
                
        return True

    def isInt(strToCheck):
        try:
            int(strToCheck)
            return True
        except:
            return strToCheck + ' isn\'t an integer value please check and try again'

    def isFloat(strToCheck):
        try:
            float(strToCheck)
            return True
        except:
            return strToCheck + ' isn\'t a float value please check and try again'

    def isAlphaNumeric(strToCheck):
        intAmount, strAmount = 0, 0
        for i in range(len(strToCheck)):
            if strToCheck[i].isdigit():
                intAmount += 1
            if 97 <= ord(strToCheck[i]) <= 122:
                strAmount += 1

        if intAmount >= 1 and strAmount >= 1:
            return True

        elif intAmount == 0:
            return strToCheck + ' must contain a number'

        elif strAmount == 0:
            return strToCheck + ' must contain a letter'

    def isEmail(email):

        regexEmail = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        if regexEmail.match(email) is not None:
            return True
        else:
            return 'Email entered isn\'t valid'

    def checkLength(strToCheck, reqLen):
        if len(strToCheck) < reqLen:
            return True
        else:
            return strToCheck + ' is too long, must be {0} characters long'.format(str(reqLen-1))

    def checkPostcode(strToCheck):
        regexPostcode = re.compile(r'[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}')

        if regexPostcode.match(strToCheck):
            return True
        else:
            return strToCheck + ' is not a valid postcode'

    def checkRange(strToCheck, low, high):
        if low <= strToCheck <= high:
            return True
        else:
            return '{0} isn\'t between {1} and {2}'.format(strToCheck, low, high)

    def checkPresence(strToCheck, fieldName):
        if strToCheck != '':
            return True
        else:
            return '{0} must be filled'.format(fieldName)
