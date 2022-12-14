

from twisted.spread import pb
from twisted.internet import reactor

def main():
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)
    def1 = factory.getRootObject()
    def1.addCallbacks(got_obj1)
    reactor.run()

def got_obj1(obj1):
    print("got first object:", obj1)
    print("asking it to getTwo")
    def2 = obj1.callRemote("getTwo")
    def2.addCallbacks(got_obj2)

def got_obj2(obj2):
    print("got second object:", obj2)
    print("telling it to do three(12)")
    obj2.callRemote("three", 12)

main()
