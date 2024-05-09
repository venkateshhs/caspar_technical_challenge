import os
from datetime import datetime
import logging

from dotenv import load_dotenv


def test_connection(engine):
    try:
        conn = engine.connect()
        conn.close()
        return True
    except Exception as e:
        return False

def get_credentials():
    """
    Load database credentials from an .env file and return them.
    """
    dotenv_path = os.path.join(os.path.dirname(__file__), 'env', '.env')
    load_dotenv(dotenv_path)

    credentials = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', '5432')
    }
    return credentials


def setup_logging():
    """
    Sets up the logging configuration.
    """
    logs_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(logs_dir, f'{timestamp}_data_ingestion.log')

    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    return logging.getLogger(__name__)
