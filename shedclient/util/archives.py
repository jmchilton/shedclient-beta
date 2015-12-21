# Safely extract tarball - using approach outlined here
# http://stackoverflow.com/questions/10060069/safely-extract-zip-or-tar-using-python
import tarfile
from os.path import abspath, realpath, dirname, join as joinpath

import logging
log = logging.getLogger(__name__)

resolved = lambda x: realpath(abspath(x))


def extract_file_safely(tar_path, to_directory):
    ar = tarfile.open(tar_path, "r:*")
    try:
        members = _safe_members(to_directory, ar)
        ar.extractall(path=to_directory, members=members)
    finally:
        ar.close()


def _safe_members(destination, members):
    base = resolved(destination)

    for finfo in members:
        if _bad_path(finfo.name, base):
            log.warn(finfo.name + " is blocked (illegal path)")
        elif finfo.issym() and _bad_link(finfo, base):
            log.warn(finfo.name + "is blocked: Hard link to" + finfo.linkname)
        elif finfo.islnk() and _bad_link(finfo, base):
            log.warn(finfo.name + "is blocked: Symlink to" + finfo.linkname)
        else:
            yield finfo


def _bad_path(path, base):
    # joinpath will ignore base if path is absolute
    return not resolved(joinpath(base, path)).startswith(base)


def _bad_link(info, base):
    # Links are interpreted relative to the directory containing the link
    tip = resolved(joinpath(base, dirname(info.name)))
    return _bad_path(info.linkname, base=tip)
