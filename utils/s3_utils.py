import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def download_file_from_s3(bucket, object_name, file_name=None):
    """Download a file from an S3 bucket

    :param bucket: Bucket to download from
    :param object_name: S3 object name
    :param file_name: File to download to. If not specified then object_name is used
    :return: True if file was downloaded, else False
    """
    # If file_name was not specified, use object_name
    if file_name is None:
        file_name = object_name

    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        s3_client.download_file(bucket, object_name, file_name)
        print(f"File {object_name} downloaded from {bucket} to {file_name}")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Example usage:
if __name__ == "__main__":
    # Upload a file
    upload_file_to_s3('test_upload.txt', 'your-bucket-name', 'uploaded_test.txt')

    # Download a file
    download_file_from_s3('your-bucket-name', 'uploaded_test.txt', 'downloaded_test.txt')