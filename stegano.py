import sys
import binascii
import re


def e1():
    cover = [line.rstrip('\n').rstrip() for line in open('cover.html')]

    i = 0
    watermark = []
    for elem in cover:
        if i < len(mess_bit):
            if int(mess_bit[i]) == 0:
                watermark.append(elem)
            elif int(mess_bit[i]) == 1:
                watermark.append(elem + ' ')

            i += 1
        else:
            watermark.append(elem)

    with open('watermark.html', 'w') as file:
        for elem in watermark:
            file.write(elem + '\n')


def d1():
    watermark = [line.rstrip('\n') for line in open('watermark.html')]
    detect = []
    for elem in watermark:
        if len(elem) > 0:
            if elem[-1:] == ' ':
                detect.append(1)
            else:
                detect.append(0)
        else:
            detect.append(0)

    detect_str = "".join(list(map(str, detect)))
    split_detect = ['0b' + detect_str[i:i + 8] for i in range(0, len(detect_str), 8)]
    ascii_detect = []
    for x in split_detect:
        if len(x) == 10 and x != '0b00000000':
            n = int(x, 2)
            ascii_detect.append(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())

    with open('detect.txt', 'w') as file:
        file.write("".join(ascii_detect))


def e2():
    cover = [line.rstrip('\n') for line in open('cover.html')]
    watermark = []

    i = 0
    for x in cover:
        tag_open = False
        tag_close = False
        line = ""
        line_format = ""

        for c in x:
            if c == '<':
                tag_open = True
            elif c == '>':
                tag_close = True

            if not tag_open and not tag_close:
                line += c
            elif tag_open and not tag_close:
                line_format += c
            elif tag_open:
                line_format += c
                tag_open = False
                tag_close = False

                line_format = re.sub(' +', ' ', line_format)

                # hide mess
                mess_hide = ''
                for q in line_format:
                    if q == ' ':
                        if i < len(mess_bit):
                            if int(mess_bit[i]) == 0:
                                mess_hide += q
                            elif int(mess_bit[i]) == 1:
                                mess_hide += '  '

                            i += 1
                        else:
                            mess_hide += q
                    else:
                        mess_hide += q

                line += mess_hide

        watermark.append(line)

    with open('watermark.html', 'w') as file:
        for elem in watermark:
            file.write(elem + '\n')


def d2():
    watermark = [line.rstrip('\n') for line in open('watermark.html')]
    detect = []

    for elem in watermark:
        tag_open = False
        tag_close = False
        space = False

        for i in range(0, len(elem)):
            c = elem[i:i + 1]
            if c == '<':
                tag_open = True
            elif c == '>':
                tag_close = True

            if tag_open:
                if c == ' ' and not space:
                    c = elem[i + 1:i + 2]
                    if c == ' ':
                        detect.append(1)
                        space = True
                    else:
                        detect.append(0)
                        space = False
                elif space:
                    space = False

            if tag_close:
                tag_open = False
                tag_close = False

    detect_str = "".join(list(map(str, detect)))
    split_detect = ['0b' + detect_str[i:i + 8] for i in range(0, len(detect_str), 8)]
    ascii_detect = []
    for x in split_detect:
        if len(x) == 10 and x != '0b00000000':
            n = int(x, 2)
            ascii_detect.append(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())

    with open('detect.txt', 'w') as file:
        file.write("".join(ascii_detect))


def e3():
    cover = [line.rstrip('\n') for line in open('cover.html')]
    watermark = []

    i = 0
    for x in cover:
        tag_open = False
        p = False
        line = ""

        for c in x:
            if c == '<':
                tag_open = True
            elif c == 'p':
                p = True
            elif c == '>' and tag_open and p:
                if i < len(mess_bit):
                    if int(mess_bit[i]) == 0:
                        line += ' style="margin-botom: 0cm;" '
                    elif int(mess_bit[i]) == 1:
                        line += ' style="lineheight: 0cm;" '

                    i += 1
                    tag_open = False
                    p = False
            else:
                tag_open = False
                p = False

            line += c

        watermark.append(line)

    with open('watermark.html', 'w') as file:
        for elem in watermark:
            file.write(elem + '\n')


def d3():
    watermark = [line.rstrip('\n') for line in open('watermark.html')]
    detect = []

    for elem in watermark:
        elem_split = elem.split('<p')
        for x in elem_split:
            if 'style="margin-botom: 0cm;"' in x:
                detect.append(0)
            elif 'style="lineheight: 0cm;"' in x:
                detect.append(1)

    detect_str = "".join(list(map(str, detect)))
    split_detect = ['0b' + detect_str[i:i + 8] for i in range(0, len(detect_str), 8)]
    ascii_detect = []
    for x in split_detect:
        if len(x) == 10 and x != '0b00000000':
            n = int(x, 2)
            ascii_detect.append(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())

    with open('detect.txt', 'w') as file:
        file.write("".join(ascii_detect))


def e4():
    cover = [line.rstrip('\n') for line in open('cover.html')]
    watermark = []

    i = 0
    for x in cover:
        line = ""
        x_format = x

        if i < len(mess_bit):
            p_open = x_format.find('<p>')
            p_close = x_format.find('</p>')

            while p_open != -1 and p_close != -1:
                if i < len(mess_bit):
                    if int(mess_bit[i]) == 0 and p_close < p_open:
                        line += '</p><p></p>'
                        i += 1
                    elif int(mess_bit[i]) == 1 and p_open < p_close:
                        line += '<p></p><p>'
                        i += 1

                    if p_close < p_open:
                        x_format = x[p_close + 4:]
                    elif p_open < p_close:
                        x_format = x[p_open + 3:]

                    p_open = x_format.find('<p>')
                    p_close = x_format.find('</p>')
        else:
            line = x

        print(line)

    watermark.append(line)
    with open('watermark.html', 'w') as file:
        for elem in watermark:
            file.write(elem + '\n')


if __name__ == '__main__':
    with open('mess.txt', 'r') as f:
        mess = f.read().split(' ')

    mess_bit = "".join([bin(int(v, 16))[2:].zfill(8) for v in mess])

    if sys.argv[1] == '-e':
        if sys.argv[2] == '-1':
            e1()
        elif sys.argv[2] == '-2':
            e2()
        elif sys.argv[2] == '-3':
            e3()
        elif sys.argv[2] == '-4':
            e4()
    elif sys.argv[1] == '-d':
        if sys.argv[2] == '-1':
            d1()
        elif sys.argv[2] == '-2':
            d2()
        elif sys.argv[2] == '-3':
            d3()

    print("Done for args: {} {}".format(sys.argv[1], sys.argv[2]))
