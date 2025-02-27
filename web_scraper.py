import pandas as pd
from scholarly import scholarly
import random
import time
import tensorflow as tf
from tensorflow import keras

def processSearch(publication): # collect data from fetched publication
  title = publication["bib"]["title"]
  abstract = publication["bib"]["abstract"]
  first_author = publication["bib"]["author"][0]
  pub_url = publication["pub_url"]
  num_citations = publication["num_citations"]
  pub_year = publication["bib"]["pub_year"]
  processed_pub = [title, first_author, num_citations, pub_year, pub_url, abstract]
  print(f"Processed publication: {processed_pub}")
  return processed_pub

def search(query,limit): # fetch publications and compile into data table
  search_query = scholarly.search_pubs(query)
  i=0
  data = []
  final_list = pd.DataFrame(data, columns=["title", "first_author", "num_citations", "pub_year", "pub_url", "abstract"])
  for result in search_query:
    if (i < limit):
      processed_result = processSearch(result)
      final_list.loc[len(final_list)] = processed_result
      final_list.to_csv('output.csv', index=False)
      i=i+1
      wait_time = random.randint(10,20) # google scholar's known rate limit is around 5-10 requests per minute, therefore it is important to keep this number above 10 to avoid being ip-banned.
      time.sleep(wait_time)
      print(f"Caught {i} out of {limit} articles! latest wait time: {wait_time}")
      wait_time_list = []
      wait_time_list.append(wait_time)
    else:
      avg_wait_time = sum(wait_time_list)/len(wait_time_list)
      print(f"finished fetching articles! Average wait time: {avg_wait_time}")
      return final_list

q1 = input("What is your Query? ")
l1 = int(input("How many articles do you want to fetch? "))
searchResult = search(q1,l1)
print(searchResult)
