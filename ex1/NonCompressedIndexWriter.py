
import os
import re
import csv

def firstfile(input,dir):
    with open(input, 'r') as file:
        lines = file.readlines()
        pro = 0  # product id line in file
        help = 3  # helpfullness in file
        score = 4  # sore in file
        count = 0 #review id
        text = 7 #text of a given review
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
            procut=str(proline[1])

            temp = {'reviewID': count,
                    'productID': procut[1:10],
                    'helpfulness': helpline[1],
                    'score': scoreline[1],
                    'text': str(textline[2:]).lower(),
                    'length': len(length)-2}
            dict.append(temp)
            pro += 9
            help += 9
            score += 9
            text+=9
            count += 1
    except IndexError:
        field=['reviewID','productID','helpfulness','score','text','length']
        csv_file = dir + r'\revtopro.csv'
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field)
            writer.writeheader()
            for data in dict:
                writer.writerow(data)

       # df = pd.DataFrame(dict)
        #df.to_csv(dir + r'\revtopro.csv', index=False)




def secondfile(input,dir):
    with open(input, 'r') as file:
        lines = file.readlines()
        pro = 0  # product id line in file
        count = 0 #review id
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
        #df = pd.DataFrame(dict)
        #df.to_csv(dir + r'\proidtorevid.csv', index=False)

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

class NonCompressedIndexWriter:

    def __init__(self, inputFile, dir):
        # Load the Pandas libraries with alias 'pd'
        self.inputFile=inputFile
        self.dir = dir
        check_folder = os.path.isdir(self.dir)
        if not check_folder:
            os.makedirs(self.dir)
        else:
            removeDir(self.dir)
            os.makedirs(self.dir)
        firstfile(self.inputFile,self.dir)
        secondfile(self.inputFile,self.dir)



    def removeIndex(self, dir):
        removeDir(dir)

