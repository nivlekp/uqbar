import enum
import importlib
import inspect


class ClassDocumenter:

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### INITIALIZER ###

    def __init__(self, package_path):
        module_path, _, client_name = package_path.rpartition(':')
        module = importlib.import_module(module_path)
        client = getattr(module, client_name)
        if not self.validate_client(client, module_path):
            message = 'Expected type, got {}'.format(type(client))
            raise ValueError(message)
        self._client = client
        self._package_path = package_path.replace(':', '.')

    ### SPECIAL METHODS ###

    def __str__(self):
        return '\n'.join([
            '.. autoclass:: {}'.format(
                self.client.__name__,
                ),
            '   :members:',
            '   :undoc-members:',
            '   :show-inheritance:',
            ])

    ### PUBLIC METHODS ###

    @classmethod
    def validate_client(cls, client, module_path):
        return (
            isinstance(client, type) and
            client.__module__ == module_path
            )

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def documentation_section(self):
        if hasattr(self.client, '__documentation_section__'):
            return self.client.__documentation_section__
        elif inspect.isabstract(self.client):
            return 'Abstract Classes'
        elif issubclass(self.client, enum.Enum):
            return 'Enumerations'
        elif issubclass(self.client, Exception):
            return 'Exceptions'
        return 'Classes'

    @property
    def package_path(self):
        return self._package_path
