import pandas as pd
import openai
import json
import time
from tqdm import tqdm

with open('keys.json', 'r') as f:
    keys = json.load(f)

deep_seek_api_key = keys['deep_seek_api_key']
openai.api_key = deep_seek_api_key
openai.api_base = "https://api.deepseek.com"

def processWSData(processType):
    import_data = pd.read_csv('output.csv')
    abstracts = import_data['abstract']
    print(f"imported {len(abstracts)} articles!")
    import_data['object'] = None
    import_data['novelty score'] = None
    if processType == 'LLM':
        print("LLM loaded!")
    return import_data

def safe_chat_completion(messages, model="deepseek-chat", retries=3, wait_seconds=5):
    for attempt in range(1, retries + 1):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                stream=False
            )
            return response
        except openai.error.APIConnectionError as e:
            print(f"[Attempt {attempt}] Connection error: {e}")
        except openai.error.OpenAIError as e:
            print(f"[Attempt {attempt}] OpenAI error: {e}")
        except Exception as e:
            print(f"[Attempt {attempt}] Unexpected error: {e}")

        if attempt < retries:
            print(f"Retrying in {wait_seconds * attempt} seconds...")
            time.sleep(wait_seconds * attempt)
    raise RuntimeError("OpenAI API failed after multiple attempts.")

def llmRead(import_data, field, target_object):
    with tqdm(
        total=len(import_data),
        desc="categorizing abstracts",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        colour="WHITE"
    ) as pbar:
        for i in range(len(import_data)):
            role_prompt = (
                f"You are an expert in {field}. For the given text, please only return one single "
                f"word that best identifies the specific {target_object} in the text. Do not return a phrase "
                f"or a sentence or a general group of {target_object}. If given a category of things, specify "
                f"what part of that category the focus is on. If you cannot identify the specific {target_object}, "
                f"please return 'none'. Use academic or canonical names if applicable."
            )
            prompt = f"Title: {import_data['title'][i]}, Abstract: {import_data['abstract'][i]}"

            messages = [
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": prompt}
            ]

            try:
                response = safe_chat_completion(messages)
                import_data.at[i, 'object'] = response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Failed to process abstract {i}: {e}")
                import_data.at[i, 'object'] = "error"

            import_data.to_csv('processed_output.csv', index=False)
            pbar.update(1)

    import_data.to_csv('processed_output.csv', index=False)
    return import_data
