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
    result = local("tar -czvf {} web_static".format(archive_path))

    if result.succeeded:
        return "versions/web_static_{}.tgz".format(archive_path)
    else:
        return None
