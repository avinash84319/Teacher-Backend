from google.cloud import storage


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
