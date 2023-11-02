import boto3 
import os 
from botocore.client import Config
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from boto3.session import Session


BUCKET_NAME = 'aws-bucket-smart-analytics'
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID, 
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def download_file(bucket_name, bucket_path, dest_path):

    print(f"Downloading file...")
    
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.download_file(bucket_path, dest_path)

    print(f"Download File {bucket_path} at {dest_path}")


def get_files_objects(bucket_name, bucket_folder):

   

    all_objs = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{bucket_folder}", Delimiter="/")

    files_objs = []

    for obj in all_objs['Contents']:
        if obj['Key'] == bucket_folder:
            continue
        files_objs.append(obj)
    
    return files_objs


def download_all_files(bucket_name, bucket_folder):
    
    files_objs = get_files_objects(bucket_name, bucket_folder)

    for obj in files_objs:
        bucket_file_path = obj['Key']
        file_name = os.path.basename(bucket_file_path)
        dest_path = f"{out_folder}/{file_name}"

        download_file(bucket_name, bucket_file_path, dest_path)


if __name__ == '__main__':
    bucket_name = BUCKET_NAME
    out_folder = 'EDA'
    #file_path = "clean_data/clean_taxi_zone.csv"
    #out_path = "EDA/totals-watch-time.csv"
    
    download_all_files(bucket_name, "clean_data/")