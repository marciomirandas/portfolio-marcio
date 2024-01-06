from rolepermissions.roles import AbstractUserRole

class Vendedor(AbstractUserRole):
    available_permissions = {
        'administrativo': True,
        'ver_materia': True,
    }

class Comprador(AbstractUserRole):
    available_permissions = {
        'ver_materia': True,
    }