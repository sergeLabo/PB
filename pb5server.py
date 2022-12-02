
"""
Idem exemple 5 avec en plus transfert de
    -json
    - images
    - str
"""

from time import sleep
from threading import Thread

from twisted.internet import reactor
from twisted.spread import pb

class PlayerSimulator(pb.Referenceable):
    """Cette class permet de créer un objet à partager.
    Il simule un player avec:
        - une position de lecture du fichier musical à self.position
        - un track à lire imposé par le client
    L'objet accessible par le client est player
    """
    def __init__(self):
        self.track = 1
        self.position = 0
        Thread(target=self.thread_update_position).start()

    def thread_update_position(self):
        n = 0
        while n < 1000:
            n += 1
            self.position += 1
            sleep(1)

    def remote_newTrack(self, track):
        """New Track imposé par le client"""
        self.track = track
        print(f"Nouveau track demandé par le client {self.track}")

class ObjetPrincipal(pb.Root):
    def __init__(self, player):
        self.player = player

    def remote_getPlayerSimulator(self):
        print(f"Le client  demande self.player, je lui retourne")
        return self.player

    def remote_getPosition(self):
        p = self.player.position
        print(f"Le serveur envoie au client la position {p}")
        return p

# un object auquel le client pourra accéder
player = PlayerSimulator()

# L'objet principal réseau qui tourne
root_obj = ObjetPrincipal(player)

reactor.listenTCP(8800, pb.PBServerFactory(root_obj))
reactor.run()
