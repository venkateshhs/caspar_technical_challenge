import os
import traceback
import pandas as pd
from sqlalchemy import create_engine
import logging
from datetime import datetime
import time

def get_credentials():
    """ Load database credentials from environment variables or hard-coded for Docker use. """
    credentials = {
        'host': 'postgres',  # Docker service name
        'dbname': 'docker_hospital_database',
        'user': 'postgres',
        'password': 'root',
        'port': '5432'
    }
    return credentials

def setup_logging():
    """ Sets up logging to stdout to take advantage of Docker's logging mechanism. """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    return logging.getLogger(__name__)

def test_connection(engine):
    """ Test the database connection with retry logic. """
    max_attempts = 5
    retry_delay = 5  # seconds
    for attempt in range(max_attempts):
        try:
            with engine.connect() as conn:
                logging.info("Database connection successful.")
                return True
        except Exception as e:
            logging.error(f"Database connection failed on attempt {attempt + 1}: {e}")
            if attempt < max_attempts - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error("All connection attempts failed.")
    return False

def data_ingestion():
    """ Main function to ingest data from CSV to PostgreSQL. """
    logger = setup_logging()
    creds = get_credentials()
    engine = create_engine(
        f"postgresql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['dbname']}")

    if not test_connection(engine):
        logger.error("Database connection error. Exiting.")
        return

    data_dir = '/data'  # Assuming '/data' is the Docker volume path mounted to the host
    try:
        steps_df = pd.read_csv(os.path.join(data_dir, 'steps.csv'))
        exercises_df = pd.read_csv(os.path.join(data_dir, 'exercises.csv'))
        patients_df = pd.read_csv(os.path.join(data_dir, 'patients.csv'))

        steps_df.to_sql('steps', engine, if_exists='replace', index=False)
        exercises_df.to_sql('exercises', engine, if_exists='replace', index=False)
        patients_df.to_sql('patients', engine, if_exists='replace', index=False)

        logger.info("Data uploaded successfully!")
    except Exception as e:
        logger.error(f"An error occurred: {traceback.format_exc()}")

if __name__ == "__main__":
    data_ingestion()
