"""
Módulo con la funcionalidad de trabajar con las carpetas.
"""

import logging
import os
from typing import List


class PyFolders:
    """
    Clase encargada de gestionar los archivos.
    """

    @staticmethod
    def list_all(folder: str) -> List[str]:
        """
        Método para listar, de forma recursiva, todos los archivos de una
        carpeta.

        :param folder: Path de la carpeta que analizar.
        :return: Lista con el path de todos los archivos.
        """

        logging.debug('Explorando carpeta "%s"', folder)

        # Se recorren todos los ficheros o directorios.
        all_files: List[str] = []
        for file_or_dir in os.listdir(folder):

            # Se crea al path completo.
            full_path = os.path.join(folder, file_or_dir)

            # Si es un archivo, se añade a la lista.
            if os.path.isfile(full_path):
                all_files.append(full_path)
                logging.debug('Añadido archivo "%s"', full_path)

            # Si es una carpeta se investiga.
            elif os.path.isdir(full_path):
                all_files += PyFolders.list_all(full_path)

            # Cualquier otro caso, se ignora.
            else:
                logging.info('Ignorando path: "%s"', full_path)

        return all_files
