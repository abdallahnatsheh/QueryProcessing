
import re
import csv


class IndexReader:
    def __init__(self, dir):
        self.dir = dir

    def getProductId(self, reviewId):
        dic=[]
        with open(self.dir + r'\revtopro.csv','r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) !=0 :
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
                    helpo=dic[i][2]
                    helpo=helpo.split('/')
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

    def getProductReviews(self,productID):
        dic = []
        ids=[]
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
                if rev.lstrip() == str(productID+'\n'):
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
        size=0
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
                counter+=text.count(token)
        return counter

    def getReviewsWithToken(self, token):
        maxtup=[]
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
                idn =i
                frqn = text.count(token)
                maxtup.append("id-"+str(idn))
                maxtup.append("freq-"+str(frqn))

        maxtup = tuple(maxtup)
        return maxtup

