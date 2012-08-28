import os
import subprocess
import codecs # codecs.open() handles unicode
import datetime
CURRDIR = os.getcwd() + '/'
DEFCOLOR = 'COLOR_LIGHT_BLUE'
C_N = '$none'
C_LG = '$lgreen'
C_G = '$green'
C_B = '$blue'
C_LB = '$lblue'
C_R = '$red'
C_GY = '$gray'
C_P = '$purple'
C_LP = '$lpurple'
C_Y = '$yellow'

#-------------- FORMATTING AND WRITING TO TERMINAL  -------------------------#

def pretty_string(s):
    # split camelCase, then make pretty
    lowers = [  'a', 'an', 'and', 'da', 'du', 'is', 'in', 'on', 
                'of', 'the', 'to']
    exceptions = [  ('I I I', 'III'), ('I I', 'II'), (' W ',' with '),
                    (r'^[l|L]$',"l'"), (r'[i|I]m ',"I'm "),('O ',"O'"),
                    (r'[w|W]hos ','Who\'s'),('D I A','DIA'),
                    ('N Y C','NYC'),('N Y'),('NY'),('L A', 'LA'),
                    ('freuds','freud\'s'),
                    ('T N'),('TN'),('Didnt','Didn\'t'),('Dont','Don\'t'),('Lets','Let\'s'),
                    ('Im','I\'m'),('Jaspers','Jasper\'s'),('Platos','Plato\s'),
                    ('Sambos','Sambo\'s'),]
    title = re.sub(r'([a-z]*)([A-Z])', r'\1 \2', s)
    title = re.sub(r'([a-z]+)([0-9])', r'\1 \2', title)
    for l in lowers:
        l1 = ' ' + l.capitalize() + ' '
        l2 = ' ' + l + ' '
        title = re.sub(l1,l2,title)
    for e in exceptions:
        title = re.sub(e[0],e[1],title)
    title = title[0].upper() + title[1:]
    return title


def pretty_file_name(l, artist = '', display = False):
    """Makes a human readable string from image file."""
    file_name = list_to_dotstring(l)
    if artist == '':
        artist = pretty_string(l[0])
    date = l[1]
    title = pretty_string(l[2])
    if len(l) > 4:
        sub_title = ''
        for s in l[3:-1]:
            sub_title += pretty_string(s) 
        title += ' (' + sub_title + ')'
    if display:
        s1 = s2 = ' '
        if len(artist) < 12:
            s1 += (12 - len(artist)) * ' '
        if len(date) < 8:
            s2 += (9  - len(date)) * ' '
        cprint(C_Y,artist,s1,C_B,date,s2,C_P,title)
    return artist, date, title, file_name


def color(s = ""):
    if s == '$none':
        c = '${COLOR_NC}\c'
    elif s == '$white':
        c = '${COLOR_WHITE}\c'
    elif s == '$black':
        c = '${COLOR_BLACK}\c'
    elif s == '$blue':
        c = '${COLOR_BLUE}\c'
    elif s == '$lblue':
        c = '${COLOR_LIGHT_BLUE}\c'
    elif s == '$green':
        c = '${COLOR_GREEN}\c'
    elif s == '$cyan':
        c = '${COLOR_CYAN}\c'
    elif s == '$lgreen':
        c = '${COLOR_LIGHT_GREEN}\c'
    elif s == '$lcyan':
        c = '${COLOR_LIGHT_CYAN}\c'
    elif s == '$red':
        c = '${COLOR_RED}\c'
    elif s == '$lred':
        c = '${COLOR_LIGHT_RED}\c'
    elif s == '$purple':
        c = '${COLOR_PURPLE}\c'
    elif s == '$lpurple':
        c = '${COLOR_LIGHT_PURPLE}\c'
    elif s == '$brown':
        c = '${COLOR_BROWN}\c'
    elif s == '$yellow':
        c = '${COLOR_YELLOW}\c'
    elif s == '$gray':
        c = '${COLOR_GRAY}\c'
    elif s == '$lgray':
        c = '${COLOR_LIGHT_GRAY}\c'
    else:
        c = '${' + DEFCOLOR + '}\c'
    call = 'echo "' + c + '"'
    subprocess.call(call, shell = True)


def cprint(*print_list):
    """Take a list of strings, print them to terminal in color.
    
    Send a list of strings, if strings are color keywords, terminal color
    is changed.
    """
    for s in print_list:
        s = str(s)
        if len(s) > 0 and s[0] == '$':
            color(s)
        else:
            call = 'echo "' + s + '\c"'
            subprocess.call(call, shell = True)
    color()
    print ""
    return


def cprint_list(color,l,pretty=False):
    color(color)
    for item in l:
        if pretty:
            print pretty_string(item)
        else:
            print item
    color()


def section(heading='*****'):
    cprint( '\n', C_Y,'***** ',C_B, heading.upper(), C_Y, ' *****')


def menu(d,prompt='true'): 
    """Take a dictionary, and turns it into a menu"""  
    keys = []
    try:
        title = d.pop('TITLE')
        section(title)
    except KeyError:
        section()
    sorted_d = sorted(d.items())
    for key in sorted_d:
        row = [C_LB,'  {0:10}'.format(key[0]),' : ',C_LG,'{}\n'.format(key[1])]
        keys.extend(row)
    cprint(*keys)
    if prompt:
        return raw_input('Enter Selection: ')


#-------------- WRITING TO FILE  --------------------------------------------#

def write_list(l,f):
    """Writes list l, one item per line, to file f."""
    count = 0
    for item in l:
        try:
            f.write(item)
        except UnicodeDecodeError:
            cprint(C_R, 'error on {}'.format(item))
        f.write('\n')
        count += 1
    return count


def write_dict(l,f):
    count = 0
    for k, v in sorted(l.items()):
        item = k + ', ' + v
        f.write(item)
        f.write('\n')
        count += 1
    return count


def write_to_file(l,file_name,title,o_type='list', mode='w'):
    """Save a list to a file"""
    file_path = CURRDIR + file_name
    cprint(C_G, "file saving mode: ", mode)
    f = codecs.open(file_path, encoding='utf-8', mode=mode)
    count = 0
    now = str(datetime.datetime.now())
    now_stamp = '##### Generated: ' + now + '\n\n'
    hash_title = '# ' + title
    f.write(hash_title)
    f.write('\n')
    f.write(now_stamp)
    if o_type == 'list':
        count = write_list(l,f)
    elif o_type == 'dict':
        count = write_dict(l,f)
    end_title = """
##### end generated log
##### total items = """ + str(count) + '\n\n'
    f.write(end_title)
    f.close()
    cprint (C_G, 'Saved ', C_P, title, C_G, ' to file ', C_LG, file_path)
    return
