"""This is an emulator for the gpio pins in rasp-pi that uses ascii art!"""
pins_info = {}
ppin_info = {'ppin_status12': 1}

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

def output(pin, on_off):
    check(pin, 'out')
    if on_off == 'on' or on_off == 'off' or on_off == 1 or on_off == 0:
        pins_info[str(pin) + '_on_off'] = on_off
    else:
        print('''
        ERROR
        Not vaild On Off agument try: 'on', 'off', 1, 0
        ''')
        exit()

def input(pin):
    check(pin, 'in')
    if ppin_info['ppin_status' + str(pin)] == 1:
        return True
    else:
        return False

if __name__ in '__main__':
    setup(12,'in')
    check(12,'in')
    #output(12,'on')
    if input(12):
        print("On")
    else:
        print("off")
    print(pins_info)

