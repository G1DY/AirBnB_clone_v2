#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["52.87.255.0", "52.3.244.163"]
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distribute an archive to a web server

    Args:
        archive_path(str): The path
    Returns:
        True if successful otherwise an error
    """
    try:
        if not (path.exists(archive_path)):
            return False
        put(archive_path, '/tmp/')
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.
            format(timestamp))
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/ \
            releases/web_static_{}/'..format(timestamp, timestamp))
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
            /data/web_static/releases/web_static_{}/'.format
            (timestamp, timestamp))
        run('sudo rm -rf /data/web_static/releases/ \
            web_static_{}/web_static'.format(timestamp))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/ \
            web_static_{}/ /data/web_static/current'.format(timestamp))
    except Exception as e:
        return False
    return True
