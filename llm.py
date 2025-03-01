import pandas as pd
import openai
import json
from tqdm import tqdm

with open('keys.json', 'r') as f:
    keys = json.load(f)
deep_seek_api_key = keys['deep_seek_api_key']
openai.api_key = deep_seek_api_key
openai.api_base = "https://api.deepseek.com"

def processWSData(processType):
    import_data = pd.read_csv('output.csv')
    abstracts = import_data['abstract']
    abstracts_length = len(abstracts)
    print(f"imported {abstracts_length} articles!")
    import_data['object'] = None
    import_data['novelty score'] = None
    if processType == 'LLM':
        print("LLM loaded!")
    return import_data

def llmRead(import_data, field, target_object):
    papers_added = 0
    with tqdm(
        total=len(import_data),
        desc="categorizing abstracts",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        colour="WHITE"
    ) as pbar:
        for i in range(len(import_data)):  # categorize each abstract with a specific object
            role_prompt = (
                f"You are an expert in {field}. For the given text, please only return one single "
                f"word that best identifies the specific {target_object} in the text. Do not return a phrase "
                f"or a sentence or a general group of {target_object}. If given a category of things, specify "
                f"what part of that category the focus is on. If you cannot identify the specific {target_object}, "
                f"please return 'none'."
            )
            prompt = f"{import_data['abstract'][i]}"
            response = openai.ChatCompletion.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": role_prompt},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
            import_data.at[i, 'object'] = response.choices[0].message.content
            import_data.to_csv('processed_output.csv', index=False)
            papers_added += 1
            pbar.update(papers_added)
            papers_added = 0
    import_data.to_csv('processed_output.csv', index=False)
    return import_data