#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset (Analysis of TMDb 10,000 movies dataset)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# I choose the TMDb movie data set for data analysis. This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including :
#     user ratings ,The budjet and revenue of The Movies, release year,production companies ,The movies names, directors and Cast
#     I would like to find other intresting patterns in this dataset
#     using paython packges pandas , numpy , seaborn , matplotlib in this analysis
#     
#   > # Questions research
# 
# <li> Which Top 20 movies earn highest profit </li>
# <li> Which movie Has Highest /  Lowest Profit </li>
# <li> Which movie get the highest or lowest votes (Ratings) </li>
# <li> what are most profitable years </li>
# <li> what are most made geners </li>
#     

# In[30]:


# First import the packages 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# >  After Observing the dataset , we will
#     clean data by Remove unnecessry columns , drop dublicted rows, change the data type for some columns 
#      and spilt the rows that containes more than values ( in this dataset seprating by pipe (|) like genres , cast ,production_companies
# 
# ### General Properties

# In[31]:


# read the data from CSV file to dataframe and print out a few lines. 
df_M = pd.read_csv('https://d17h27t6h515a5.cloudfront.net/topher/2017/October/59dd1c4c_tmdb-movies/tmdb-movies.csv')
df_M.head(2)


#  in this section I will find information about the data set like columns names , data tpe , number of rows and columns and numper of non null values

# In[3]:


# using info() function
df_M.info()


# In[126]:


# hear the dimensions of the dataframe , numbers of columns and rows
df_M.shape


#  <li> Observation From The Dataset
# <li> Number of rows are 10866
# <li> Number of columns are 21
# <li> The data type of each column 
# <li> data type of the column 'imdb_id' is object should be int 
# <li> the data type of the column 'release_date' is object should be date
# <li> Remove the unused colums homepage,tagline, budget_adj and revenue_adj
# <li> genres , cast and production_companies columns have multi values should  be spearate
# 
#  
# 
# 

# 
# ### Data Cleaning (Information That We Need To Delete Or Modify)
# 
# 
# 

# 1. remove duplicated rows

# In[32]:


# sum of duplicated rows
df_M.duplicated().sum()


# In[128]:


# drop duplicated using 
df_M.drop_duplicates(inplace = True)
df_M.duplicated().sum()


# 2- Remove the unused colums that are not needes in the analysis process
#  homepage,tagline, budget_adj and revenue_adj 

# In[33]:


# use drop() to delete columns
df_M.drop(['budget_adj','revenue_adj','homepage','tagline'],axis =1,inplace = True)


# In[34]:


print ("the number of columns aftr drop unused colums is 17 :" )
df_M.shape 


# Summary statistics of the runtime for the movies 

# In[63]:


# using describe()
df_M['runtime'].describe()


# 3- Changing Format Of Release Date Into Datetime Format

# In[35]:


# the data type of the column 'release_date' is object should be date
df_M['release_date'] = pd.to_datetime(df_M['release_date'])


# In[37]:


df_M.release_date.dtypes


# 4- I obserive the data type of column 'imdb_id' is object and should modify to int but first I will spilet the litters from the numbers
# 

# In[38]:


# 1. Separate letters (tt) in the column 'imdb_id ' from numbers and show the result
df_M['imdb_id'] = df_M['imdb_id'].str.replace('tt','')


# In[39]:


# 2. data type of imdb_id is object
df_M.imdb_id.dtypes


# In[40]:


df_M.imdb_id = pd.factorize(df_M.imdb_id)[0]


# In[41]:


# 4. Now the data type of imdb_id has been fixed
df_M.imdb_id.dtypes


# 5- Separate rows that have more than one value which is separated by pipe (|)
# <li> The columns contain pipes Th genres , production_companies , cast

# In[42]:


# The colmn genres split by "|" I but in data frame
hb_M = df_M[df_M['genres'].str.contains('|') == True]
hb_M.head(2)


# In[43]:


# create two copies of the hb_M dataframe
df_1 = hb_M.copy()  
df_2 = hb_M.copy()  

# Each one should look like this
df_1.head(2)


# In[44]:


df_2.head(1)


# In[45]:


split_columns = ['genres','production_companies','cast']

for c in split_columns:
  df_1[c] = df_1[c].astype(str).str.split("|").str[0]
  df_2[c] = df_2[c].astype(str).str.split("|").str[1]


# In[17]:


# combine dataframes to add to the original dataframe
new_rows = df_1.append(df_2)

# now we have separateit to new rows 
new_rows


# In[46]:


# drop the original hybrid rows
df_M.drop(hb_M.index, inplace=True)

# add in our newly separated rows
df_M = df_M.append(new_rows, ignore_index=True)


# In[47]:


df_M.head(2)


# After separating drop the null values 
# 1. Remove null values

# In[48]:


df_M.isnull().sum()


# In[49]:


df_M.dropna(inplace=True)
df_M.isnull().sum()


# In[50]:


df_M.head(2)


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# >  After trimmed and cleaned The data, Now move on to exploration. Compute statistics and create visualizations to find Patterns between the data , find answers of My research questions . 
# ### Research Question 1 (Top 20 movies based on its Profit)

# In[51]:


info = pd.DataFrame(df_M['revenue'].sort_values(ascending = False))
info['original_title'] = df_M['original_title']
data = list(map(str,(info['original_title'])))
x = list(data[:20])
y = list(info['revenue'][:20])
ax = sns.pointplot(x=y , y=x) 
sns.set(rc={'figure.figsize':(10,10)})
ax.set_title("Top 20 Movies has high Profit" , fontsize = 15)
ax.set_xlabel("revenue" , fontsize = 15)
sns.set_style("darkgrid")


# The Avatar Movie has the highst provit in the dataset

# ### Research Question 2 (Which movie Has Highest /  Lowest Profit and budget)

# In[52]:


#calculate Profit for each of the movie
#add a new column Profit for each of the movie
df_M['Profit'] = df_M['revenue'] - df_M['budget']


# In[53]:


# create function to find min and max 
#use the function 'idmin' to find the index of lowest profit movie.
#use the function 'idmax' to find the index of Highest profit movie.
def find_minmax(x):
    min_M = df_M[x].idxmin()
    max_M = df_M[x].idxmax()
    high = pd.DataFrame(df_M.loc[max_M,:])
    low = pd.DataFrame(df_M.loc[min_M,:])
    
    #print the movie with high and low profit
    print("Movie Which Has Highest "+ x + " : ",df_M['original_title'][max_M])
    print("Movie Which Has Lowest "+ x + "  : ",df_M['original_title'][min_M])
    return pd.concat([high,low],axis = 1)

#call the find_minmax function.
find_minmax('Profit')


# In[54]:


# use find_minmax to find Movie Which Has Highest ,Lowest budget
find_minmax('budget')


# ### Research Question 3  ( Movie with Highest And Lowest Votes?)

# In[55]:


#find_minmax to find Movie Which Has rating
find_minmax('vote_average')


# In[56]:


#find the max and min vote averag
df_M.vote_average.max() 


# In[57]:


df_M.vote_average.min()


# In[59]:


#top 10 highets rated movies.
#sort the 'vote_average' column in decending order and store it in the new dataframe.
info = pd.DataFrame(df_M['vote_average'].sort_values(ascending = False))
info['original_title'] = df_M['original_title']
data = list(map(str,(info['original_title'])))

##extract the top 10 highly rated movies data from the list and dataframe.
x = list(data[:10])
y = list(info['vote_average'][:10])

#make the point plot and setup the title and labels.
ax = sns.pointplot(x=y,y=x)
sns.set(rc={'figure.figsize':(10,5)})
ax.set_title("Top 10 Highest Rated Movies",fontsize = 15)
ax.set_xlabel("Vote Average",fontsize = 13)
#setup the stylesheet
sns.set_style("darkgrid")


# The chart shows the Story of Film: An Odyssey Movie has Highest votes

# ### Research Question 3 : what are most profitable years 

# In[60]:


#do year-wise analysis of profit earn by movies in each earn.
#take the average of profit made by movies in each year and plot.
#make the group of the data according to their release_year and find the mean profit and plot.
df_M.groupby('release_year')['revenue'].mean().plot()

#setup the title and labels of the figure.
plt.title("Year Vs Average revenue",fontsize = 10)
plt.xlabel('Release year',fontsize = 10)
plt.ylabel('Average revenue',fontsize =10)

#setup the figure size.
sns.set(rc={'figure.figsize':(10,10)})
sns.set_style("whitegrid")


# According to the plot The Revenue of the movies has increased over the years
#     

# In[ ]:


# Research Question 4 : what are most made geners and most companie produced movies


# In[68]:


df_M['production_companies'].value_counts()


# In[62]:


# using value_counts() to count the number of movies for each genre
df_M['genres'].value_counts()


# In[159]:



#count geners of movies using value_counts().
geners_d = df_M['genres'].value_counts().sort_index()


#plot the bar graph using plot.
geners_d.plot(x='genres',kind='bar',fontsize = 11,figsize=(8,6))

#set the labels and titles of the plot.
plt.title('geners vs value counts',fontsize = 15)
plt.xlabel('genres',fontsize = 13)
plt.ylabel('Number of each gener',fontsize = 13)
sns.set_style("darkgrid")


# The bar chart shows the drame movies are most made 

# <a id='conclusions'></a>
# ## Conclusions
# 
#  <li> Avatar, Star Wars and Titanic are the most profitable movies. <li> Maximum Number Of Movies Release In year 2014. <li> Drame, Comedy and Action are most-made genres.
# <li> The Story of Film: An Odyssey Movie has Highest votes
# <li> Drama is the most popular genre Then comedy then action.
# <li> Short or Long duration movies are more popular than long duration movies.
# <li> The profits of the movies are increasing over the years.
# <li> Revenue is directly connected to the budget.
# <li> Universal Pictures and Paramount Pictures are the most production companies produced Movies
#  
# ## Limitations
# <li> During the data cleaning process, I split the data seperated by '|'  for easy parsing during the exploration phase. This increases the time taken in analysis the data set and .    
# produced missing values 
# <li> The non numeric missing values is harder to handle from numeric values (which can count the mean to fill it  )  
# 

# In[69]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




