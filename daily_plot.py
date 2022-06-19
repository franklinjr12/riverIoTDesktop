import os
import uuid
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import numpy
import matplotlib.pyplot as plt


def f():
    connect_str = ""
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # # List all containers
    # all_containers = blob_service_client.list_containers(include_metadata=True)
    # for container in all_containers:
    #     print(container['name'], container['metadata'])
    # Get a client to interact with a specific container - though it may not yet exist
    datas = []
    download_file_path = "DOWNLOAD.txt"
    if (os.path.exists(download_file_path) == False):
        container_name = ""
        blob_name_path = "riverIoT/00/2021/09/30/00/.avro"
        container_client = blob_service_client.get_container_client(
            container_name)
        # for blob in container_client.list_blobs():
        #     print("Found blob: ", blob.name)
        for minute in range(59):
            try:
                blob_name = ""
                if (minute < 10):
                    blob_name = blob_name_path[:len(
                        blob_name_path)-5] + "0" + str(minute) + blob_name_path[len(blob_name_path)-5:]
                else:
                    blob_name = blob_name_path[:len(
                        blob_name_path)-5] + str(minute) + blob_name_path[len(blob_name_path)-5:]

                blob_client = blob_service_client.get_blob_client(
                    container=container_name, blob=blob_name)
                stream = blob_client.download_blob()

                data = "".join(map(chr, stream.readall()))
                pos1 = data.find("{\"deviceData")
                pos2 = data.find("}}", pos1)
                # print(data[pos1:pos2+1])
                j = json.loads(data[pos1:pos2+2])
                # print(j)
                datas.append(j)

                with open(download_file_path, "a") as download_file:
                    download_file.write(data[pos1:pos2+2]+"\n")
                # download_file.write(blob_client.download_blob().readall())

            except Exception as ex:
                print(ex)
    else:
        with open(download_file_path, "r") as download_file:
            for line in download_file.readlines():
                datas.append(json.loads(line))
    # print(datas)
    temperature = []
    for e in datas:
        print(e)
        temperature.append(e["deviceData"]["t"])
    plt.plot(range(len(datas)), temperature)
    plt.show()


try:
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")

    # Quick start code goes here

    f()

    # # CONNECT TO STORAGE
    # connect_str = "DefaultEndpointsProtocol=https;AccountName=riveriotstorage;AccountKey=sMvbELVCFZ3+/T/V8Ta45wSGPtMkx6Sh/2K89uRFfUN6z1mhwRteGzz6wx2HkpWtqQlLbZ45nwF0sh92IQHbhA==;EndpointSuffix=core.windows.net"

    # # === CREATE CONTAINER ===
    # # Create the BlobServiceClient object which will be used to create a container client
    # blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # # Create a unique name for the container
    # container_name = str(uuid.uuid4())

    # # Create the container
    # container_client = blob_service_client.create_container(container_name)
    # container_client = blob_service_client.g

    # # === UPLOAD BLOB ===
    # # Create a local directory to hold blob data
    # local_path = "./data"
    # os.mkdir(local_path)

    # # Create a file in the local data directory to upload and download
    # local_file_name = str(uuid.uuid4()) + ".txt"
    # upload_file_path = os.path.join(local_path, local_file_name)

    # # Write text to the file
    # file = open(upload_file_path, 'w')
    # file.write("Hello, World!")
    # file.close()

    # # Create a blob client using the local file name as the name for the blob
    # blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    # # Upload the created file
    # print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
    # with open(upload_file_path, "rb") as data:
    #     blob_client.upload_blob(data)

    # # === LIST BLOBS ===
    # # List the blobs in the container
    # print("\nListing blobs...")
    # blob_list = container_client.list_blobs()
    # for blob in blob_list:
    #     print("\t" + blob.name)

    # # Download the blob to a local file
    # # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
    # download_file_path = os.path.join(local_path, str.replace(
    #     local_file_name, '.txt', 'DOWNLOAD.txt'))
    # print("\nDownloading blob to \n\t" + download_file_path)

    # with open(download_file_path, "wb") as download_file:
    #     download_file.write(blob_client.download_blob().readall())

    # # === DELETE CONTAINER ===
    # # Clean up
    # print("\nPress the Enter key to begin clean up")
    # input()

    # print("Deleting blob container...")
    # container_client.delete_container()

    # print("Deleting the local source and downloaded files...")
    # os.remove(upload_file_path)
    # os.remove(download_file_path)
    # os.rmdir(local_path)

    print("Done")

except Exception as ex:
    print('Exception:')
    print(ex)
