import csv
import re
from collections import Counter
from itertools import chain


def findtoken(dic,token):

    for i in range(len(dic)):
        if token == dic[i][1]:
            return True
    return False
def biagram(word):
    cc = Counter()
    #word = ''.join(('$', word, '$'))
    res = Counter(word[idx: idx + 2] for idx in range(len(word) - 1))
    if res == cc:
        return word
    return res

def wildagram(word):
    res = []
    dic = []

    word = ''.join(('$', word, '$'))
    word = word.split('*')
    for i in range(len(word)):
        res=biagram(word[i])
        for alpha in res:
            dic.append(alpha)
    return dic

def checkbigram(self,tempdic):
    dic = [] #to load the csv in list
    temp = [] # to check every column
    listo=[] #make a list of the bigram numbers
    templist = [] #put all the bigram numbers in list
    toto = ""
    dummy=0
    with open(self.dir + r'\bigramlist.csv', 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read())
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        for row in reader:
            if len(row) != 0:
                dic.append(row)
        del dic[0]
        # i need this operation into every part of dic to make a list of all the words in the bigram tempdic

    for elemnt in range(len(tempdic)):
        for alpha in range(len(dic)-1):
            if tempdic[elemnt] in dic[alpha][0]:
                listo=[]
                toto = ""
                dummy = ""
                temp = dic[alpha][1]
                invalid = re.compile('[^0-9]')
                temp = [i for i in temp if not invalid.search(i)]
                for i in range(len(temp)):
                    toto = toto + temp[i]
                temp = toto
                listo .append(temp)
                temp = dic[alpha][2:]
                if temp:
                    dummy= temp[len(temp)-1][0:]
                    dummy = dummy.split(']')
                    invalid = re.compile('[^0-9]')
                    temp = [i for i in temp if not invalid.search(i)]
                    dummy = [i for i in dummy if not invalid.search(i)]
                    listo = listo +temp
                    listo = listo + dummy
                templist.append(listo)
    #list_2 = [num for num in temp if isinstance(num, (int, float))]
    return templist
def getthesewords(self,max):
    dic = []
    listofwords = [] # put all words on it to return
    with open(self.dir + r'\posting.csv', 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read())
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        for row in reader:
            if len(row) != 0:
                dic.append(row)
        del dic[0]

    max = [str(x) for x in max]
    for num in range(len(max)):
        for elemnt in range(len(dic)-1):
            if max[num] == dic[elemnt][0]:
                listofwords.append(dic[elemnt][1])
    return  listofwords

def checkjaccard(basegram,tempforcorr):
    bigramlist = [] #list of all the bigrams
    listjaccard = []
    for i in range(len(tempforcorr)):
        bigramlist.append(wildagram(tempforcorr[i]))
    for i in range(len(bigramlist)):
        mona =len(sorted(set(basegram)&set(bigramlist[i]), key = lambda k : basegram.index(k)))
        mekhane = len(list((Counter(basegram) - Counter(bigramlist[i])).elements())+list((Counter(bigramlist[i]) - Counter(basegram)).elements()))
        listjaccard.append(float(float(mona)/float(mekhane)))
    maxindex = max((v,i) for i,v in enumerate(listjaccard))
    return tempforcorr[maxindex[1]]



class IndexReader:
    def __init__(self, dir):
        self.dir = dir

    def getProductId(self, reviewId):
        dic = []
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
            for i in range(len(dic)):
                rev = int(dic[i][0])
                if rev == reviewId:
                    return str(dic[i][1])

    def getReviewScore(self, reviewId):
        dic = []
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
            for i in range(len(dic)):
                rev = int(dic[i][0])
                if rev == reviewId:
                    return int(float(dic[i][3].strip()))

    def getReviewHelpfulnessNumerator(self, reviewId):
        dic = []
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
            for i in range(len(dic)):
                rev = int(dic[i][0])
                if rev == reviewId:
                    helpo = dic[i][2]
                    helpo = helpo.split('/')
                    return int(float(helpo[0]))

    def getReviewHelpfulnessDenominator(self, reviewId):
        dic = []
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
            for i in range(len(dic)):
                rev = int(dic[i][0])
                if rev == reviewId:
                    helpo = dic[i][2]
                    helpo = helpo.split('/')
                    return int(float(helpo[1]))

    def getReviewLength(self, reviewId):
        dic = []
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
            for i in range(len(dic)):
                rev = int(dic[i][0])
                if rev == reviewId:
                    leng = dic[i][5]
                    return int(float(leng))

    def getProductReviews(self, productID):
        dic = []
        ids = []
        with open(self.dir + r'\proidtorevid.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
            for i in range(len(dic)):
                rev = str(dic[i][0])
                if rev.lstrip() == str(productID + '\n'):
                    ids.append(i)
            ids = tuple(ids)
            return ids

    def getNumberOfReviews(self):
        dic = []
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
            return len(dic)

    def getTokenSizeOfReviews(self):
        dic = []
        size = 0
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
            for i in range(len(dic)):
                leng = int(dic[i][5])
                size += leng
        return size

    def getTokenFrequency(self, token):

        token = token.lower()
        dic = []
        counter = 0
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
        size = self.getNumberOfReviews()
        for i in range(size):
            text = dic[i][4]
            text = re.sub("[^a-z]+", " ", text)
            text = text.split()
            if token in text:
                counter += 1
        return counter

    def getTokenCollectionFrequency(self, token):
        token = token.lower()
        dic = []
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
        size = self.getNumberOfReviews()
        counter = 0
        for i in range(size):
            text = dic[i][4]
            text = re.sub("[^a-z]+", " ", text)
            text = text.split()
            if token in text:
                counter += text.count(token)
        return counter

    def getReviewsWithTokenBigram(self, token):
        maxtup = []

        dic = []
        with open(self.dir + r'\posting.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
        if token[0] == '$':
            token = token[1:]
            for item in dic:
                if token in item[1][0]:
                    maxtup.append(item[0])
            return maxtup
        elif token[len(token) - 1] == '$':
            token = token[:-1]
            for item in dic:
                if token in item[1][-1]:
                    maxtup.append(item[0])
            return maxtup
        else:
            for item in dic:
                if token in item[1]:
                    maxtup.append(item[0])
            return maxtup

    def getReviewsWithTokenPosting(self, token):
        maxtup = []
        token = token.lower()
        dic = []
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
        size = self.getNumberOfReviews()
        for i in range(size):
            text = dic[i][4]
            text = re.sub("[^a-z]+", " ", text)
            text = text.split()
            if token in text:
                idn = i
                maxtup.append(str(idn))

        maxtup = tuple(maxtup)
        return maxtup

    def getReviewsWithToken(self, token):
        maxtup = []
        token = token.lower()
        dic = []
        with open(self.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]
        size = self.getNumberOfReviews()
        for i in range(size):
            text = dic[i][4]
            text = re.sub("[^a-z]+", " ", text)
            text = text.split()
            if token in text:
                idn = i
                frqn = text.count(token)
                maxtup.append("id-" + str(idn))
                maxtup.append("freq-" + str(frqn))

        maxtup = tuple(maxtup)
        return maxtup


    def getTokenCorrections(self, token, lambd, d):
        dic = []
        tmepdic = []
        tempnumlist = []
        temptoken= str(token)
        bfinalresult = []
        thefinal = []
        with open(self.dir + r'\posting.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dic.append(row)
            del dic[0]


        if '*' in token:

            tempdic=wildagram(token)

            tempnumlist = checkbigram(self,tempdic)
            tempnumlist = [ list(map(int,x)) for x in tempnumlist]
            #test = [[3,4,5,6,7],[1,3,4,5,6,7,8],[3,4,5,6,7,8],[1,2,3,4,5,6,7]]
            counter_obj = Counter(chain.from_iterable(tempnumlist))
            t = counter_obj.most_common()
            max = []
            m = t[0][1]
            for i in range(len(t)-1):
                if t[i][1] == m:
                    max.append(t[i][0])

            bfinalresult = getthesewords(self,max)
            temptoken = temptoken.replace('*','.+')
            for word in bfinalresult:
                # The .+ symbol is used in place of * symbol
                if re.search(temptoken, word):
                    thefinal.append(word)
            return  thefinal

        else:
            if findtoken(dic,token):
                return token
            else:
                tempforcorr = []
                tempdic = wildagram(token)

                tempnumlist = checkbigram(self, tempdic)
                tempnumlist = [list(map(int, x)) for x in tempnumlist]
                # test = [[3,4,5,6,7],[1,3,4,5,6,7,8],[3,4,5,6,7,8],[1,2,3,4,5,6,7]]
                counter_obj = Counter(chain.from_iterable(tempnumlist))
                t = counter_obj.most_common()
                max = []
                m = t[0][1]
                for i in range(len(t) - 1):
                    if t[i][1] == m:
                        max.append(t[i][0])

                tempforcorr = getthesewords(self, max)
                basegram = tempdic #save the bigram of the token
                finalword = checkjaccard(basegram,tempforcorr)
                return finalword


