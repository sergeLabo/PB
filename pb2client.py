
"""
Accès aux objets du serveur depuis le client
Cet exemple montre que c'est bien les mêmes, mais les univers parallèles créent
un peu de trouble.

Ce client accède à:
    - remote_getObject avec callRemote sur "getObject"
    - remote_checkObject avec callRemote sur "checkObject"
du serveur.
"""

from twisted.internet import reactor
from twisted.spread import pb

def main():
    foo = Foo()
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)
    factory.getRootObject().addCallback(foo.step1)
    reactor.run()

class Foo:
    """Permet de créer l'objet principal client qui tourne"""

    def __init__(self):
        """self.root_obj_client sera l'objet principal du serveur root_obj"""
        self.root_obj_client = None

    def step1(self, obj):
        print(f"step1: got client_accessible object from server = {obj}")
        self.root_obj_client = obj
        print("Appel de getObject sur le serveur et ajout du callback")
        self.root_obj_client.callRemote("getObject").addCallback(self.step2)

    def step2(self, client_accessible):
        print(f"Got object from server: {client_accessible}")
        print(f"Giving it back to server: {self.root_obj_client}")
        self.root_obj_client.callRemote("checkObject", client_accessible)

main()
