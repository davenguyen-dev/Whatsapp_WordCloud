import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  
from os import path 
from nltk.corpus import stopwords
from wordcloud import WordCloud, ImageColorGenerator  

data = open(  , 'r') #insert file path in first argument

# Turn all letters into lower case
text = data.read().lower()
type(text) #it's a string

#find all words between 3 and 15 characters long
match_pattern = re.findall(r'\b[a-z]{3,15}\b', text)
type(match_pattern) #it's a list
y1 = len(match_pattern)

# Remove stopwords using nltk library
match_pattern = [word for word in match_pattern if word not in stopwords.words('english')] #list comprehension
y2 = len(match_pattern)

# Further remove custom words
wordsForRemoval = ["word1", "word2", "word3"] #replace words you want to be removed 
for i in list(match_pattern): #iterating on a copy to prevent errors
    if i in wordsForRemoval:
        match_pattern.remove(i) 
y3 = len(match_pattern)

#Plotting wordlist refining process above
def whatsapp_word_refining_plot():
    x = ["RegEx \n3-15 leters only", "NLTK Stopwords \nRemoved", "Custom Words \nRemoved"]
    y = [y1, y2, y3]
    plt.plot(x, y)
    plt.xlabel('REMOVAL PROCESS OVER TIME')
    plt.ylabel('NUMBER OF WORDS IN LIST')
    plt.title('REFINING THE WHATSAPP WORDCLOUD WORDLIST \nUSING MULTI-STAGE METHODS')
    plt.show()
whatsapp_word_refining_plot()

# Obtaining frequency of each word in list
frequency = { }
for word in match_pattern:
    count = frequency.get(word,0)
    frequency[word] = count + 1
type(frequency) #it's now a dictionary

frequency_list = frequency.keys() #not necessary to do this

# Convert dictionary to dataframe
df = pd.DataFrame(list(frequency.items()),columns = ['word','frequency']) 

# Sort values in dataframe by descending frequency of word
df.sort_values(["frequency"], inplace=True, ascending=False)

# To make sure WordCloud().generate can function (needs words to be in string format) 
whatsapp_wordcloud_data_string = str(df['word'])

# To make easier to graph, we replace first column with words
#df.set_index(['word'], inplace=True)

# To show all of dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# If we want to show the first 100 words and their frequencies
#print(df.head(100))

# Plot line (not very good because of limited x-axis space)
#df.head(10).plot()
#plt.show()

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(whatsapp_wordcloud_data_string)

# Refining the generated image:
# lower max_font_size, change the maximum number of word and lighten the background:
wordcloud = WordCloud(width=800, height=400, max_font_size=100, max_words=100, background_color="black").generate(whatsapp_wordcloud_data_string)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# Save the image in the img folder:
wordcloud.to_file("wordcloud.png")

