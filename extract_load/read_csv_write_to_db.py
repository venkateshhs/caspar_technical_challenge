import os
import traceback
import pandas as pd
from sqlalchemy import create_engine
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from common_methods import get_credentials, setup_logging, test_connection
import logging

setup_logging()

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join('env', '.env'))

# Retrieve the encryption key from environment variables
key = os.getenv('ENCRYPTION_KEY').encode()
cipher_suite = Fernet(key)


def encrypt_data(data):
    """ Encrypt data using Fernet symmetric encryption. """
    return cipher_suite.encrypt(data.encode()).decode()


def data_ingestion():
    try:
        creds = get_credentials()
        engine = create_engine(
            f"postgresql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['dbname']}")

        if test_connection(engine):
            logging.info("DB Connected successfully")
        else:
            logging.error("DB Connection error")
            return

        data_dir = os.path.join(os.getcwd(), 'Data')
        steps_df = pd.read_csv(os.path.join(data_dir, 'steps.csv'))
        exercises_df = pd.read_csv(os.path.join(data_dir, 'exercises.csv'))
        patients_df = pd.read_csv(os.path.join(data_dir, 'patients.csv'))
        logging.info(f'Steps DataFrame example:\n{steps_df.head(2)}')
        logging.info(f'exercises_df  DataFrame example:\n{exercises_df.head(2)}')
        logging.info(f'patients  DataFrame example:\n{patients_df.head(2)}')

        # Encrypt the first_name and last_name columns
        patients_df['first_name'] = patients_df['first_name'].apply(encrypt_data)
        patients_df['last_name'] = patients_df['last_name'].apply(encrypt_data)

        # Write data to PostgreSQL database
        steps_df.to_sql('steps', engine, if_exists='replace', index=False)
        exercises_df.to_sql('exercises', engine, if_exists='replace', index=False)
        patients_df.to_sql('patients', engine, if_exists='replace', index=False)

        logging.info("Data uploaded successfully!")

    except Exception as e:
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    data_ingestion()
