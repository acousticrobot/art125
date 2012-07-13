#!/usr/bin/env python

# Name: Image Indexer
# Author: Jonathan Gabel
# version: 0.8
# (c) GPL 2012
# URL: http://jonathangabel.com
# Image Indexer is a command line utility to deal with artist image repositories.
# It works with images named with the following naming convention:
# artist.date.Title.Subtitle.jpg
# It expects a file in the directory named __whos_who.txt with the following dictionary
# format, one artists per line:
# artist : FirstName LastName

import os
import re
import codecs # codecs.open() handles unicode
from unidecode import unidecode
from termate import pretty_string, pretty_file_name, color, cprint, trm_sect, menu
from filemate import write_list, write_dict, write_to_file, write_titles, change_dir, nav_dir
from filemate import load_directory_as_list, compare_directories, load_file_as_dict
from filemate import add_file_to_list, load_images_as_lists, list_to_dotstring



CURRDIR = os.getcwd() + '/'


#-------------- LOADING FROM FILES AND DIRECTORY ----------------------------#
# :--------- Indexer Specific: ---------------------:

def load_artists_in_dir():
    """Return list of artist from current directory
    
    no titles or dates retained"""
    image_list = load_images_as_lists()
    artists = []
    for i in image_list:
        if i[0] not in artists:
            artists.append(i[0])
    return artists


def find(args,split=True):
    images = load_images_as_lists()
    srch, pos, typ, search_all = [], 2, 'intersection', False
    args = re.split(r' ',args)
    for arg in args:
        if arg == '-u':
            typ = 'union'
        elif arg == '-i':
            typ = 'intersection'
        elif arg == '-a':
            pos = 0
        elif arg == '-t':
            pos = 2
        elif arg == '-e':
            search_all = True
        elif arg[:2] == '-p':
            pos = arg[3]
        elif arg != '':
            srch.append(arg.lower())
    results = []
    cprint('$green'Y,"Search Type: ", '$lgreen', typ)
    if search_all:
        cprint('$green'Y,"Searching all Positions...")
    else:
        cprint('$green'Y,"Search Position: ",'$lgreen', pos)
    if typ == 'intersection':
        refined_results = []
    for i in range(len(srch)):
        cprint('$green'Y,"Searching: ",'$lgreen', srch[i])
        if i == 0 or typ == 'union':
            targets = images
            collection = results
        else:
            targets = results
            collection = refined_results
        for target in targets:
            if search_all:
                for item in target:
                    if srch[i] in item.lower() and target not in collection:
                        collection.append(target)
            else:
                if target[pos] and srch[i] in target[pos].lower():
                    if target not in collection:
                        collection.append(target)
        if i > 0 and typ == 'intersection':
            results = list(refined_results)
    for item in results:
        pretty_file_name(item,display = True)
    menu_args = {'TITLE': 'Save Options',
                    'F': 'Full file name',
                    'T':'Title Only',
                    '[0-9]':'Title at Position',
                    'P':'Title as Search Position',
                    'Return':'Return Without Save'}
    sel = menu(menu_args)
    res = []
    if sel == '' or sel[0] in ('r','R'):
        cprint('$red','Returning without save')
        return
    if sel in ('F','f'):
        for f in results:
            res.append(list_to_dotstring(f))
    elif sel in ('p', 'P'):
        sel = pos # next if, we save only the position from the find
    elif sel in ('t','T'):
        sel = 2
    else:
        try:
            sel = int(sel)
        except ValueError, TypeError:
            cprint('$red',"Not a valid value, skipping save...")
            return 
    if sel in range(0,9):
        for f in results:
            if f[sel]:
                s = f[sel]
                if split:
                    s = re.sub(r'([A-Z])', r' \1', s);
                res.append(s)
    t = 'File from {t} search: {s} at position {p}'.format(
            t = typ, s = srch, p = sel )
    write_to_file(res,'_titles.txt', t, mode='a') 
        
    


#-------------- CLEANING ODD FILES ------------------------------------------#

def write_names():
    """Match names from images to whos_who, print all to file.
    
    DEPRECIATED: load_whos_who is now load_file_as_dict()
    Keeping as is for historical documentation."""
    quicknames = load_artists_in_dir()
    ww = load_whos_who('__whos_who.txt')
    names = []
    for artist in quicknames:
        if artist in ww:
            n = u'{quickname}, {fullname}'.format(
                                quickname = artist,fullname = ww[artist])
            names.append(n)
        else:
            n = u'{quickname}, ** {title}'.format(
                                quickname = artist, title = artist.title())
            names.append(n)
    write_to_file(names,'_names.txt','Artist Names and Quicknames')


def gather_artists():
    """Load and combine artist names from files '_artists_logged.txt' and '_artists_add.txt'."""
    artists = []
    for f in ('_artists.txt', '_add.txt'):
        add_file_to_list(f,artists)
    a_set = sorted(set(artists))
    return a_set


def under_to_camel():
    """Clean up the image file names: my_title to myTitle
    
    titles with underscores replace with camel
    NOTE: for safety, this function only prints the mv commands,
    review and then copy / paste into terminal"""
    images = load_images_as_lists()
    for image in images:
        i = list(image)
        change = False
        if len(i) > 3 and '_' in i[2]:
            new_title = ''
            name = re.split(r'_',i[2])
            for n in name:
                n = n[0].upper() + n[1:]
                new_title += n
            new_title = new_title[0].lower() + new_title[1:]
            i[2] = new_title
            change = True
        if change:
            old_image = list_to_dotstring(image)
            new_image = list_to_dotstring(i)
            print_bash_rename(old_image, new_image)


def add_dots():
    """Read in titles with added dots from file, make alterations"""
    images = load_images_as_lists()
    titles = load_file_as_list('_titles.txt')
    for title in titles:
        s = re.split(r'\.',title)
        strip = ''
        for word in s:
            strip += word
        for image in images:
            if len(image) > 3 and image[2] == strip:
                old_image = list_to_dotstring(image)
                i = list(image)
                i[2] = title
                new_image = list_to_dotstring(i)
                print_bash_rename(old_image, new_image)


def make_quicknames(artists):
    """Get artist's names from file with format: last, first
    
    return list with format: [('quickname','first last')]"""
    registry = []
    for artist in artists:
        a = re.split(r', ',artist)
        quickname = unidecode(a[0].lower())
        if len(a) == 1:
            full_name = a[0]
        else:
            full_name = a[1] + ' ' + a[0]
        registry.append((quickname,full_name))       
    return registry


def artist_dict_from_files():
    """Turn artist list from files into a dictionary.
    
    input form: last name, first name
    returns: quickname, Full Name"""
    artists_list = gather_artists()
    registry = make_quicknames(artists_list)
    return dict(registry)


#-------------- RENAMING IMAGES ---------------------------------------------#

def print_bash_rename(old_name, new_name):
    rename = 'mv ' + CURRDIR + old_name + ' ' + CURRDIR + new_name
    cprint('$red', 'mv ', '$green'Y, old_name, ' ', '$blue', new_name)
    return rename


def execute_bash_rename(f='_rename.txt'):
    l = load_file_as_list(f)
    for item in l:
        if item[:3] == "mv ":
            subprocess.check_call(item, shell=True)
            cprint('$yellow', "executing: ", '$red', item)
    return


def alter_txt(text,operation,pattern,add=''):
    """Alter text with a regex, pivot on a group.
    
    see examples in alter_file_names below"""
    m = re.search(pattern,text)
    new_text = ''
    if m and m.groups() > 0:
        if operation == 'prepend':
            new_text = text[0:m.start(1)] + add + text[m.start(1):len(text)]
        elif operation == 'append':
            new_text = text[0:m.end(1)] + add + text[m.end(1):len(text)]
        elif operation == 'remove':
            new_text = text[0:m.start(1)] + text[m.end(1):len(text)]
        elif operation == 'replace':
            new_text = text[0:m.start(1)] + add + text[m.end(1):len(text)]
        return new_text
    else:
        return None


def alter_file_names(objective,pattern,replacement=''):
    """Find offending names and print an mv command.
    
    regex expects at least one group
    examples:
        'prepend', r'\.(\d\d)\.','19' : 47 to 1947
        'append', r'\.(1900)\.','s' : 1900 to 1900s
        'slice', r'(1900\.)19\d+' : 1900.1947 to 1947
        'replace', r'(__)', '.' : __detail to .detail
    """
    directory = load_directory_as_list(CURRDIR)
    p = re.compile(pattern)
    r = re.compile(replacement)
    for f in directory:
        if p.search(f) != None:
            new_name = alter_txt(f, objective, p, replacement)
            print_bash_rename(f, new_name)         


def lower_first_character():
    """Clean up the file name sections: MyName.FirstChar to myName.firstChar.
    
    NOTE: for safety, this function only prints the mv commands to 
    file _rename.txt, review and then [X] EXECUTE in terminal."""
    images = load_images_as_lists()
    renames = []
    for image in images:
        new = list(image)
        change = False
        for i in range(len(new)):
            if new[i][0].isupper():
                new[i] = new[i][0].lower() + new[i][1:]
                change = True
        if change:
            old_name = list_to_dotstring(image)
            new_name = list_to_dotstring(new)
            renames.append(print_bash_rename(old_name, new_name))
    write_to_file(renames,'_rename.txt','Rename Commands') 
    print 'Review _rename.txt and then press X to EXECUTE'


def space_rinse_and_repeat(pos = 2):
    """Reads new titles from file, finds old file and prints bash mv.
    
    Save list of titles and open file. Split with spaces where it
    should be capitalized, and save as _titles.txt.  This function takes the
    file, makes a camel version of title,finds the original in the directory,
    and writes out the rename commands to _rename.txt. Review the rename    
    commands and copy / paste into the terminal. 
    Assumes file format: name.date.title.etc.jpg. Change pos to target other 
    than title position.
    """  
    images = load_images_as_lists()
    news = load_file_as_list('_titles.txt')
    renames = []
    for n in news:
        old = re.sub(' ', '', n)
        new = n.title()
        new = re.sub(' ', '', new)
        new = new[0].lower() + new[1:]
        for image in images:
            if len(image) > pos + 1 and image[pos] == old:
                old_image = list_to_dotstring(image)
                ni = list(image)
                ni[2] = new
                new_image = list_to_dotstring(ni)
                renames.append(print_bash_rename(old_image, new_image))
                break
    write_to_file(renames,'_rename.txt','Rename Commands') 
    print 'Review _rename.txt and then press X to EXECUTE'


def encode_str(str = 'andre.1999.AluminumDoubleTwelver.3versions'):
    """TODO: make a title coder / decoder """
    str = 'andre.1999.AluminumDoubleTwelver.3versions'
    str = str.encode('base-64','strict')
    print 'Encoded String: ' + str;
    print 'Decoded String: ' + str.decode('base-64','strict') 


#------------- ASSEMBLE THE ARMY  -------------------------------------------#

def check_whos_who():
    print "Loading images..."
    images = load_images_as_lists()
    ww = load_file_as_dict('__whos_who.txt')
    if not ww:
        cprint('$red',"Returning without loading Who's Who")
        return None
    unkn_artist = []
    for image in images:
        if image[0] not in ww and image[0] + ' : ' not in unkn_artist:
            print 'No record of: {}'.format(image[0])
            unkn_artist.append(image[0] + ' : ')
    if unkn_artist:
        cprint('$red',"Unknown Artists Found")
        unkn_artist.append("# Add artist full name and update who\'s who. For example: zorn: John Zorn")
        write_to_file(unkn_artist,'_whos_new.txt','Add The Following:','list','a')
    else:
        cprint('$green', 'Who\'s Who up to date.')


def update_whos_who():
    """Save whos_who to _whos_old and add whos_new to whos_who."""
    ww = load_file_as_dict('__whos_who.txt')
    wn = load_file_as_dict('_whos_new.txt')
    write_to_file(ww,'_whos_old.txt',"Who's Who Archive",'dict','a')
    new_ww = dict(ww.items() + wn.items())
    write_to_file(new_ww,'__whos_who.txt',
        "Who's Who: Quickname and Full Name",'dict')


def md_title_link(l):
    """Makes a Markdown Title linked to an image.
    
    Takes a list style image, returns md string"""
    artist, date, title, file_name = pretty_file_name(l,display = False)
    link = '[' + title + '](' + CURRDIR + file_name + ')'
    return link

           
def md_index():
    """Print image directory as markdown"""
    print "Loading Images..."
    images = load_images_as_lists()
    print "Loading Who's Who..."
    ww = load_file_as_dict('__whos_who.txt')
    print "Saving File..."
    md = list(('## Image Index\n','\n'))
    
        # print alphabet-index:
    head = ''
    for i in range(65, 91):
        head += '[' + chr(i) + '][] '
    md.append(head)
    c = 64  # current index letter
    j = 0
    last = ''
    
    while j < len(images):
            # check artist name from file against who's who
        quickname = images[j][0]
        if images[j][0] not in ww:
            print 'Error on {num}, No record of: {image}'.format(
                        num = j, image = images[j] )
            print 'Please update Who\'s Who'
            j += 1
            continue
        md_name = '### ' + ww[images[j][0]] + '\n'
        year = images[j][1]
        if year == '1990s': # generic year, don't list
            md_title = md_title_link(images[j]) + '\n'
        else:
            md_title = md_title_link(images[j]) + ', ' + year + '\n'
        curr_c = quickname[0]
        if ord(curr_c) > c + 32: # a to A etc.
            c = ord(curr_c) - 32
            md.append('-----\n')
            md.append('*[---back to top---][Artist Names and Images]*\n')
            md.append('#### ' + chr(c))
            md.append('-----\n')
        if quickname != last:
            last = quickname
            md.append(md_name)
        md.append(md_title)
        j += 1
    write_to_file(md,'_index.md','Artist Names and Images')
    print "Contverting to HTML..."
    md = CURRDIR + '_index.md'
    html = CURRDIR + '_index.html'
    pandoc = 'pandoc -f markdown -t html -o {} {}'.format(md, html)
    d = subprocess.check_output(pandoc, shell=True)
    print d
    # except CalledProcessError: 
    #     cprint('$red','Unable to Save html', d)


def init_dir():
    if not nav_dir():
        return None
    check_whos_who()
    return True   


def init():
    """Run a loop with program possibilities."""
    
    trm_sect('Initializing')
    if not init_dir():
        cprint('$red',"Quitting on error loading directory")
        return
    trm_sect('Image Indexer')
    sel = ''
    while sel != 'Q':
        menu_args = {'TITLE':'Please Enter one of the following',
                    'md': 'Create markdown INDEX',
                    'title -f0 -tz -p2':
                        'Create TITLES list -from -to -file.name.position)',
                    'find -a/-t/-p -i/-u': 
                        'FIND files by artist/title/file.name.position intersetion/union',
                    'R': 'RINSE titles',
                    'L': 'LOWER-CASE titles',
                    'W': 'Update WHO\'S WHO\'S',
                    'X': 'EXECUTE rename commands',
                    'cd': 'change DIRECTORY',
                    'xd': 'cross directory comparison',
                    'Q' : 'Quit'}
        sel = menu(menu_args)
        if not sel:
            continue
        elif sel.lower() == 'md':
            print 'Creating Markdown Index...'
            md_index()
        elif sel[0:4].lower() == 'find':
            print 'Find files...'
            find(sel[4:])
        elif sel[0:5].lower == 'title':
            print '\nWriting Titles to File...\n'
            write_titles(sel[5:])   
        elif sel in ('r','R'):
            print '\nWriting Title Rename Commands to File...\n'
            space_rinse_and_repeat()
        elif sel in ('l','L'):
            print '\nWriting Title Rename Commands to File...\n'
            lower_first_character()
        elif sel in ('w','W'):
            print 'Updating Who\'s Who...'
            update_whos_who()
        elif sel in ('x','X'):
            print '\nExecuting Bash Renames...\n'
            execute_bash_rename()
        elif sel[0:2].lower() == 'cd':
            print '\nChanging Directory...\n'
            sel = sel[2:].strip()
            nav_dir(sel)
            check_whos_who()
        elif sel[0:2].lower() == 'xd':
            sel = sel[2:].strip()
            dirs = re.split(" ",sel)
            print dirs
            dir1 = dirs[0].strip()
            dir2 = dirs[1].strip()
            try:
                compare_directories(dir1,dir2)
            except IndexError, subprocess.CalledProcessError:
                cprint('$red',"Not valid Directories")
        elif sel in ('Q','q'):
            print 'Exiting...'
            sel = 'Q'
            


init()