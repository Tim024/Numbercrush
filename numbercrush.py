from controller import Controller
from model import *
from view import *

if __name__ == '__main__':
    v = basicView()
    m = Trois()
    c = Controller(m,v)
    c.run()