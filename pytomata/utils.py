import os

from proto import module

def rmdir(sftp, path):
    files = sftp.listdir(path)

    for f in files:
        filepath = os.path.join(path, f)
        try:
            sftp.remove(filepath)
        except IOError:
            rmdir(sftp, filepath)

    sftp.rmdir(path)


def get_module_func(module: module, func: str):
    """Get a function from a module by name."""
    if hasattr(module, func) and callable(getattr(module, func)):
       return getattr(module, func)
    else:
        return None
