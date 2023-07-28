from fabric.api import local
from datetime import datetime

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    local("mkdir -p versions")
    result = local("tar -czvf {} web_static".format(archive_path), capture=True)

    if result.succeeded:
        file_size = result.stdout.split()[-2]
        print("web_static packed: {} -> {}Bytes".format(archive_path, file_size))
        return archive_path
    else:
        return None
