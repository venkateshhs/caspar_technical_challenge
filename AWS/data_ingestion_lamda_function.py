import os
import logging
import boto3
import traceback
import awswrangler as wr
import pg8000
import pandas as pd


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_db_connection():
    """
    Get credentials from Environment_Variables, establish and return a PostgreSQL database connection using psycopg2.
    """
    logger.info("Establishing database connection")
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_port = os.environ.get('DB_PORT')

    try:
        conn = pg8000.connect(
            user=db_user,
            host=db_host,
            database=db_name,
            port=db_port,
            password=db_password
        )
        logger.info("Database connection established")
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None


def lambda_handler(event, context):
    logger.info("Lambda function triggered")
    # Extract S3 event information
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    logger.info(f"Processing file {key} from bucket {bucket}")

    try:
        s3_client = boto3.client('s3', "eu-central-1")
        response = s3_client.get_object(Bucket=bucket, Key=key)
        data_df = pd.read_csv(response.get("Body"))
        logger.info(f"data_df:{data_df.head(5)}")
        # This is to remove a unnamed column in patients.csv
        if 'Unnamed: 0' in data_df.columns:
            del data_df['Unnamed: 0']

        logger.info(f"data_df:{data_df.head(5)}")
        table_name = key.split('.')[0]
        conn = get_db_connection()
        if conn:
            wr.postgresql.to_sql(
                df=data_df,
                table=table_name,
                schema="public",
                con=conn
            )

            conn.close()
            logger.info(f"Data written successfully to RDS table: {table_name}.")
        else:
            logger.error("Database connection failed.")

        return {'status': "SUCCESS", "message": f"data successfully written to RDS table: {table_name}"}

    except Exception as e:
        logger.error(f"Error processing S3 event: {e}")
        err = traceback.format_exc()
        logger.error(f'Traceback: {err}')
        return {'status': "ERROR", "message": "RDS write failed"}

