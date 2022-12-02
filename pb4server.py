"""
Serveur:
    Echange bidirectionnel serveur client
"""

from twisted.internet import reactor
from twisted.spread import pb


class ObjetAccessibleParLeClient(pb.Referenceable):
    """Cette class permet de créer un objet pour en avoir un à partager,
    mais il ne fait rien dans cet exemple
    L'objet accessible par le client est client_accessible
    """
    pass

class ObjetPrincipal(pb.Root):
    def __init__(self, client_accessible):
        self.client_accessible = client_accessible

    def remote_getObject(self):  # ancien remote_getTwo
        """Méthode appelée par "getObject" chez le client avec
            self.oneRef.callRemote("getObject").addCallback(self.step2)
        """
        print(f"Le client a reçu: {self.client_accessible}")
        return self.client_accessible

    def remote_checkObject(self, new_client_accessible):  # ancien remote_checkTwo
        """Méthode appelée par "checkTwo" chez le client
        self.oneRef.callRemote("checkTwo", client_accessible)
        """
        print(f"Mon client_accessible est: {self.client_accessible}")
        print(f"Le client_accessible est:  {new_client_accessible}")
        if self.client_accessible == new_client_accessible:
            print("Les client_accessible sont les mêmes")

    def remote_takeTwo(self, two):
        """takeTwo"""
        print(f"Le serveur à reçu du client un Two: {two}")
        print("Le serveur demande au client: print(12)")
        two.callRemote("print", 12)

# un object auquel le client pourra accéder
client_accessible = ObjetAccessibleParLeClient()

# L'objet principal réseau qui tourne
root_obj = ObjetPrincipal(client_accessible)

reactor.listenTCP(8800, pb.PBServerFactory(root_obj))
reactor.run()
