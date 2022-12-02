
from twisted.spread import pb

class Two(pb.Referenceable):

    def remote_three(self, arg):
        """Appelé par le callback three sur le client

        obj2.callRemote("three", 12)

        """
        print("Two.three was given", arg)

class One(pb.Root):
    def remote_getTwo(self):
        """Appelé par le callback getTwo sur le client

        def2 = obj1.callRemote("getTwo")

        """
        two = Two()
        print("returning a Two called", two)
        return two

from twisted.internet import reactor
reactor.listenTCP(8800, pb.PBServerFactory(One()))
reactor.run()
