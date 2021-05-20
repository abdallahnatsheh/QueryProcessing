from IndexReader import IndexReader
import math
import re
import csv


def get_top_cosine_scores(query, dictionary, vector_squares_sum,dir):
    idxR = IndexReader(dir)
    scores = []  # final list contain rev-id,score
    N = vector_squares_sum  # number of the rev-ids
    big_list = []
    big_list2=[]
    vector_norm=0
    vector_norm_lnl=0
    #here is the LTC
    for elment in range(len(dictionary)):
        rev_list = []
        term_list = []
        tf_raw = []
        tf_wt = []
        df = []
        idf_wt = []
        tf_wt_idf_wt = []
        nlize = []
        tlist = []
        rev_list.append(dictionary[elment][0])
        tlist=dictionary[elment][4]
        tlist = re.sub("[^a-zA-z]+", " ", tlist).split(" ")
        tlist= list(set(tlist[2:]))
        tlist =sorted(tlist)
        tlist = tlist[1:]
        tquery = str(query).split(" ")
        for i in tquery:
            if i in tlist:
                continue
            tlist.append(i)
        tlist = sorted(tlist)

        for i in range(len(tlist)) :
            term_list.append(tlist[i])
            tf_raw.append(tquery.count(tlist[i]))
            if tf_raw[i] == 0:
                tf_wt.append(0)
            else:
                tf_wt.append(1 + math.log(float(tf_raw[i]), 10))
            df.append(idxR.getTokenFrequency(str(tlist[i])))
            if df[i] == 0 :
                idf_wt.append(0)
            else:
                idf_wt.append(math.log(N/df[i], 10))
            tf_wt_idf_wt.append(tf_wt[i]*idf_wt[i])
        counter = 0
        for num in tf_wt_idf_wt:
            counter = counter + pow(float(num),2)
        vector_norm = math.sqrt(counter)
        for word in range(len(tlist)):
            if vector_norm == 0:
                nlize.append(0)
            else:
                nlize.append(float(tf_wt_idf_wt[word])/float(vector_norm))
        rev_list.append(term_list)
        rev_list.append(tf_raw)
        rev_list.append(tf_wt)
        rev_list.append(df)
        rev_list.append(idf_wt)
        rev_list.append(tf_wt_idf_wt)
        rev_list.append(nlize)
        big_list.append(rev_list)
    scores.append(big_list)
    #the end of the LTC
    for elment in range(len(dictionary)):
        rev_list = []
        term_list = []
        tf_raw = []
        tf_wt = []
        df = []
        idf_wt = []
        tf_wt_idf_wt = []
        nlize = []
        tlist = []
        rev_list.append(dictionary[elment][0])
        tlist=dictionary[elment][4]
        tlist = re.sub("[^a-zA-z]+", " ", tlist).split(" ")
        tlist= list(set(tlist[2:]))
        tlist =sorted(tlist)
        tlist = tlist[1:]
        tquery = str(query).split(" ")
        for i in tquery:
            if i in tlist:
                continue
            tlist.append(i)
        tlist = sorted(tlist)

        for i in range(len(tlist)) :
            term_list.append(tlist[i])
            tf_raw.append(tlist.count(tlist[i]))
            if tf_raw[i] == 0:
                tf_wt.append(0)
            else:
                tf_wt.append(1 + math.log(float(tf_raw[i]), 10))
            idf_wt.append(1)
            tf_wt_idf_wt.append(tf_wt[i]*idf_wt[i])
        counter = 0
        for num in tf_wt_idf_wt:
            counter = counter + pow(float(num),2)
        vector_norm_lnl = math.sqrt(counter)
        for word in range(len(tlist)):
            if vector_norm_lnl == 0:
                nlize.append(0)
            else:
                nlize.append(float(tf_wt_idf_wt[word])/float(vector_norm_lnl))
        rev_list.append(term_list)
        rev_list.append(tf_raw)
        rev_list.append(tf_wt)
        rev_list.append(df)
        rev_list.append(idf_wt)
        rev_list.append(tf_wt_idf_wt)
        rev_list.append(nlize)
        big_list2.append(rev_list)
    scores.append(big_list2)
    return scores
class IndexSearcher:
    def __init__(self, reader):
        self.reader = reader

    def vectorSpaceSearch(self, query, k):
        lnl_ltc=[]
        dictionary = []
        with open(self.reader.dir + r'\revtopro.csv', 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                if len(row) != 0:
                    dictionary.append(row)
            del dictionary[0]
        vector_squares_sum = len(dictionary)

        lnl_ltc=get_top_cosine_scores(query, dictionary, vector_squares_sum,self.reader.dir)
        ltc_list=[]
        lnl_list=[]
        for i in range(int(vector_squares_sum)):
            temp1=[]
            temp1.append(lnl_ltc[0][i][0])
            temp1.append(lnl_ltc[0][i][7])
            ltc_list.append(temp1)
        for i in range(int(vector_squares_sum)):
            temp1=[]
            temp1.append(lnl_ltc[1][i][0])
            temp1.append(lnl_ltc[1][i][7])
            lnl_list.append(temp1)
        #now i have just to miltiply all the results and finish this shit
        big_boy=[] #the final

        for i in range(int(vector_squares_sum)):
            small_boy = []  # temp for the final

            temp=ltc_list[i][1]
            temp2=lnl_list[i][1]
            count=0
            for j in range(len(temp2)):
                count=count+temp[j]*temp2[j]
            small_boy.append(count)
            small_boy.append(ltc_list[i][0])
            big_boy.append(small_boy)

        big_boy=sorted(big_boy)
        print(big_boy)
        if k >= len(big_boy):
            listt=[]
            for i in range(len(big_boy)):
                listt.append(big_boy[i][1])
            listt = listt[::-1]
            listt=tuple(listt)
            #print(listt)
            return listt
        else:
            #if k < bigboy length
            listtt=[]
            final=[]
            listtt=big_boy[::-1]
            for gg in range(k):
                final.append(listtt[gg][1])
            final=tuple(final)
            return final

