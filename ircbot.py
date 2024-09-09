#!/usr/bin/env python3
# this is an IRC ready version of the markov bot.
# using example code found on the internet to create a minimal IRC bot
# and chattymarkov
import socket
import random
import time
from chattymarkov import ChattyMarkov 
markov = ChattyMarkov("json://./brain.json") 
antispam = 3.5
chanceToSpeak = 1
class IRCBot:
    def __init__(self, **kwargs):
        self.settings = {
	# SET YOUR BOT UP HERE
            'host':"irc.prison.net",
            'port':6667,
            'channel':"#bongspam",
            'contact': ":",
            'nick':"BobSpack",
            'ident':'fpoo',
            'realname':'farty poo'
	# END OF SETTINGS
        }
        self.add_kwargs(kwargs)
        self.sock = self.irc_conn()
        self.main_loop()
    def add_kwargs(self, kwargs):
        '''
        add keyword args as class attributes. This allows you to change the settings based on 
        dict arg, and not have to hard code it in. The settings keys become this class' attributes. 
        And the value becomes the value for those attributes. 
        AKA
        self.nick = "mybot"  etc.
         
        IRCbot(**{nick:"mybot2"})
        IRCbot(**{nick:"mybot3"})
        '''
        for kwarg in kwargs:
            if kwarg in self.settings:
                self.settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(self.settings)
         
    def irc_conn(self):
        '''
        connect to server/port channel, send nick/user 
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('connecting to "{0}/{1}"'.format(self.host, self.port))
        sock.connect((self.host, self.port))
        print('sending NICK "{}"'.format(self.nick))
        sock.send("NICK {0}\r\n".format(self.nick).encode())
        sock.send("USER {0} {0} bla :{0}\r\n".format(
            self.ident,self.host, self.realname).encode())
        print('joining {}'.format(self.channel))
        sock.send(str.encode('JOIN '+self.channel+'\n'))
        self.joined = True
        return sock
         
    def main_loop(self):
        '''
        The main loop to keep the program running and waiting for commands
        '''
        while True:
            self.parse_data()   #read in data from irc
            self.ping_pong()    #check for PING from network
            self.markov_reply() #learn/reply with markov chain
#            self.random_outburst() #chance to have a random outburst of stupid
    def get_user(self, stringer):
        '''get username from data string'''
        start = stringer.find('~')
        end = stringer.find('@')
        user = stringer[start +1:end]
        return user

    def parse_data(self):
        '''
        get server data and parse it based on each message/command in irc
        '''
        data=self.sock.recv(1042) #recieve server messages
        data = data.decode('utf-8') #data decoded
        self.data = data.strip('\n\r') #data stripped
        try:
            self.operation = data.split()[1] #get operation ie. JOIN/QUIT/PART/etc.
            textlist = data.split()[3:]
            text = ' '.join(textlist)
            self.text = text[1:] #content of each message
            self.addrname = self.get_user(data) #get address name
            self.username = data[:data.find('!')][1:] #get username
            print(str(self.username) + ": " + str(self.text))
            self.cmd = self.text.split()[0][1:]
        except IndexError: #startup data has different layout than normal
            pass
             
    def markov_reply(self):
        if len(self.username) <= 16 and not "NAMES" in self.text and self.nick in self.text:
            response = str(self.username) + ": " + str(markov.generate())
            self.say(response)
        if len(self.username) <= 16 and not "NAMES" in self.text and random.randint(0,100) <= chanceToSpeak:
            cleanedText = str(self.text).replace(str(self.nick),'')
            cleanedText = cleanedText.replace(':','')
            if 'PRIVMSG' in cleanedText:
                return
            markov.learn(cleanedText)
            print("learned : " + cleanedText)
            response = str(markov.generate())
            print("said: " + response)
#            print("typing for " + str(len(string)*antispam))
#            time.sleep(len(string)*antispam)
            time.sleep(antispam)
            self.say(response)
#            if random.randint(0,30) == 19:
#                response = str(markov.generate())
#                print("said : " + response)
#                self.say(response)
    def ping_pong(self):
        '''
        The server pings and anything that does not pong back gets kicked
        '''

        try:
            if self.data[:4] == 'PING':
                print(self.data)
                self.send_operation('PONG')
                print("PONG")
                if random.randint(0,500) <= chanceToSpeak:
                    outburst = str(markov.generate())
                    print("outburst: " + outburst)
                    self.say(outburst)
        except TypeError: #startup data
            pass
             
    def send_operation(self, operation=None, msg=None, username=None):
        '''
        the specific string structure of sending an operation and private message to one user
        '''
        if msg is None:
            #send ping pong operation
            self.sock.send('{0} {1}\r\n'.format(operation, self.channel).encode())
        elif msg != None:
            #send private msg to one username
            self.sock.send('PRIVMSG {0} :{1}\r\n'.format(self.username,msg).encode())
             
    def say(self, string):
        '''
        send string to channel...the equivalent to print() in the IRC channel
        '''
        self.sock.send('PRIVMSG {0} :{1}\r\n'.format(self.channel, string).encode())
         

bot = IRCBot()
