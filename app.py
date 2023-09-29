from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

app = Flask(__name__)

# Azure Storage Account Configuration
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=utkarshdemorg8b53;AccountKey=dI/84oeqNwqFsd09AJ/AnbW9cqLi+F8fOow+tj/B0ofVkA2kM46gEaY9t3v/m0L7SZSd/LHPBYXn+ASta8L1cQ==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "demo-ml-project"  # Replace with your container name

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]

        if file:
            # Get the filename
            filename = secure_filename(file.filename)
            
            # Create a blob client and upload the file to Azure Blob Storage
            blob_client = container_client.get_blob_client(filename)
            blob_client.upload_blob(file)

            return redirect(url_for("list_files"))

    return render_template("upload.html")

@app.route("/list")
def list_files():
    # List all files in the Azure Blob Storage container
    blob_list = []
    for blob in container_client.list_blobs():
        blob_list.append(blob.name)

    return render_template("list.html", blob_list=blob_list)

if __name__ == "__main__":
    from werkzeug.utils import secure_filename
    app.secret_key = os.urandom(24)
    app.run(debug=False)
