"""
Accès aux objets de ce serveur depuis le client.
Cet exemple montre que c'est bien les mêmes, mais les univers parallèles créent
un peu de trouble.

Le client vient accéder ici client_accessible = ObjetAccessibleParLeClient()

Le client appelle
    - remote_getTwo avec self.oneRef.callRemote("getTwo").addCallback(self.step2)
    - remote_checkTwo avec self.oneRef.callRemote("checkTwo", two)

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
        """Méthode appelée par "getTwo" chez le client avec
        self.oneRef.callRemote("getTwo").addCallback(self.step2)
        """
        print(f"One.getTwo(), returning my client_accessible called", self.client_accessible)
        return self.client_accessible

    def remote_checkObject(self, new_client_accessible):  # ancien remote_checkTwo
        """Méthode appelée par "checkTwo" chez le client
        self.oneRef.callRemote("checkTwo", client_accessible)
        """
        print(f"My client_accessible is: {self.client_accessible}")
        print(f"Le client_accessible is: {new_client_accessible}")
        if self.client_accessible == new_client_accessible:
            print("client_accessible are the same")

# un object auquel le client pourra accéder
client_accessible = ObjetAccessibleParLeClient()

# L'objet principal réseau qui tourne
root_obj = ObjetPrincipal(client_accessible)

reactor.listenTCP(8800, pb.PBServerFactory(root_obj))
reactor.run()
