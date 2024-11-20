import sys
from pathlib import Path

class AutoImporter:
    def __init__(self, base_dir=None):
        """
        Inicializa la clase AutoImporter.
        - base_dir: Directorio base para buscar subdirectorios. Si no se especifica, se usa el directorio actual.
        """
        # Determina el directorio base
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.add_to_sys_path()

    def add_to_sys_path(self):
        """
        Añade recursivamente todos los subdirectorios del base_dir a sys.path.
        """
        # Recorre todos los subdirectorios del directorio base
        for subdir in self.base_dir.rglob('*'):
            if subdir.is_dir():
                # Añade el subdirectorio a sys.path si no está ya presente
                if str(subdir) not in sys.path:
                    sys.path.append(str(subdir))
