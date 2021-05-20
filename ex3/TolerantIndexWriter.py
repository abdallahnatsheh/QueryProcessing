import os
import re
import csv
from TolerantIndexReader import TolerantIndexReader
from collections import Counter


def biagram(word):
    word = ''.join(('$', word, '$'))
    res = Counter(word[idx: idx + 2] for idx in range(len(word) - 1))
    return res


def createdict(dic):
    bigdoc = []
    mylist = dic[0]
    for items in dic:
        mylist = list(dict.fromkeys(items))
        mylist = [each_string.lower() for each_string in mylist]
        bigdoc.append(mylist)
    return bigdoc


def fourfile(dir):
    dic = []
    with open(dir + r'\posting.csv', 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read())
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        for row in reader:
            if len(row) != 0:
                dic.append(row)
        del dic[0]
        tempdict = []  # its used to create the last csv
        templist = []  # its used to add the bigram to sort them
        templist1 = []  # its used to put all the word of bigram exisiting
        idxR = TolerantIndexReader(dir)
        for item in dic:
            word = biagram(item[1])
            for alpha in word:
                templist.append(alpha)
                # templist1.append(idxR.getReviewsWithTokenBigram(alpha))

        templist = sorted(templist)

        sorted_templist = []  # this is the final list of the bigram to add to csv
        for i in templist:
            if i not in sorted_templist:
                sorted_templist.append(i)
                templist1.append(idxR.getReviewsWithTokenBigram(i))
    for i in range(len(sorted_templist)):
        temp = {'word': sorted_templist[i],
                'postinglist': templist1[i]}
        tempdict.append(temp)
    field = ['word', 'postinglist']
    csv_file = dir + r'\bigramlist.csv'
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field)
        writer.writeheader()
        for data in tempdict:
            writer.writerow(data)


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


def prepairfrontcode(dictionary):
    tempdict = []  # temp list for the text words
    for item in dictionary:
        for word in item:
            if word in tempdict:
                continue
            else:
                tempdict.append(word)
    tempdict = sorted(tempdict)
    return tempdict


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
        termnum = 0
        dictionary = createdict(dict)
        mainlist = prepairfrontcode(dictionary)
        # its used for the posting list shit!
        idxR = TolerantIndexReader(dir)
        for item in mainlist:
            temp = {'termnumber': termnum,
                    'word': item}
            tempdict.append(temp)
            termnum = termnum + 1
        field = ['termnumber', 'word']
        csv_file = dir + r'\posting.csv'
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field)
            writer.writeheader()
            for data in tempdict:
                writer.writerow(data)


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
        # df = pd.DataFrame(dict)
        # df.to_csv(dir + r'\proidtorevid.csv', index=False)


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
    if not os.access(filePath, os.W_OK):
        os.chmod(filePath, 0o666)
    return


class TolerantIndexWriter:

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
        fourfile(self.dir)

    def removeIndex(self, dir):
        removeDir(dir)
