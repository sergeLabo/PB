"""
Client:
    Echange bidirectionnel serveur client
"""

from twisted.internet import reactor
from twisted.spread import pb

class Two(pb.Referenceable):
    def remote_print(self, arg):
        print(f"Two.print() appelé par le serveur avec l'argument: {arg}")
        print(arg)

class Foo:
    """Permet de créer l'objet principal client qui tourne"""

    def __init__(self):
        """self.root_obj_client sera l'objet principal du serveur root_obj"""
        self.root_obj_client = None

    def step1(self, obj):
        self.root_obj_client = obj
        obj_server = self.root_obj_client.callRemote("getObject")
        print(f"Le client a accès à: {obj_server}")
        obj_server.addCallback(self.step2)

    def step2(self, client_accessible):
        print(f"Got object from server: {client_accessible}")
        print(f"Giving it back to server: {self.root_obj_client}")
        self.root_obj_client.callRemote("checkObject", client_accessible)

def got_obj(obj, two):
    print("J'ai eu l'objet:", obj)
    print(f"Je lui donne le mien {two}")
    obj.callRemote("takeTwo", two)

def main():
    foo = Foo()
    two = Two()
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)
    factory.getRootObject().addCallback(foo.step1)
    def1 = factory.getRootObject()
    def1.addCallback(got_obj, two)  # hands our 'two' to the callback
    reactor.run()

main()
