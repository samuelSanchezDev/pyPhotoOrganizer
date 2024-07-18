"""
Módulo con la funcionalidad de manipular los archivos.
"""

from typing import List, Set
import os
import hashlib


class PyFiles:
    """
    Clase encargada de gestionar los archivos.
    """

    @staticmethod
    def unique_digest(files: List[str]) -> List[str]:
        """
        Método para filtrar los archivos con mismo digest.

        :param files: Lista con los path de los archivos.
        :return: Lista con los path de los archivos con digest único.
        """

        # Se filtran los path que no corresponden a archivos.
        real_files: List[str] = list(filter(os.path.isfile, files))

        # Se calcula el hash de los archivos y se ignoran aquellos duplicados.
        all_hash: Set[bytes] = set()
        unique_files: List[str] = []
        for file in real_files:

            my_hash = hashlib.sha1()
            with open(file, 'rb') as f:
                my_hash.update(f.read())
                digest = my_hash.digest()

            if digest not in all_hash:
                all_hash.add(digest)
                unique_files.append(file)

        return unique_files
