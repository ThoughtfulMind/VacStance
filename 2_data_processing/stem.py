from nltk.stem import PorterStemmer

ps = PorterStemmer()

 

file1 = open('keywords.txt', 'rt')

Lines = file1.readlines()

for line in Lines:

    token=line.strip()

    print(token.lower()+"\t"+ps.stem(token))
