import npyscreen
from telnetlib import Telnet

class Vars():
    #a solution to getting vars from screen to screen.
    def __init__(self, addy = '127.0.0.1', port = '2010', user = 'User', passw = 'passwd'):
        self.addy      = addy
        self.port      = port
        self.user      = user
        self.passw     = passw
        self.buffer    = None
        self.selection = None


class MyTestApp(npyscreen.NPSAppManaged):

    def onStart(self):
        self.registerForm("MAIN", LoginForm()) #starting form for all managed.
        self.registerForm('gamewarn', GameWarn())
        self.registerForm('GameMenu', GameMenu())
# This form class defines the display that will be presented to the user.
class GameMenu(npyscreen.Form):
    def create(self):
        self.selected = self.add(npyscreen.TitleSelectOne, max_height=4, value=[1, ], name="Choose your own bog:",
                   values=['Newbie Loop', 'Eternal Vacuum'], scroll_exit=True)


    def afterEditing(self):
        var.selection = self.selected.value
        self.parentApp.setNextForm(None)


class GameWarn(npyscreen.Form):

    #todo change to a license agreement lol
    def create(self):
        self.add(npyscreen.FixedText, value = 'Use at your own risk.')
        self.add(npyscreen.FixedText, value = 'More stuff here later.')

    def afterEditing(self):
        self.parentApp.setNextForm('GameMenu')

class LoginForm(npyscreen.Form):

    def create(self):
        self.add(npyscreen.TitleFixedText, name = 'Bogleg Bot', color = 'RED')
        self.addy = self.add(npyscreen.TitleText, color = 'LABEL', name = 'Address:', value = '127.0.0.1')
        self.port  = self.add(npyscreen.TitleText, name = 'Port:', value = '2010')
        self.user  = self.add(npyscreen.TitleText, name = "Username:" )
        self.passw = self.add(npyscreen.TitlePassword, name = 'Password:')


    def afterEditing(self):
        self.parentApp.setNextForm('gamewarn')

        var.port  = self.port.value
        var.addy  = self.addy.value
        var.user  = str(self.user.value)
        var.passw = str(self.passw.value)


class PlayerBody():
    '''
    This class tracks player info.
    '''
    def __init__(self):
        self.name = var.user
        self.exits = None

    def get_name(self):
        return self.name


#functions

#negotiate password
def login(telnetOb:Telnet):
    newL = '\n'.encode('ascii')
    telnetOb.open(var.addy, var.port)
    telnetOb.read_until(b'Login')
    telnetOb.write(var.user.encode('ascii')+newL)
    telnetOb.read_until(b'Password')
    telnetOb.write(var.passw.encode('ascii')+newL)

#get exits, handles contact default formatting
def getExits(tnOB:Telnet):
    sorting = True
    exitLine = ''
    while sorting:
        line = tnOB.read_until(b'\n')
        if b'<' in line:
            print(line)
            exitLine = line
            sorting = False

    exitLine = exitLine.decode()
    exits = []

    for i in list(set(exitLine)):
        if i.isalpha():
            exits.append(i)
    pb.exits = exits
    print(exits)
    return exits

def goToNewbie(tnOb:Telnet):
    dirs = ['d', 'w', 's', 'read book', 'n', 'n', 'n', 'n' ]
    for i in dirs:
        tnOb.write(i.encode('utf-8')+b'\n')


if __name__ == "__main__":
    var = Vars()
    tn  = Telnet()
    tn.open(var.addy, var.port)
    App = MyTestApp()
    App.run()
    pb = PlayerBody()
    login(tn)
    getExits(tn)
    goToNewbie(tn)


