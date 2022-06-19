import os
import uuid
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


def download_blob_to_file(blob_service_client, container_name, blob_name):
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name)
    stream = blob_client.download_blob()
    download_file_path = "data/"+blob_name.replace("/", "_")
    if (os.path.exists(download_file_path) == False):
        # print("\nDownloading blob to \n\t" + download_file_path)
        with open(download_file_path, "wb") as download_file:
            download_file.write(stream.readall())
    return stream


def f():
    connect_str = "DefaultEndpointsProtocol=https;AccountName=riveriotstorage;AccountKey=sMvbELVCFZ3+/T/V8Ta45wSGPtMkx6Sh/2K89uRFfUN6z1mhwRteGzz6wx2HkpWtqQlLbZ45nwF0sh92IQHbhA==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "riveriotcontainer"
    choosen_date = "2022/06/19"
    blob_name_start = "riverIoT/00/"+choosen_date+"/16"
    print("name: "+blob_name_start)
    container_client = blob_service_client.get_container_client(container_name)
    blobs_list = container_client.list_blobs(
        name_starts_with=blob_name_start)
    names_list = [blob.name for blob in blobs_list]
    all_data = []
    for blob_name in names_list:
        stream = download_blob_to_file(
            blob_service_client, container_name, blob_name)
        start = 0
        while(True):
            start = stream.readall().find(b"{\"deviceData\"", start)
            if(start < 0):
                break
            end = stream.readall().find(b"}}", start)
            all_data.append(json.loads(stream.readall()[
                            start:end+2].decode("utf-8")))
            start = end
    print(all_data)


try:
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
    f()
    print("Done")

except Exception as ex:
    print('Exception:')
    print(ex)
