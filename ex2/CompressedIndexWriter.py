import os
import re
import csv
from CompressedIndexReader import CompressedIndexReader


def frontcodefile(block):
    word = ""
    temp = ""

    for item in block:

        temp = item
        if not word:
            word = word + item
        else:
            for i in range(len(word)):
                if item != "":
                    if str(word[i]) == str(item[i]):
                        temp = temp[1:]
                    else:
                        word = word + temp
                        temp = ""
                        break
                else:
                    word = word + temp
            word = word + temp

    return word


def createdict(dic):
    bigdoc = []
    mylist = dic[0]
    for items in dic:
        mylist = list(dict.fromkeys(items))
        mylist = [each_string.lower() for each_string in mylist]
        bigdoc.append(mylist)
    return bigdoc
    # block=mylist[:10]
    # frontcodefile(block)
    #


def prepairfrontcode(dictionary):
    tempdict = [] #temp list for the text words
    templist = [] #templist for 9 in 10 front coding
    tempword = "" # the result from frontcoding
    blocklen=0 #length of the text after front coding.
    for item in dictionary:
        for word in item:
            tempdict.append(word)
    tempdict = sorted(tempdict)
    for i in range(int(len(tempdict) / 10)):
        templist = tempdict[:10]
        tempword += frontcodefile(templist)
        del tempdict[:10]
    tempword= tempword.replace(tempword[:25], '')
    tempword = re.sub("[^a-zA-Z]+", "", tempword)


    return tempword

def  createblocks(dictionary,frontcodeword):
    blocklist=[]
    tempdict = []  # temp list for the text words
    for item in dictionary:
        for word in item:
            tempdict.append(word)
    print(tempdict)

def thirdfile(input, dir):
    with open(input, 'r') as file:
        lines = file.readlines()
        text = 7  # text of a given review
        dict = []
    try:
        for i in lines:
            textline = re.sub("[^a-zA-z]+", " ", lines[text])
            textline = textline.split()
            textline[:] = (elem[:10] for elem in textline)
            textline = textline[2:]
            dict.append(textline)
            text += 9

    except IndexError:
        tempdict = []
        dictionary = createdict(dict)
        frontcodeword=""

       #its used for the posting list shit!
        idxR = CompressedIndexReader(dir)
        for item in dictionary:
           for word in item:
               temp = {'word': word,
                      'postinglist': idxR.getReviewsWithToken(word)}
               tempdict.append(temp)
        field = ['word', 'postinglist']
        csv_file = dir + r'\tempdict.csv'
        with open(csv_file, 'w') as csvfile:
           writer = csv.DictWriter(csvfile, fieldnames=field)
           writer.writeheader()
           for data in tempdict:
               writer.writerow(data)

    # wordlen|frontcodeword|block10|block9---0|
    frontcodeword = prepairfrontcode(dictionary)
    createblocks(dictionary,frontcodeword)



def firstfile(input, dir):
    with open(input, 'r') as file:
        lines = file.readlines()
        pro = 0  # product id line in file
        help = 3  # helpfullness in file
        score = 4  # sore in file
        count = 0  # review id
        text = 7  # text of a given review
        dict = []
    try:
        for i in lines:
            proline = lines[pro].split(':')
            helpline = lines[help].split(':')
            scoreline = lines[score].split(':')
            textline = re.sub("[^a-zA-z]+", " ", lines[text])
            textline = textline.split()
            textline[:] = (elem[:10] for elem in textline)
            length = re.sub("[^a-zA-z]+", " ", lines[text])
            length = length.split()
            procut = str(proline[1])

            temp = {'reviewID': count,
                    'productID': procut[1:10],
                    'helpfulness': helpline[1],
                    'score': scoreline[1],
                    'text': str(textline[2:]).lower(),
                    'length': len(length) - 2}
            dict.append(temp)
            pro += 9
            help += 9
            score += 9
            text += 9
            count += 1
    except IndexError:
        field = ['reviewID', 'productID', 'helpfulness', 'score', 'text', 'length']
        csv_file = dir + r'\revtopro.csv'
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field)
            writer.writeheader()
            for data in dict:
                writer.writerow(data)

    # df = pd.DataFrame(dict)
    # df.to_csv(dir + r'\revtopro.csv', index=False)


def secondfile(input, dir):
    with open(input, 'r') as file:
        lines = file.readlines()
        pro = 0  # product id line in file
        count = 0  # review id
        dict = []
    try:
        for i in lines:
            proline = lines[pro].split(':')
            temp = {
                'productID': str(proline[1]),
                'reviewID': count
            }
            dict.append(temp)
            pro += 9
            count += 1
    except IndexError:
        field = ['productID', 'reviewID']
        csv_file = dir + r'\proidtorevid.csv'
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field)
            writer.writeheader()
            for data in dict:
                writer.writerow(data)


def removeDir(dirName):
    # Remove any read-only permissions on file.
    removePermissions(dirName)
    for name in os.listdir(dirName):
        file = os.path.join(dirName, name)
        if not os.path.islink(file) and os.path.isdir(file):
            removeDir(file)
        else:
            removePermissions(file)
            os.remove(file)
    os.rmdir(dirName)
    return


def removePermissions(filePath):
    # if (os.access(filePath, os.F_OK)) : #If path exists
    if (not os.access(filePath, os.W_OK)):
        os.chmod(filePath, 0o666)
    return


class CompressedIndexWriter:
    def __init__(self, inputFile, dir):
        # Load the Pandas libraries with alias 'pd'
        self.inputFile = inputFile
        self.dir = dir
        check_folder = os.path.isdir(self.dir)
        if not check_folder:
            os.makedirs(self.dir)
        else:
            removeDir(self.dir)
            os.makedirs(self.dir)
        firstfile(self.inputFile, self.dir)
        secondfile(self.inputFile, self.dir)
        thirdfile(self.inputFile, self.dir)
