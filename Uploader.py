import sys
import argparse
import logging
from azure.storage.blob import BlockBlobService, PublicAccess, ContentSettings
import os
import mimetypes

class ABSUtil:
    # init constract
    def __init__(self, account_name, account_key, container_name):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.object = BlockBlobService(
            account_name=self.account_name, account_key=self.account_key)

        print("account_name=" + account_name)
        print("account_key=" + account_key)
        print("container_name=" + container_name)
        

    def upload(self, dest, file_path):
        self.object.create_blob_from_path(self.container_name, dest, file_path,
                                  content_settings=ContentSettings(mimetypes.guess_type(file_path)[0]))
        print("dest=" + dest)
        print("file_path=" + file_path)


    def upload_dir(self, dest, dir_path):
        for root, dirs, files in os.walk(dir_path):
            for filename in files:
                self.upload(os.path.join(dest, root, filename),
                            os.path.join(root, filename))
        print("dest=" + dest)
        print("dir_path=" + dir_path)

def main():
    parser = argparse.ArgumentParser(description='write something')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False, dest='debug', help='debug mode')
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False, dest='verbose', help='verbose mode')
    parser.add_argument(
        '-p', '--path', dest='path', help='destination file path')
    parser.add_argument(
        '-f', '--folder', dest='dir', help='source file directory')
    parser.add_argument(
        '-k', '--key', dest='key', help='key for ABS')
    parser.add_argument(
        '-a', '--account', dest='account', help='account for ABS')
    parser.add_argument(
        '-c', '--container', dest='container', help='container for ABS')
    args = parser.parse_args()
    service = ABSUtil(args.account, args.key, args.container)
    
    if  os.path.isfile(args.dir):
        service.upload(args.path, args.dir)
    else:
        service.upload_dir(args.path, args.dir)


if __name__ == "__main__":
    main()
