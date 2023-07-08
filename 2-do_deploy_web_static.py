#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["52.87.255.0", "52.3.244.163"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        print("Archive file not found.")
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    print("Uploading archive to the web server...")
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        print("Failed to upload the archive.")
        return False

    print("Creating release directory: /data/web_static/releases/{}/".\
          format(name))
    if run("rm -rf /data/web_static/releases/{}/".format(name)).\
           failed is True:
        print("Failed to remove the previous release directory.")
        return False

    if run("mkdir -p /data/web_static/releases/{}/".format(name)).\
           failed is True:
        print("Failed to create the release directory.")
        return False

    print("Extracting archive to the release directory...")
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".\
           format(file, name)).failed is True:
        print("Failed to extract the archive.")
        return False

    print("Removing the archive from the web server...")
    if run("rm /tmp/{}".format(file)).failed is True:
        print("Failed to remove the archive.")
        return False

    print("Moving contents to the release directory...")
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/\
           releases/{}/".format(name, name)).failed is True:
        print("Failed to move contents to the release directory.")
        return False

    print("Removing the redundant web_static directory...")
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).\
           failed is True:
        print("Failed to remove the redundant web_static directory.")
        return False

    print("Removing the current symbolic link...")
    if run("rm -rf /data/web_static/current").failed is True:
        print("Failed to remove the current symbolic link.")
        return False

    print("Creating new symbolic link...")
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".\
           format(name)).failed is True:
        print("Failed to create the new symbolic link.")
        return False

    print("New version deployed!")

    # Print the HTML content of 0-index.html
    index_html_path = "/data/web_static/releases/{}/{}".\
                      format(name, "0-index.html")
    print("Printing the HTML content of 0-index.html:")
    print(run("cat {}".format(index_html_path)).stdout)

    return True
