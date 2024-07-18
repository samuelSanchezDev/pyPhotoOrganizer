"""
Módulo con la funcionalidad de manipular los archivos.
"""

import datetime
import logging
import pathlib
import re
from typing import List, Set, Tuple, Union
import os
import hashlib

DATE_FORMAT = r'(\d{4})(\d{2})(\d{2})'  # Mach para fechas en formato YYYYMMDD


class PyFiles:
    """
    Clase encargada de gestionar los archivos.
    """

    PICTURES: List[str] = [  # Extensiones de imagen
        '.bmp',  # BMP
        '.gif',  # GIF
        '.jpg', '.jpeg',  # JPEG
        '.png',  # PNG
        '.webp',  # WebP
        '.heic', '.heif'  # HEIF
        '.avif',  # AVIF
    ]

    VIDEOS: List[str] = [  # Extensiones de vídeo
        '.3gp',  # 3GPP
        '.mp4',  # MPEG-4
        '.mkv',  # Matroska
        '.webm',  # WebM
    ]

    @staticmethod
    def unique_digest(files: List[str]) -> List[str]:
        """
        Método para filtrar los archivos con mismo digest.

        :param files: Lista con los path de los archivos.
        :return: Lista con los path de los archivos con digest único.
        """

        logging.debug('Filtrando archivos únicos.')

        # Se filtran los path que no corresponden a archivos.
        real_files: List[str] = list(filter(os.path.isfile, files))

        # Se calcula el hash de los archivos y se ignoran aquellos duplicados.
        all_hash: Set[bytes] = set()
        unique_files: List[str] = []
        for file in real_files:
            logging.debug('Verificando hash del archivo "%s"', file)

            my_hash = hashlib.sha1()
            with open(file, 'rb') as f:
                my_hash.update(f.read())
                digest = my_hash.digest()

            if digest not in all_hash:
                logging.debug('Archivo aceptado.')
                all_hash.add(digest)
                unique_files.append(file)

        return unique_files

    @staticmethod
    def date_from_name(file: str) -> Union[Tuple[int, int, int], None]:
        """
        Método para obtener la fecha del archivo del nombre (tiene que estar
        con la forma YYYYMMDD). La función no comprueba que el archivo exista.

        :param file: path del archivo.
        :return: una tupla con el año, mes y día del archivo, o None en caso
        de que no se pueda obtener.
        """

        logging.debug('Obteniendo fecha de archivo.')

        # Se obtiene el nombre del archivo.
        file_name = os.path.basename(file)

        # Se filtran los que no tienen en el nombre el patrón YYYYMMDD.
        result = re.search(DATE_FORMAT, file_name)
        if not result:
            logging.debug('El archivo "%s" no sigue el formato YYYYMMDD.',
                          file)
            return None

        # Se obtienen el año, mes y día.
        year, month, day = result.group(1), result.group(2), result.group(3)

        # Se verifica que son int.
        try:
            year, month, day = int(year), int(month), int(day)
        except TypeError as e:  # Solo salta si la fecha no se puede convertir.
            logging.debug('No se ha podido convertir la fecha a entero.')
            logging.debug('Excepción: %s', e)
            return None

        # Se verifica que la fecha sea real
        try:
            datetime.date(year, month, day)
            return year, month, day
        except ValueError as e:  # Solo salta si la fecha no válida
            logging.debug('La fecha %04d/%04d/%04d no es válida.', year, month,
                          day)
            logging.debug('Excepción: %s', e)
            return None

    @staticmethod
    def filter_pictures(files: List[str]) -> List[str]:
        """
        Método para filtrar los archivos correspondientes a fotos (y vídeos).
        Para ello se usan las extensiones consideradas en PyFiles.PICTURES y
        PyFiles.VIDEOS.

        :param files: Lista con los archivos que filtrar.
        :return: Lista con los archivos filtrados.
        """

        logging.debug('Filtrando archivos por extensión.')

        # Función para comprobar si un archivo es una foto.
        def check_extension(file: str) -> bool:

            # Se extrae la extensión.
            extension = pathlib.Path(file).suffix.lower()

            # Se comprueba si la extensión esta en PyFiles.PICTURES o
            # PyFiles.VIDEOS
            is_valid = (extension in PyFiles.PICTURES) or \
                (extension in PyFiles.VIDEOS)

            logging.debug('Verificando si es una foto o vídeo "%s"... %s',
                          file, is_valid)
            return is_valid

        # Se filtran todos los archivos
        return list(filter(check_extension, files))
