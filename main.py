import argparse
import pandas as pd
import json
import os
import csv
from tqdm import tqdm
from dotenv import load_dotenv
from api.remote import generate_response_api
from api.local import generate_response_local_parallel
from prompt import prompt_template

load_dotenv()

parser = argparse.ArgumentParser(description='Run LLM locally or from an API provider')
parser.add_argument('--mode', choices=['local', 'remote'], default='remote', required=True,
                    help='Choose the mode to run the LLM')
args = parser.parse_args()

model = os.environ['MODEL']

dataset_path = 'data/raw_data.csv'
personalities_path = 'data/persona.json'

personalities = []
for personas in json.load(open(personalities_path)).values():
    personalities.extend(personas)

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

for persona_index in range(3):
    dataset = pd.read_csv(dataset_path)

    for col, data in tqdm(dataset.iterrows(), total=len(dataset), desc="Processing"):
        queries = []
        for persona in personalities:
            query = prompt_template.create_prompt(data['country'], data['story'], persona_index, persona)
            queries.append((col, persona, query))

        for query_batch in batch(queries, 4):
            if args.mode == 'local':
                results = generate_response_local_parallel(model, [q[2] for q in query_batch], temperature=0.5, max_tokens=512, max_workers=4)
            else:
                results = [(q[2], generate_response_api(model, q[2], max_tokens=10)) for q in query_batch]

            for (col, persona, _), (_, result) in zip(query_batch, results):
                try:
                    dataset.loc[col, persona] = result.lower()
                except Exception as e:
                    print("An error occurred", e)
                    dataset.loc[col, persona] = "error"

    if not os.path.exists('results'):
        os.makedirs('results')
    if not os.path.exists(f'results/{model}'):
        os.makedirs(f'results/{model}')
        
    dataset.to_csv(f'results/{model}/results_{persona_index}.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
