from google.cloud import storage
from pdfminer.high_level import extract_text
import io


def upload_blob(path,gcp_path):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "teacherstudent"
    # The path to your file to upload
    source_file_name = path
    # The ID of your GCS object
    destination_blob_name = gcp_path

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    blob.make_public()

    file_url = blob.public_url

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

    return file_url


def check_bucket():
    """Check if the bucket exists"""
    bucket_name = "teacherstudent"
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
        return True
    except:
        return False

def get_pdf_text_from_gcp(pdf_path):
    """Get the text from the PDF stored on Google Cloud Storage."""

    try:
        print(pdf_path)

        bucket_name = "teacherstudent"
        storage_client = storage.Client()

        path = pdf_path.split("/")[-1]
        print(path)

        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(path)
        # Download PDF as a binary file
        pdf_content = blob.download_as_bytes()
        # Extract text from the binary PDF using pdfminer.six
        text = extract_text(io.BytesIO(pdf_content))

        return text

    except Exception as e:

        print(e)

        return False