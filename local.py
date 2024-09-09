#!/usr/bin/env python3
from chattymarkov import ChattyMarkov
import time
bob = ChattyMarkov("json://./brain.json")
alice = ChattyMarkov("json://./brain.json")
delay = 0.25
while True:
    bobPhrase = bob.generate()
    print("Bob: " + bobPhrase)
    time.sleep(delay)
    alice.learn(bobPhrase)
    alicePhrase = alice.generate()
    print("Alice: " + alicePhrase)
    time.sleep(delay)
    bob.learn(alicePhrase)
