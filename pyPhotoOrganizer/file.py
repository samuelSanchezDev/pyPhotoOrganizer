"""
Módulo con la funcionalidad de manipular los archivos.
"""

import datetime
import re
from typing import List, Set, Tuple
import os
import hashlib

DATE_FORMAT = r'(\d{4})(\d{2})(\d{2})'  # Mach para fechas en formato YYYYMMDD


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

    @staticmethod
    def date_from_name(file: str) -> Tuple[int, int, int]:
        """
        Método para obtener la fecha del archivo del nombre (tiene que estar
        con la forma YYYYMMDD). La función no comprueba que el archivo exista.

        :param file: path del archivo.
        :return: una tupla con el año, mes y día del archivo.
        """

        # Se obtiene el nombre del archivo.
        file_name = os.path.basename(file)

        # Se filtran los que no tienen en el nombre el patrón YYYYMMDD.
        result = re.search(DATE_FORMAT, file_name)
        if not result:
            return None

        # Se obtienen el año, mes y día.
        year, month, day = result.group(1), result.group(2), result.group(3)

        # Se verifica que son int.
        try:
            year, month, day = int(year), int(month), int(day)
        except TypeError:  # Solo salta si la fecha no se puede convertir.
            return None

        # Se verifica que la fecha sea real
        try:
            datetime.date(year, month, day)
            return year, month, day
        except ValueError:  # Solo salta si la fecha no válida
            return None
