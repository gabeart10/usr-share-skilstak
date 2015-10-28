"""This is an emulator for the gpio pins in rasp-pi that uses ascii art!"""

pins_set = []
pins_plugedin = []
pins_info = {}


def setup(pin, in_or_out):
    if 'out' in in_or_out or 'in' in in_or_out:
        pins_info[pin] = in_or_out
    elif not pin:
        print('''
        ERROR
        No pin found.
        ''')
        exit()
    else:
        print('''
        ERROR
        Has to be 'in' or 'out'
        ''')
        exit()

def check(pin, in_or_out):
    if pin not in pins_info:
        print('''
        ERROR
        Pin ''' + str(pin) + ''' was not made.
        ''')
        exit()
    elif pins_info[pin] != in_or_out:
        print('''
        ERROR
        Pin ''' + str(pin) + ' was not made a ' + in_or_out + ".")

def make_board
if __name__ in '__main__':
    setup(12,'in')
    print(pins_info)
    check(12,'out')
