#!/usr/bin/python3
"""a fabricfile that generates .tgz archive"""
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
        file_size = result.stdout.split()[-2]
        print("web_static packed: {} -> {}Bytes".format(archive_path,
              file_size))
        return "versions/web_static_{}.tgz".format(archive_path)
    else:
        return None
