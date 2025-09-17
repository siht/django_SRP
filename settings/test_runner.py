# settings/test_runner.py
import doctest
import os
import unittest
from django.test.runner import DiscoverRunner
from django.apps import apps
import importlib

class UnifiedTestRunner(DiscoverRunner):
    """
    Un test runner que ejecuta tanto los tests de Django como los doctests,
    descubriendo automáticamente los módulos de doctests.
    """

    def get_doctest_modules(self):
        """
        Descubre automáticamente los módulos de doctest
        escaneando el sistema de archivos del proyecto.
        """
        modules = []
        project_root = os.getcwd() # Obtiene la raíz del proyecto
        excluded_dirs = ['env', '.venv', 'venv', '__pycache__']

        for dirpath, dirnames, filenames in os.walk(project_root):
            # Excluye directorios no deseados
            dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
            
            for filename in filenames:
                if filename.endswith('.py'):
                    # Construye la ruta del archivo
                    file_path = os.path.join(dirpath, filename)
                    
                    # Convierte la ruta de archivo en un nombre de módulo
                    module_name = os.path.splitext(os.path.relpath(file_path, project_root))[0]
                    module_name = module_name.replace(os.sep, '.')
                    
                    try:
                        if not module_name.startswith('.'): # Evita módulos sin nombre de paquete
                            module = importlib.import_module(module_name)
                            modules.append(module)
                    except (ImportError, ModuleNotFoundError) as e:
                        print(f"No se pudo importar el módulo {module_name}: {e}")
                        continue
        return modules

    def run_suite(self, suite):
        # Primero, ejecuta la suite de tests de Django (unittest)
        super_result = super().run_suite(suite)

        # Ahora, ejecuta los doctests
        print("\nRunning doctests...")
        doctest_runner = unittest.TextTestRunner(verbosity=self.verbosity)
        doctest_suite = unittest.TestSuite()

        # Agrega los tests de los módulos descubiertos
        for module in self.get_doctest_modules():
            doctest_suite.addTest(doctest.DocTestSuite(module))

        doctest_result = doctest_runner.run(doctest_suite)
        return super_result