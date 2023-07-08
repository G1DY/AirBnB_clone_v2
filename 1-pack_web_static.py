#!/usr/bin/python3
"""a fabricfile that generates .tgz archive"""
import os.path
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates tgz archive from contents of web_static folder"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    local("mkdir -p versions")
    result = local("tar -czvf {} web_static".format(archive_path),
                   capture=True)

    if result.succeeded:
        file_size_output = result.stdout
        print(file_size_output)
        lines = file_size_output.split("\n")
        file_size = None
        for line in lines:
            if "web_static" in line:
                file_info = line.split()
                if len(file_info) >= 3:
                    file_size = file_info[2]
                break
        if file_size:
            print("web_static packed: {} -> {}Bytes".format(archive_path,
                  file_size))
            print("List of files added to the archive:")
            print(file_size_output)
            return archive_path
        else:
            print("Error: Unable to determine file size.")
    else:
        print("Error: Failed to generate the archive.")

    return None
