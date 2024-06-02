import zipfile
import tarfile
from abc import ABC, abstractmethod
from pathlib import Path
import shutil


class AbstractArchive(ABC):
    """Abstract base class for all types of archives."""

    @abstractmethod
    def __init__(self, path: Path) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def archive(directory: Path, destination: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def extract(self, destination: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_content(self) -> list[str]:
        raise NotImplementedError


class Zip(AbstractArchive):
    def __init__(self, path: Path) -> None:
        self.zip = zipfile.ZipFile(path)

    @staticmethod
    def archive(directory: Path, destination: Path) -> None:
        shutil.make_archive(
            base_name=destination,
            format="zip",
            root_dir=directory,
            base_dir=directory,
        )

    def extract(self, destination: Path) -> None:
        self.zip.extractall(destination)

    def list_content(self) -> list[str]:
        return self.zip.namelist()


class Tar(AbstractArchive):
    def __init__(self, path: Path) -> None:
        self.tar = tarfile.TarFile(path)

    @staticmethod
    def archive(directory: Path, destination: Path) -> None:
        shutil.make_archive(
            base_name=destination,
            format="tar",
            root_dir=directory,
            base_dir=directory,
        )

    def extract(self, destination: Path) -> None:
        self.tar.extractall(destination)

    def list_content(self) -> list[str]:
        return self.tar.getnames()


class TarGz(Tar):
    @staticmethod
    def archive(directory: Path, destination: Path) -> None:
        shutil.make_archive(
            base_name=destination,
            format="gztar",
            root_dir=directory,
            base_dir=directory,
        )
