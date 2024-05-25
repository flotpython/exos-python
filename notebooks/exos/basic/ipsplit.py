def ip_v0(ip):
    """
    Convertit une adresse IP en une liste de 4 entiers
    """
    # pour commencer on fait un split('.')
    # qui nous retourne une liste de chaines
    # et sur chacune de ces chaines on applique
    # la fonction 'int()' pour convertir en entier
    return [int(x) for x in ip.split('.')]


def ip_v1(ip):
    """
    Convertit une adresse IP en un entier sur 32 bits
    """
    # on s'appuie sur la première version
    bytes = ip_v0(ip)
    # ne reste plus quà faire un peu d'arithmétique
    result = 0
    while bytes:
        result = result * 256 + bytes.pop(0)
    return result
