#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import pandas as pd
import logging
from typing import List

# Local modules
import src.utilities as utils

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load configuration
config = utils.read_config()

# Constants for paths
API_ENDPOINT = "http://api.getthedata.com/postcode/"

def load_data(filepath: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    logging.info(f"Loading data from {filepath}")
    return utils.load_data(filepath)

def extract_postal_codes(df: pd.DataFrame) -> List[str]:
    """Extract and clean postal codes from the dataframe."""
    return df['postal_code'].astype(str).str.replace(" ", "").tolist()

def fetch_postcode_data(postal_code: str) -> dict:
    """Fetch latitude and longitude for a given postal code using the API."""
    url = f"{API_ENDPOINT}{postal_code}"
    
    try:
        response = requests.get(url, timeout=5)  # Set timeout to prevent hanging requests
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        data = response.json()

        if 'data' in data and data['status'] == 'match':
            return {
                'postal_code': data['data']['postcode'],
                'latitude': data['data']['latitude'],
                'longitude': data['data']['longitude']
            }
        else:
            logging.warning(f"No match found for postal code: {postal_code}")
            return {'postal_code': postal_code, 'latitude': None, 'longitude': None}

    except requests.RequestException as e:
        logging.error(f"Error fetching data for {postal_code}: {e}")
        return {'postal_code': postal_code, 'latitude': None, 'longitude': None}

def download_postcode_data(postal_codes: List[str]) -> pd.DataFrame:
    """Retrieve latitude and longitude data for all postal codes."""
    logging.info("Fetching postcode data...")
    records = [fetch_postcode_data(pc) for pc in postal_codes]
    return pd.DataFrame(records)

def merge_data(df: pd.DataFrame, postcode_data: pd.DataFrame) -> pd.DataFrame:
    """Merge the original dataframe with postcode data."""
    return df.merge(postcode_data, how='left', on='postal_code')

def main():
    data_path = os.path.join(config['data']['intFilePath'], "state_of_our_prisons/private_prisons.csv")
    df = load_data(data_path)
    postal_codes = extract_postal_codes(df)
    postcode_data = download_postcode_data(postal_codes)
    df_final = merge_data(df, postcode_data)

    output_filepath = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/private_prisons.csv")
    logging.info(f"Saving enhanced data to {output_filepath}")
    df_final.to_csv(output_filepath, index=False)
    logging.info("Processing complete.")

if __name__ == '__main__':
    main()