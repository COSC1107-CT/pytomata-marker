import os

def rmdir(sftp, path):
    files = sftp.listdir(path)

    for f in files:
        filepath = os.path.join(path, f)
        try:
            sftp.remove(filepath)
        except IOError:
            rmdir(sftp, filepath)

    sftp.rmdir(path)


def report_progress_bytes_transfered(xfer, to_be_xfer, job_id, logger):
    remains_per = 0.000
    remains_per = (xfer / to_be_xfer) * 100
    logger.debug(
        f"Complete percent for job {job_id}: {remains_per:.2f}% - ({xfer} bytes transfered out of {to_be_xfer})"
    )

