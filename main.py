import argparse
import pandas as pd
import json
import os
import csv
from tqdm import tqdm

from dotenv import load_dotenv

from api.remote import generate_response_api
from api.local import generate_response_local
from prompt import prompt_template

load_dotenv()

parser = argparse.ArgumentParser(description='Run LLM locally or from an API provider')
parser.add_argument('--mode', choices=['local', 'remote'], default='remote', required=True,
                    help='Choose the mode to run the LLM')
args = parser.parse_args()

model = os.environ['MODEL']

dataset_path = 'data/raw_data.csv'

dataset = pd.read_csv(dataset_path)

personalities_path = 'data/persona.json'
personalities = []
for personas in json.load(open(personalities_path)).values():
    personalities.extend(personas)

for persona_index in range(3):
    for col, data in tqdm(dataset.iterrows(), total=len(dataset), desc="Processing"):
        for persona in personalities:
            query = prompt_template.create_prompt(data['country'], data['story'], persona_index, persona)

            try: 
                if args.mode == 'local':
                    response = generate_response_local(model, query, max_tokens=10)
                else:
                    response = generate_response_api(model, query, max_tokens=10)

                dataset.loc[col, persona] = response.lower()

            except Exception as e:
                print("An error occurred", e)
                dataset.loc[col, persona] = "error"

    if not os.path.exists('results'):
        os.makedirs('results')
    if not os.path.exists(f'results/{model}'):
        os.makedirs(f'results/{model}')
        
    dataset.to_csv(f'results/{model}/results_{persona_index}.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
