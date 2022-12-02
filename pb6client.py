
from time import sleep
from threading import Thread

import numpy as np
import cv2

from twisted.internet import reactor
from twisted.spread import pb


class GetImage(pb.Copyable):
    def test(self, truc):
        print("toto", truc)

    def get_image(self, img):
        print(img)

class RemoteGetImage(pb.RemoteCopy):
    pass

pb.setUnjellyableForClass(GetImage, RemoteGetImage)

class Client:
    """Permet de créer l'objet principal client qui tourne"""

    def __init__(self):
        """self.root_obj_client sera l'objet principal du serveur root_obj"""
        self.root_obj_client = None
        self.gi = GetImage()

    def on_start(self, obj):
        print(f"on_start: got client_accessible object from server = {obj}")
        self.root_obj_client = obj

        # Transfert d'une image
        self.root_obj_client.callRemote("image").addCallback(self.gi.test)



def main():
    clt = Client()
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)
    factory.getRootObject().addCallback(clt.on_start)
    reactor.run()

main()
