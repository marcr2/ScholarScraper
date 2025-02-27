# import tensorflow as tf # errors with tensorflow import
# from tensorflow import keras
import pandas as pd

def processWSData():
    processType = input("Will you be using LLM or NLP? ")
    import_data = pd.read_csv('output.csv')
    abstracts = import_data['abstract']
    abstracts_length = len(abstracts)
    abstracts_range = range(abstracts_length)
    print(f"imported {abstracts_length} articles!")
    if (processType == "LLM"):
        for i in abstracts_range :
            abstract_rows = abstracts[i]
            llmRead(abstract_rows)
            print(f"read {i} articles!")
    elif (processType == "NLP"):
        nlp_type = input("Which NLP will you be using? ")
        nlpRead(input)
    else:
        print("Invalid process")
        return

def llmRead(abstract_rows):
    print(abstract_rows)
    
def nlpRead(abstract_rows):
    print(abstract_rows)

processWSData()