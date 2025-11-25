class ProfileType(object):
    """Object representando diferentes tipos de Perfis de Usuários.

    Atributos:
        - ADMIN (int): Administrador, usuário com permissões de Administrador.
        - DEVELOPER (int): Desenvolvedor, usuário com permissões de Desenvolvedor.
        - CRM_USER (int): Usuário do CRM, usuário com permissões de Usuário do CRM.
    """

    ADMIN = 1
    DEVELOPER = 2
    CRM_USER = 3

    PROFILE_TYPE_CHOICES = (
        (ADMIN, "Administrador"),
        (DEVELOPER, "Desenvolvedor"),
        (CRM_USER, "Usuário do CRM"),
    )


class Status(object):
    """Object representando diferentes status de objetos.

    Atributos:
        - ACTIVE (int): Ativo, objeto ativo.
        - INACTIVE (int): Inativo, objeto inativo.
    """

    ACTIVE = 1
    INACTIVE = 2

    STATUS_CHOICES = (
        (ACTIVE, "Ativo"),
        (INACTIVE, "Inativo"),
    )
