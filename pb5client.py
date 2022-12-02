
from time import sleep
from threading import Thread

from twisted.internet import reactor
# Interaction réseau en TCP
from twisted.spread import pb  # Perspetive Broker de Twisted

class Client:
    """Permet de créer l'objet principal client qui tourne"""

    def __init__(self):
        """self.root_obj_client sera l'objet principal du serveur root_obj"""
        self.root_obj_client = None
        self.track = 1

    def on_start(self, obj):
        print(f"on_start: got client_accessible object from server = {obj}")
        self.root_obj_client = obj
        # Appel du Player sur le serveur et ajout du callback
        self.root_obj_client.callRemote("getPlayerSimulator").addCallback(self.run)

    def run(self, args):
        Thread(target=self.thread_run).start()

    def thread_run(self):
        n = 0
        while n < 500:
            # Position
            n += 1
            self.root_obj_client.callRemote("getPosition").addCallback(self.print_position)

            # Changement de track tous les 10
            if n % 10 == 2:
                self.track += 1
                self.root_obj_client.callRemote("getPlayerSimulator").addCallback(self.toto)
            sleep(0.3)

    def toto(self, args):
        print("args:", args)
        print(f"Envoi du track: {self.track}")
        args.callRemote("newTrack", self.track)


    def print_position(self, position):
        print(f"Le client a reçu: {position}")


def main():
    clt = Client()
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)
    factory.getRootObject().addCallback(clt.on_start)
    reactor.run()

main()
