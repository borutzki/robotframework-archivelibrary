#!/usr/bin/env python

import zipfile
from pathlib import Path

from robot.api.deco import keyword, library
from utils import Tar, TarGz, Zip
from version import VERSION


@library(scope="GLOBAL", version=VERSION)
class ArchiveLibrary:
    """ArchiveLibrary is a Robot Framework keyword library to
    handle ZIP and possibly other archive formats.
    """

    compressions = {
        "stored": zipfile.ZIP_STORED,
        "deflated": zipfile.ZIP_DEFLATED,
        "bzip2": zipfile.ZIP_BZIP2,
        "lzma": zipfile.ZIP_LZMA,
    }

    tars = [".tar", ".tar.bz2", ".tar.gz", ".tgz", ".tz2"]

    zips = [
        ".docx",
        ".egg",
        ".jar",
        ".odg",
        ".odp",
        ".ods",
        ".xlsx",
        ".odt",
        ".pptx",
        ".zip",
    ]

    def __init__(self):
        pass

    @keyword("Extract Zip File")
    def extract_zip_file(self, zip_file: Path, dest: Path | None = None) -> None:
        """Extract a ZIP file

        `zip_file` the path to the ZIP file

        `dest` optional destination folder. Assumes current working directory if it is none
               It will be created if It doesn't exist.
        """
        if dest is None:
            dest = Path(".")
        zip = Zip(zip_file)
        zip.extract(dest)

    @keyword("Extract Tar File")
    def extract_tar_file(self, tar_file: Path, dest: Path | None = None) -> None:
        """Extract a TAR file

        `tar_file` the path to the TAR file

        `dest` optional destination folder. Assumes current working directory if it is none
               It will be created if It doesn't exist.
        """
        if dest is None:
            dest = Path(".")
        tar = Tar(tar_file)
        tar.extract(dest)

    @keyword("Archive Should Contain File")
    def archive_should_contain_file(self, zip_file: Path, filename: str) -> None:
        """Check if a file exists in the ZIP file without extracting it

        `zip_file` the path to the ZIP file

        `filename` name of the file to search for in `zip_file`
        """
        if zip_file.suffix in self.zips:
            list = Zip(zip_file).list_content()
        elif zip_file.suffix in self.tars:
            list = Tar(zip_file).list_content()
        else:
            raise NameError("Incorrect archive type!")

        assert filename in list, f"File {filename} not found in archive {zip_file}!"

    @keyword("Create Tar From Files In Directory")
    def create_tar_from_files_in_directory(
        self,
        directory: Path,
        filename: Path,
        sub_directories: bool = True,
        tgz: bool = False,
    ):
        """Take all files in a directory and create a tar package from them

        `directory` Path to the directory that holds our files

        `filename` Path to our destination TAR package.

        `sub_directories` Shall files in sub-directories be included - True by default.

        `tgz` Creates a .tgz / .tar.gz archive (compressed tar package) instead of a regular tar - False by default.
        """
        # TODO: Restore option to include / exclude subdirectories
        if tgz:
            TarGz.archive(directory, filename)
        else:
            Tar.archive(directory, filename)

    @keyword("Create Zip From Files In Directory")
    def create_zip_from_files_in_directory(
        cls,
        directory: Path,
        filename: Path,
        sub_directories: bool = False,
        compression: str = "stored",
    ):
        """Take all files in a directory and create a zip package from them

        `directory` Path to the directory that holds our files

        `filename` Path to our destination ZIP package.

        `sub_directories` Shall files in sub-directories be included - False by default.

        `compression` stored (default; no compression), deflated, bzip2 (with python >= 3.3), lzma (with python >= 3.3)
        """
        # TODO: Restore option to include / exclude subdirectories
        # TODO: Restore option to choose compression type
        Zip.archive(directory, filename)
