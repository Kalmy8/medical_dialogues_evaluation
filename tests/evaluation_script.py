import pandas as pd
import asyncio
import aiohttp
import logging
from typing import Dict, Any

# --- Configuration ---
API_URL = "http://localhost:8000/api/score"
INPUT_CSV_PATH = "tests/evaluation_set.csv"
OUTPUT_CSV_PATH = "tests/evaluation_set_results.csv"

# These values are chosen to stay under the OpenAI TPM limit of 30,000.
# (4 workers * (1 req / ~3s)) * 60s/min * 456 tokens/req ~= 27,360 TPM
CONCURRENT_REQUESTS = 4  # Max number of parallel requests
DELAY_AFTER_REQUEST = 2.0 # Seconds to wait after a request completes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def call_api(session: aiohttp.ClientSession, row: pd.Series) -> Dict[str, Any]:
    """Calls the scoring API for a single row of data."""
    payload = {
        "section_text": row["section_text"],
        "dialogue": row["dialogue"]
    }
    try:
        async with session.post(API_URL, json=payload, timeout=60) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        logging.error(f"API request failed for row {row.name}: {e}")
        return {
            "chief_complaint_documented": False,
            "individual_treatment_plan_developed": False,
            "specific_treatment_goals_established": False,
            "standardized_assessment_tools_used": False,
        }
    except asyncio.TimeoutError:
        logging.error(f"API request timed out for row {row.name}")
        return {
            "chief_complaint_documented": False,
            "individual_treatment_plan_developed": False,
            "specific_treatment_goals_established": False,
            "standardized_assessment_tools_used": False,
        }


async def process_row_with_limiter(session: aiohttp.ClientSession, row: pd.Series, semaphore: asyncio.Semaphore):
    """Wrapper to process a single row with semaphore and a delay."""
    async with semaphore:
        result = await call_api(session, row)
        await asyncio.sleep(DELAY_AFTER_REQUEST)
        return result


async def main():
    """Main function to run the evaluation script."""
    logging.info(f"Reading data from {INPUT_CSV_PATH}...")
    try:
        df = pd.read_csv(INPUT_CSV_PATH)
    except FileNotFoundError:
        logging.error(f"Input file not found at: {INPUT_CSV_PATH}")
        return

    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, row in df.iterrows():
            tasks.append(process_row_with_limiter(session, row, semaphore))

        logging.info(f"Starting API calls for {len(df)} rows (Concurrency: {CONCURRENT_REQUESTS}, Delay: {DELAY_AFTER_REQUEST}s)...")
        
        # Use a list to store results and track progress
        all_results = []
        for i, task in enumerate(asyncio.as_completed(tasks)):
            result = await task
            all_results.append(result)
            
            if (i + 1) % 10 == 0 or (i + 1) == len(tasks):
                logging.info(f"Progress: {i + 1}/{len(tasks)} tasks completed.")

    logging.info("Processing results...")
    results_df = pd.DataFrame(all_results)
    
    # Concatenate the original DataFrame with the results
    final_df = pd.concat([df, results_df], axis=1)

    logging.info(f"Saving results to {OUTPUT_CSV_PATH}...")
    final_df.to_csv(OUTPUT_CSV_PATH, index=False)
    logging.info("Evaluation finished successfully.")


if __name__ == "__main__":
    asyncio.run(main())
