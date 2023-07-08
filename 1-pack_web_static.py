#!/usr/bin/python3
"""a fabricfile that generates .tgz archive"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates tgz archive from contents of web_static folder"""
    archive_path = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(archive_path))

        return "versions/web_static_{}.tgz".format(archive_path)
    except Exception as e:
        return None
