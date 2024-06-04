import string
import re 
import os 
import pandas as pd
from nltk.tokenize import RegexpTokenizer , sent_tokenize
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import nltk
nltk.download('punkt')
nltk.download('stopwords')

input = pd.read_excel("Input.xlsx")
input
for index, row in input.iterrows():
  url = row['URL']
  url_id = row['URL_ID']#
 #url = 'https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the-economy-environment-infrastructure-and-city-life-by-the-year-2040-2/'
  page=requests.get(url )  
  soup = BeautifulSoup(page.text , 'html.parser')
  #find title
  try:
     title = soup.find('h1').get_text()
  except:
    print("can't get title of {}".format(url))
  #find text
  content = ""
  try:
    # Select all <p> elements except the first 16 and last 3
    for p in soup.find_all('p')[16:-3]:
        content += p.get_text()
  except:
    print("Can't get text of {}".format(url))
  lines = (line.strip() for line in content.splitlines())
  chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
  text = '\n'.join(chunk for chunk in chunks if chunk)
  #print(title)
  #print(text)
  #print('--'*50)
  
  ###write title and text to the file
  #folder_name = "ExtractedTitleText"
  #if not os.path.exists(folder_name):
   # os.makedirs(folder_name)

  #file_name = os.path.join(folder_name, 'TitleText' + str(url_id) + '.txt')
  #with open(file_name, 'w', encoding='utf-8') as file:
    #file.write(title + '\n' + content)


text_dir = r"C:\Users\Dell\Desktop\BlackCoffer\ExtractedTitleText"
stopwords_dir = r"C:\Users\Dell\Desktop\BlackCoffer\StopWords"
sentiment_dir = r"C:\Users\Dell\Desktop\BlackCoffer\MasterDictionary"

# Initialize an empty set to store stopwords
stopwords = set()

# Loop through all text files in the stopwords directory
for filename in os.listdir(stopwords_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(stopwords_dir, filename)
        # Open the file and read each line
        with open(filepath, "r", encoding="ISO-8859-1") as file:
            # Read each line and split it into words
            for line in file:
                words = line.split()
                # Add each word to the stopwords set
                stopwords.update(words)

# Now, stopwords variable contains all the words from the text files
#print(stopwords)



docs = []
for text_file in os.listdir(text_dir):
  with open(os.path.join(text_dir,text_file),'r',encoding='utf-8') as f:
    text = f.read()
#tokenize the given text file
    words = word_tokenize(text)
# Define a translation table to remove all punctuation marks
    translation_table = str.maketrans( '','', string.punctuation)
# remove the stop words from the tokens
    filtered_text = [word.translate(translation_table) for word in words if word.translate(translation_table).lower() not in stopwords]
# add each filtered tokens of each file into a list
    docs.append(filtered_text)

# store positive, Negative words from the directory
positive=set()
negative=set()

for files in os.listdir(sentiment_dir):
  if files =='negative-words.txt':
    with open(os.path.join(sentiment_dir,files),'r',encoding='ISO-8859-1') as f:
      negative.update(f.read().splitlines())
  else:
    with open(os.path.join(sentiment_dir,files),'r',encoding='ISO-8859-1') as f:
      positive.update(f.read().splitlines())

positive_words = []
positive_score =[]
for i in range(len(docs)):
    positive_words.append([word for word in docs[i] if word.lower() in positive])
    positive_score.append(len(positive_words[i]))

negative_words = []
negative_score =[]
for i in range(len(docs)):
    negative_words.append([word for word in docs[i] if word.lower() in negative])
    negative_score.append(len(negative_words[i]))

polarity_score =[]
for i in range(len(docs)):
    polarity_score.append((positive_score[i] - negative_score[i]) / ((positive_score[i] + negative_score[i]) + 0.000001))


subjectivity_score = []
for i in range (len(docs)):
    subjectivity_score.append((positive_score[i] + negative_score[i]) / ((len(docs[i])) + 0.000001))



avg_sentence_length = []
Percentage_of_Complex_words  =  []
Fog_Index = []
complex_word_count =  []
avg_syllable_word_count =[]


stopwords = set()
def calculations(file):
  with open(os.path.join(text_dir, file),'r', encoding='utf-8') as f:
    text = f.read()
# remove punctuations 
    text = re.sub(r'[^\w\s.]','',text)
# split the given text file into sentences
    sentences = text.split('.')
# total number of sentences in a file
    num_sentences = len(sentences)
# total words in the file
    words = [word  for word in text.split() if word.lower() not in stopwords ]
    num_words = len(words)

    complex_words = []
    for word in words:
       vowels = 'aeiou'
       syllable_count_word = sum( 1 for letter in word if letter.lower() in vowels)
       if syllable_count_word > 2:
         complex_words.append(word)


    syllable_count = 0
    syllable_words =[]
    for word in words:
        if word.endswith('es'):
           word = word[:-2]
        elif word.endswith('ed'):
           word = word[:-2]
        vowels = 'aeiou'
        syllable_count_word = sum( 1 for letter in word if letter.lower() in vowels)
        if syllable_count_word >= 1:
           syllable_words.append(word)
           syllable_count += syllable_count_word


    avg_sentence_len = num_words / num_sentences
    avg_syllable_word_count = syllable_count / len(syllable_words)
    Percent_Complex_words  =  len(complex_words) / num_words
    Fog_Index = 0.4 * (avg_sentence_len + Percent_Complex_words)

    return avg_sentence_len, Percent_Complex_words, Fog_Index, len(complex_words),avg_syllable_word_count
  


# iterate through each file or doc
for file in os.listdir(text_dir):
  x,y,z,a,b = calculations(file)
  avg_sentence_length.append(x)
  Percentage_of_Complex_words.append(y)
  Fog_Index.append(z)
  complex_word_count.append(a)
  avg_syllable_word_count.append(b)



# Word Count and Average Word Length Sum of the total number of characters in each word/Total number of words
# We count the total cleaned words present in the text by 
# removing the stop words (using stopwords class of nltk package).
# removing any punctuations like ? ! , . from the word before counting.

def cleaned_words(file):
  with open(os.path.join(text_dir,file), 'r',encoding='utf-8') as f:
    text = f.read()
    text = re.sub(r'[^\w\s]', '' , text)
    words = [word  for word in text.split() if word.lower() not in stopwords]
    length = sum(len(word) for word in words)
    average_word_length = length / len(words)
  return len(words),average_word_length

word_count = []
average_word_length = []
for file in os.listdir(text_dir):
  x, y = cleaned_words(file)
  word_count.append(x)
  average_word_length.append(y)


# To calculate Personal Pronouns mentioned in the text, we use regex to find 
# the counts of the words - “I,” “we,” “my,” “ours,” and “us”. Special care is taken
#  so that the country name US is not included in the list.
def count_personal_pronouns(file):
  with open(os.path.join(text_dir,file), 'r',encoding='utf-8') as f:
    text = f.read()
    personal_pronouns = ["I", "we", "my", "ours", "us"]
    count = 0
    for pronoun in personal_pronouns:
      count += len(re.findall(r"\b" + pronoun + r"\b", text)) # \b is used to match word boundaries
  return count

personalpro_count = []
for file in os.listdir(text_dir):
  x = count_personal_pronouns(file)
  personalpro_count.append(x)