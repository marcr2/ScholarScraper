import pandas as pd
from tqdm import tqdm

def calcNoveltyScore(processed_data, i):
    num_cit = processed_data['num_citations'][i]
    pub_year = processed_data['pub_year'][i]
    age = 2025-pub_year
    weigh_age = age/2
    avg_dev = processed_data['num_citations'].mean() - num_cit
    novelty_score = avg_dev-weigh_age
    return novelty_score

def processLLMData(processed_data):
    print(f"imported {len(processed_data)} articles!")
    dropped_art = len(processed_data) - len(processed_data[processed_data['object'] != 'none'])
    processed_data = processed_data[processed_data['object'] != 'none'].reset_index(drop=True) # remove all none objects
    print(f"Dropped {dropped_art} articles!")
    unique_obj_numb = processed_data['object'].nunique() # count number of unique objects
    print(f"Identified {unique_obj_numb} unique objects!")
    papers_added = 0
    with tqdm(
            total=len(processed_data),
            desc="calculating novelty scores",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            colour="WHITE"
        ) as pbar:
            for i in range(len(processed_data)):
                novelty_score = calcNoveltyScore(processed_data, i)
                processed_data.at[i, 'novelty score'] = novelty_score # append novelty score
                processed_data.to_csv('processed_output.csv', index=False)
                papers_added += 1
                pbar.update(papers_added)
                papers_added = 0
    processed_data = processed_data.sort_values('novelty score', ascending=False)
    processed_data.to_csv('processed_output.csv', index=False)
    return processed_data