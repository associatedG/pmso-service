from .json_reader import read_file


def get_all_roles_names():
    """
    Get all names of roles
    """
    roles_config_file = "config/roles_config.json"
    roles = read_file(roles_config_file)
    return roles["name"]
