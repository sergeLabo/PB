
from time import sleep
from threading import Thread

import numpy as np
import cv2

from twisted.internet import reactor
from twisted.spread import pb



class MyImage:

    def __init__(self):
        self.img = cv2.imread('./covers/Fasokan.jpg')
        self.numpydata = np.asarray(self.img)
        self.data = 12



class ObjetPrincipal(pb.Root):
    def __init__(self):
        self.mi = MyImage()

    def remote_image(self):
        print("Le serveur envoie une image")
        return self.mi.numpydata
        # # return {"toto": [0,1,"toto"]}


# L'objet principal réseau qui tourne
root_obj = ObjetPrincipal()

reactor.listenTCP(8800, pb.PBServerFactory(root_obj))
reactor.run()
