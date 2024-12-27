from PIL import Image
import pytesseract
import argparse
import cv2
import os
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import csv
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from csv import writer

image=cv2.imread('jayesh3.jpg',0)
text=(pytesseract.image_to_string(image)).lower()
print(text)

file=['entertainment','investment','shopping','grocery','transport','home','others']
for category in file:
    with open(f'{category}.csv', 'a', newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['date', 'organisation', 'amount'])
    
match=re.findall(r'\d+[/.-]\d+[/.-]\d+', text)
st=''
st=st.join(match)
print(st)

nltk.download('punkt',quiet=True)
nltk.download('wordnet',quiet=True)

sent_tokens=nltk.sent_tokenize(text)
head = sent_tokens[0].splitlines()[0]

price=re.findall(r'[\$\£\€](\d+(?:\.\d{1,2})?)',text)
price = list(map(float,price)) 
print(max(price))
x=max(price) 

print(word_tokenize(text))

tokenizer = nltk.RegexpTokenizer(r"\w+")
new_words = tokenizer.tokenize(text)
print(new_words)

nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english')) 
filtered_list=[w for w in new_words if w not in stop_words ]
print(filtered_list)

entertainment = [] 
for syn in wordnet.synsets("entertainment"): 
    for l in syn.lemmas(): 
        entertainment.append(l.name()) 
        
l=['happy','restaurant','food','kitchen','hotel','room','park','movie','cinema','popcorn','combo meal']
entertainment=entertainment+l

home_utility=[] 
for syn in wordnet.synsets("home"): 
    for l in syn.lemmas(): 
         home_utility.append(l.name()) 
l2=['internet','telephone','elecricity','meter','wifi','broadband','consumer','reading','gas','water','postpaid','prepaid']
home_utility+=l2

grocery=[] 
for syn in wordnet.synsets("grocery"): 
    for l in syn.lemmas(): 
         grocery.append(l.name())
l3=['bigbasket','milk','atta','sugar','suflower','oil','bread','vegetabe','fruit','salt','paneer','coffee']
grocery+=l3

investment=[] 
for syn in wordnet.synsets("investment"): 
    for l in syn.lemmas(): 
         investment.append(l.name()) 
l1=['endowment','grant','loan','applicant','income','expenditure','profit','interest','expense','finance','property','money','fixed','deposit','kissan','vikas']
investment=investment+l1

transport=[]
for syn in wordnet.synsets("car"): 
    for l in syn.lemmas(): 
         transport.append(l.name()) 
l4=['cab','ola','uber','autorickshaw','railway','air','emirates','aerofloat','taxi','booking','road','highway']
transport+=l4

shopping=[]
for syn in wordnet.synsets("dress"): 
    for l in syn.lemmas(): 
         shopping.append(l.name()) 
l4=['iphone','laptop','saree','max','pantaloons','westside','vedic','makeup','lipstick','cosmetics','mac','facewash','heels','crocs','footwear','purse']
shopping+=l4

for word in filtered_list:
    if word in entertainment:
        e=True
        break
    elif word in investment:
        inv=True
        break
    elif word in grocery:
        g=True
        break
    elif word in shopping:
        s=True
        break
    elif word in transport:
        t=True
        break
    elif word in home_utility:
        h=True
        break

if(e):
    print("entertainment category")
    filename='{}.csv'.format('entertainment')
    #df=pd.read_csv('entertainment.csv')
elif(inv):
    print("investment category")
    filename='{}.csv'.format('investment')
    #df=pd.read_csv('investment.csv')
elif(s):
    print("shopping category")
    filename='{}.csv'.format('shopping')
    #df=pd.read_csv('shopping.csv')
elif(g):
    print("grocery category")
    filename='{}.csv'.format('grocery')
    #df=pd.read_csv('grocery.csv')
elif(t):
    print("transport category")
    filename='{}.csv'.format('transport')
    #df=pd.read_csv('transport.csv')
elif(h):
    print("home utility category")
    filename='{}.csv'.format('home')
    #df=pd.read_csv('home.csv')
else:
    print("others")
    filename='{}.csv'.format('others')
    #df=pd.read_csv('others.csv')

row_contents = [st, head, x]
def append_list_as_row(file, list_of_elem):
    with open (file, 'a+' , newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)
append_list_as_row(filename, row_contents)

def load_and_parse_csv(filename):
    try:
        df = pd.read_csv(filename)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%Y-%m-%d')
        else:
            print(f"Warning: 'date' column missing in {filename}")
            df['date'] = pd.NaT  # Add an empty date column
        return df
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return pd.DataFrame(columns=['date', 'organisation', 'amount'])  # Return empty DataFrame

entertainment = load_and_parse_csv('entertainment.csv')
investment = load_and_parse_csv('investment.csv')
shopping = load_and_parse_csv('shopping.csv')
grocery = load_and_parse_csv('grocery.csv')
transport = load_and_parse_csv('transport.csv')
other = load_and_parse_csv('others.csv')
home = load_and_parse_csv('home.csv')


# Convert the 'date' column to datetime, skipping errors caused by headers
entertainment['date'] = pd.to_datetime(entertainment['date'], errors='coerce')
investment['date'] = pd.to_datetime(investment['date'], errors='coerce')
shopping['date'] = pd.to_datetime(shopping['date'], errors='coerce')
grocery['date'] = pd.to_datetime(grocery['date'], errors='coerce')
transport['date'] = pd.to_datetime(transport['date'], errors='coerce')
other['date'] = pd.to_datetime(other['date'], errors='coerce')
home['date'] = pd.to_datetime(home['date'], errors='coerce')
