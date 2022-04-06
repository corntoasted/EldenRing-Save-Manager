from tkinter import *
from tkinter import font as FNT
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter import ttk
from collections import Counter
import subprocess, os, zipfile, requests, re, time, hexedit, webbrowser
import tkinter as TKIN

# Directories and settings
savedir = ".\\data\\save-files\\"
app_title = "Elden Ring Save Manager"
backupdir = ".\\data\\backup\\"
update_dir = ".\\data\\updates\\"
version = 'v1.4'
v_num = 1.4 # Used for checking version for update
video_url = 'https://youtu.be/okJIfoLO38s'
background_img = './data/background.png'
icon_file = './data/icon.ico'
gamesavedir_txt = '.\\data\\GameSaveDir.txt'
bk_p = (-140,20) # Background image position
#gamedir = "%APPDATA%\\EldenRing\\"

# Load and parse save directory
if not os.path.exists(gamesavedir_txt):
    with open(gamesavedir_txt, 'w') as fh:
        fh.write('"%APPDATA%\\EldenRing\\"')

with open(gamesavedir_txt, 'r') as fh:
    gamedir = fh.readline()

def get_steamid():
    th = subprocess.run(f'dir {gamedir}', stdout=subprocess.PIPE, shell=True)
    x = re.findall(r'\d{17}',str(th))
    if len(x) < 1:
        popup("Steam ID not detected. Ensure your default game directory\nis set properly before performing any actions.")
        return None
    else:
        return x[0]



def import_save():
    if os.path.isdir(savedir) is False:
        run_command(f'md {savedir}')
    d = fd.askopenfilename().replace("/", "\\")

    if len(d) < 1:
        return

    if not d.endswith(('ER0000.sl2')):
        popup('Select a valid save file!\nIt should be named: ER0000.sl2')
        return



    def cancel():
        popupwin.destroy()

    def done():
        name = ent.get().strip()
        if len(name) < 1:
            popup('No name entered.')
            return
        isforbidden = False
        for char in name:
            if char in "~'{};:./\,:*?<>|-!@#$%^&()+":
                isforbidden = True
        if isforbidden is True:
            popup('Forbidden character used')
            return
        elif isforbidden is False:
            entries = []
            for entry in os.listdir(savedir):
                entries.append(entry)
            if name.replace(' ', '-') in entries:
                popup('Name already exists')
                return



        id = user_steam_id


        newdir = "{}{}\\{}\\".format(savedir,name.replace(' ', '-'),id)
        cp_to_saves_cmd = "copy {} {}".format(f'"{d}"',newdir)

        if os.path.isdir(newdir) is False:
            cmd_out = run_command("md {}".format(newdir))

            if cmd_out[0]  == 'error':
                return
            lb.insert(END, "  " + name)
            cmd_out = run_command(cp_to_saves_cmd)
            if cmd_out[0] == 'error':
                return
            create_notes(name, newdir)


            file_id = hexedit.get_id(f'{newdir}\ER0000.sl2')
            if file_id != int(id):
                popup(f'Steam ID of file did not match your own ID\nAutomatically patched file with your Steam ID\nFile ID: {file_id}\nYour ID: {id}')
            hexedit.replace_id(f'{newdir}\ER0000.sl2',int(id))

            popupwin.destroy()


    popupwin = Toplevel(root)
    popupwin.title("Import")
    #popupwin.geometry("200x70")
    lab = Label(popupwin, text='Enter a Name:')
    lab.grid(row=0, column=0)
    ent = Entry(popupwin, borderwidth=5)
    ent.grid(row=1,column=0, padx=25, pady=10)
    x = root.winfo_x()
    y = root.winfo_y()
    popupwin.geometry("+%d+%d" %(x+200,y+200))
    but_done = Button(popupwin, text='Done', borderwidth=5, width=6, command=done)
    but_done.grid(row=2, column=0, padx=(25,65), pady=(0,15), sticky='w')
    but_cancel = Button(popupwin, text='Cancel', borderwidth=5, width=6, command=cancel)
    but_cancel.grid(row=2, column=0, padx=(70,0), pady=(0,15))



def open_folder():
    if len(lb.curselection()) < 1:
        popup('No listbox item selected.')
        return
    name = fetch_listbox_entry(lb)[0]
    cmd = f'start {savedir}{name.replace(" ", "-")}'
    run_command(cmd)


def forcequit():
    comm = "taskkill /IM eldenring.exe -F"
    popup(text='Are you sure?', buttons=True, command=comm)


def update_app():

    version_url = 'https://github.com/Ariescyn/EldenRing-Save-Manager/releases/latest'
    r = requests.get(version_url) # Get redirect url
    ver = float(r.url.split('/')[-1].split('v')[1])


    if ver > v_num:
        popup(text=f' Release v{str(ver)} Available\nClose the program and run the Updater.', buttons=True, functions=(root.quit,donothing), button_names=('Exit Now', 'Cancel'))

    else:
        popup('Current version up to date')
        return


def reset_default_dir():
    global gamedir
    with open(gamesavedir_txt, 'w') as fh:
        fh.write('"%APPDATA%\\EldenRing\\"')
    with open(gamesavedir_txt, 'r') as fh:
        gamedir = fh.readline()
    popup('Successfully reset default directory')


def create_notes(name,dir):
    """Create a notepad document in specified save slot."""
    name = name.replace(' ', '-')
    cmd = f'type nul > {dir}\\notes.txt'
    run_command(cmd)


def help_me():
    out = run_command("notepad ./data/readme.txt")


def load_listbox(lstbox):
    """LOAD current save files and insert them into listbox. This is Used
        to load the listbox on startup and also after deleting an item from the listbox to refresh the entries."""
    if os.path.isdir(savedir) is True:
        for entry in os.listdir(savedir):
            lstbox.insert(END, "  " + entry.replace('-', ' '))


def save_backup():
    """Quickly save a backup of the current game save. Used from the menubar."""
    comm = "Xcopy {} {} /E /H /C /I /Y".format(gamedir,backupdir)

    if os.path.isdir(backupdir) is False:
        cmd_out1 = run_command("md {}".format(backupdir))
        if cmd_out1[0] == 'error':
            return
    cmd_out2 = run_command(comm)
    if cmd_out2[0] == 'error':
        return
    else:
        popup('Backup saved successfully')


def load_backup():
    """Quickly load a backup of the current game save. Used from the menubar."""
    comm = "Xcopy {} {} /E /H /C /I /Y".format(backupdir,gamedir)
    if os.path.isdir(backupdir) is False:
        run_command("md {}".format(backupdir))

    if len(re.findall(r'\d{17}',str(os.listdir(backupdir)))) < 1:
        popup('No backup found')

    else:
        popup('Overwrite existing save?',command=comm, buttons=True)


def create_save():
    """Takes user input from the create save entry box and copies files from game save dir to the save-files dir of app"""
    name = cr_save_ent.get().strip()
    newdir = "{}{}".format(savedir,name.replace(' ', '-'))

    # Check the given name in the entry
    if len(name) < 1:
        popup('No name entered')

    isforbidden = False
    for char in name:
        if char in "~'{};:./\,:*?<>|-!@#$%^&()+":
            isforbidden = True
    if isforbidden is True:
        popup('Forbidden character used')

    if os.path.isdir(savedir) is False:
        #subprocess.run("md .\\save-files", shell=True)
        cmd_out = run_command("md {}".format(savedir))
        if cmd_out[0] == 'error':
            return


    # If new save name doesnt exist, insert it into the listbox,
    # otherwise duplicates will appear in listbox even though the copy command will overwrite original save
    if len(name) > 0 and isforbidden is False:
        cp_to_saves_cmd = "Xcopy {} {} /E /H /C /I /Y".format(gamedir,newdir)
        # /E – Copy subdirectories, including any empty ones.
        # /H - Copy files with hidden and system file attributes.
        # /C - Continue copying even if an error occurs.
        # /I - If in doubt, always assume the destination is a folder. e.g. when the destination does not exist
        # /Y - Overwrite all without PROMPT (ex: yes no)
        if os.path.isdir(newdir) is False:
            cmd_out = run_command("md {}".format(newdir))
            if cmd_out[0]  == 'error':
                return
            lb.insert(END, "  " + name)
            cmd_out = run_command(cp_to_saves_cmd)
            if cmd_out[0] == 'error':
                return
            create_notes(name, newdir)
        else:
            popup('File already exists, OVERWRITE?', command=cp_to_saves_cmd, buttons=True)


def donothing():
    pass


def load_save_from_lb():
    """Fetches currently selected listbox item and copies files to game save dir."""
    if len(lb.curselection()) < 1:
        popup('No listbox item selected.')
        return
    name = fetch_listbox_entry(lb)[0]
    comm = "Xcopy {}{}\\ {} /E /H /C /I /Y".format(savedir,name.replace(' ', '-'),gamedir)
    if not os.path.isdir(f'{savedir}{name}'):
        popup('Save slot does not exist.\nDid you move or delete it from data/save-files?')
        lb.delete(0,END)
        load_listbox(lb)
        return
    cmd_out = run_command(comm)
    if cmd_out[0] == 'error':
        return
    else:
        popup('Backup loaded successfully')


def popup(text, command=None, functions=False, buttons=False, button_names=('Yes', 'No')):
    """text: Message to display on the popup window.
       command: Simply run the windows CMD command if you press yes.
       functions: Pass in external functions to be executed for yes/no"""

    def run_cmd():
        cmd_out = run_command(command)
        popupwin.destroy()
        if cmd_out[0] == 'error':
            popupwin.destroy()

    def dontrun_cmd():
        popupwin.destroy()


    def run_func(arg):
        arg()
        popupwin.destroy()


    popupwin = Toplevel(root)
    popupwin.title("Manager")
    #popupwin.geometry("200x75")
    lab = Label(popupwin, text=text)
    lab.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    # Places popup window at center of the root window
    x = root.winfo_x()
    y = root.winfo_y()
    popupwin.geometry("+%d+%d" %(x+200,y+200))


    # Runs for simple windows CMD execution
    if functions is False and buttons is True:
        but_yes = Button(popupwin, text=button_names[0], borderwidth=5, width=6, command=run_cmd).grid(row=1, column=0, padx=(10,0), pady=(0,10))
        but_no = Button(popupwin, text=button_names[1], borderwidth=5, width=6, command=dontrun_cmd).grid(row=1, column=1, padx=(10,10), pady=(0,10))



    elif functions is not False and buttons is True:
        but_yes = Button(popupwin, text=button_names[0], borderwidth=5, width=6, command=lambda: run_func(functions[0])).grid(row=1, column=0, padx=(10,0), pady=(0,10))
        but_no = Button(popupwin, text=button_names[1], borderwidth=5, width=6, command=lambda: run_func(functions[1])).grid(row=1, column=1, padx=(10,10), pady=(0,10))
    # if text is the only arguement passed in, it will simply be a popup window to display text


def run_command(subprocess_command):
    """ Used throughout to run commands into subprocess and capture the output. Note that
        it is integrated with popup function for in app error reporting."""

    out = subprocess.run(subprocess_command, shell=True , capture_output=True, text=True)
    if len(out.stderr) > 0:
        popup(out.stderr)
        return ('error',out.stderr)

    else:
        return ('Successfully completed operation',out.stdout)


def delete_save():
    name = fetch_listbox_entry(lb)[0]
    comm = "rmdir {}{} /s /q".format(savedir,name)
    def yes():
        out = run_command(comm)
        lb.delete(0,END)
        load_listbox(lb)
    def no():
        return
    popup(f'Delete {fetch_listbox_entry(lb)[1]}?', functions=(yes,no), buttons=True)


def fetch_listbox_entry(lstbox):
    """ Returns currently selected listbox entry.
        internal name is for use with save directories and within this script.
        Name is used for display within the listbox"""


    name = ''
    for i in lstbox.curselection():
        name = name + lstbox.get(i)
    internal_name = name.strip().replace(' ', '-')
    return (internal_name, name)


def about():
    popup(text='Author: Lance Fitz\nEmail: scyntacks94@gmail.com\nGithub: github.com/Ariescyn')


def rename_slot():
    def cancel():
        popupwin.destroy()

    def done():
        new_name = ent.get()
        if len(new_name) < 1:
            popup('No name entered.')
            return
        isforbidden = False
        for char in new_name:
            if char in "~'{};:./\,:*?<>|-!@#$%^&()+":
                isforbidden = True
        if isforbidden is True:
            popup('Forbidden character used')
            return
        elif isforbidden is False:
            entries = []
            for entry in os.listdir(savedir):
                entries.append(entry)
            if new_name in entries:
                popup('Name already exists')
                return

            else:
                newnm = new_name.replace(' ', '-')
                cmd = f'rename "{savedir}{lst_box_choice}" "{newnm}"'
                run_command(cmd)
                lb.delete(0,END)
                load_listbox(lb)
                popupwin.destroy()

    lst_box_choice =  fetch_listbox_entry(lb)[0]
    if len(lst_box_choice) < 1:
        popup('No listbox item selected.')
        return

    popupwin = Toplevel(root)
    popupwin.title("Rename")
    #popupwin.geometry("200x70")
    lab = Label(popupwin, text='Enter new Name:')
    lab.grid(row=0, column=0)
    ent = Entry(popupwin, borderwidth=5)
    ent.grid(row=1,column=0, padx=25, pady=10)
    x = root.winfo_x()
    y = root.winfo_y()
    popupwin.geometry("+%d+%d" %(x+200,y+200))
    but_done = Button(popupwin, text='Done', borderwidth=5, width=6, command=done)
    but_done.grid(row=2, column=0, padx=(25,65), pady=(0,15), sticky='w')
    but_cancel = Button(popupwin, text='Cancel', borderwidth=5, width=6, command=cancel)
    but_cancel.grid(row=2, column=0, padx=(70,0), pady=(0,15))


def update_slot():
    lst_box_choice =  fetch_listbox_entry(lb)[0]
    if len(lst_box_choice) < 1:
        popup('No listbox item selected.')
        return
    cmd = "Xcopy {} {}{} /E /H /C /I /Y".format(gamedir,savedir,lst_box_choice)
    popup(text="Are you sure?", buttons=True, command=cmd)


def change_default_dir():
    global gamedir
    newdir = fd.askdirectory()
    if len(newdir) < 1: # User presses cancel
        return

    # Check if selected directory contains 17 digit steamid folder and GraphicsConfig.xml
    if os.path.exists(f'{newdir}/GraphicsConfig.xml') and len(re.findall(r'\d{17}',str(os.listdir(newdir)))) > 0:
        newdir = f'"{newdir}"'


        with open('.\\data\\GameSaveDir.txt', 'w') as fh:
            fh.write(newdir)
        gamedir = newdir
        popup(f'Directory set to:\n {newdir}')
    else:
        popup('Cant find savedata in this Directory.\nThe selected folder should contain GraphicsConfig.xml and\na folder named after your 17 digit SteamID')


def char_manager():

    def readme():
        run_command("notepad ./data/copy-readme.txt")

    def open_video():
        webbrowser.open_new_tab(video_url)

        # ACCIDENTALLY LEFT THIS CRAP HERE! I will remove it on next release.
        rn = Toplevel(popupwin)
        rn.title("Rename")
        #popupwin.geometry("200x70")
        lab = Label(rn, text='Enter a new name for SOURCE character:')
        lab.grid(row=0, column=0)
        ent = Entry(rn, borderwidth=5)
        ent.grid(row=1,column=0, padx=25, pady=10)
        x = popupwin.winfo_x()
        y = popupwin.winfo_y()
        rn.geometry("+%d+%d" %(x+200,y+200))
        but_done = Button(rn, text='Done', borderwidth=5, width=6, command=do)
        but_done.grid(row=2, column=0, padx=(25,65), pady=(0,15), sticky='w')
        but_cancel = Button(rn, text='Cancel', borderwidth=5, width=6, command=lambda: rn.destroy())
        but_cancel.grid(row=2, column=0, padx=(70,0), pady=(0,15))





    def get_char_names(lstbox,drop,v):
        v.set('Character')
        name = fetch_listbox_entry(lstbox)[0]
        file = f'{savedir}{name}\\{user_steam_id}\\ER0000.sl2'
        names = hexedit.get_names(file)
        drop['menu'].delete(0,'end') # remove full list

        index = 1
        for opt in names:
            if not opt is None:
                opt = f'{index}. {opt}'
                drop['menu'].add_command(label=opt, command=TKIN._setit(v, opt))
                index += 1


    def do_copy():
        def pop_up(txt,bold=True):
            win = Toplevel(popupwin)
            win.title("Manager")
            lab = Label(win, text=txt)
            if bold is True:
                lab.config(font=bolded)
            lab.grid(row=0, column=0, padx=15, pady=15, columnspan=2)
            x = popupwin.winfo_x()
            y = popupwin.winfo_y()
            win.geometry("+%d+%d" %(x+200,y+200))


        src_char = vars1.get() # "1. charname"
        dest_char = vars2.get()

        name1 = fetch_listbox_entry(lb1)[0] # Save file name. EX: main
        name2 = fetch_listbox_entry(lb2)[0]

        if len(name1) < 1 or len(name2) < 1:
            pop_up(txt='Slot not selected')
            return
        if src_char == 'Character' or dest_char == 'Character':
            pop_up(txt='Character not selected')

        src_file = f'{savedir}{name1}\{user_steam_id}\\ER0000.sl2'
        dest_file = f'{savedir}{name2}\{user_steam_id}\\ER0000.sl2'


        src_ind = int(src_char.split('.')[0])
        dest_ind = int(dest_char.split('.')[0])

        # Duplicate names check
        src_char_real = src_char.split('. ')[1]
        dest_names = hexedit.get_names(dest_file)
        src_names = hexedit.get_names(src_file)

        if max(Counter(dest_names).values()) > 1:
            pop_up("Sorry, can't handle writing to file with duplcate character names.", bold=False)
            return


        src_names.pop(src_ind -1)
        dest_names.pop(dest_ind - 1)
        backup_path = r'.\data\temp\ER0000.sl2'

        if src_file == dest_file:
            cmd = f'copy "{src_file}" {backup_path} /Y'
            x = run_command(cmd)
            rand_name = hexedit.random_str()
            hexedit.change_name(backup_path,rand_name,src_ind) # Change backup to random name
            hexedit.copy_save(backup_path,src_file,src_ind,dest_ind)
            hexedit.change_name(src_file,rand_name,dest_ind)
            get_char_names(lb1, dropdown1,vars1)
            get_char_names(lb2,dropdown2,vars2)
            vars1.set('Character')
            vars2.set('Character')
            pop_up(txt='Success!\nDuplicate names not supported\nGenerated a new random name', bold=False)
            return

        elif src_char_real in dest_names:
            cmd = f'copy "{src_file}" {backup_path} /Y'
            x = run_command(cmd)
            rand_name = hexedit.random_str()
            hexedit.change_name(backup_path, rand_name ,src_ind)
            hexedit.copy_save(backup_path,dest_file,src_ind,dest_ind)
            hexedit.change_name(dest_file,rand_name,dest_ind)

            get_char_names(lb1, dropdown1,vars1)
            get_char_names(lb2,dropdown2,vars2)
            vars1.set('Character')
            vars2.set('Character')
            pop_up(txt='Duplicate names not supported\nGenerated a new random name', bold=False)
            return


        hexedit.copy_save(src_file,dest_file,src_ind,dest_ind)
        hexedit.change_name(dest_file,src_char_real,dest_ind)



        get_char_names(lb1, dropdown1,vars1)
        get_char_names(lb2,dropdown2,vars2)

        vars1.set('Character')
        vars2.set('Character')

        pop_up(txt='Success!')

    def cancel():
        popupwin.destroy()



    popupwin = Toplevel(root)
    popupwin.title("Character Manager")
    popupwin.resizable(width=True, height=True)
    popupwin.geometry("650x500")

    bolded = FNT.Font(weight='bold') # will use the default font

    x = root.winfo_x()
    y = root.winfo_y()
    popupwin.geometry("+%d+%d" %(x+200,y+200))


    menubar = Menu(popupwin)
    popupwin.config(menu=menubar) # menu is a parameter that lets you set a menubar for any given window

    helpmen = Menu(menubar, tearoff=0)
    helpmen.add_command(label='Readme', command=readme)
    helpmen.add_command(label='Watch Video', command=open_video)
    menubar.add_cascade(label='Help', menu=helpmen)

    srclab = Label(popupwin,text='Source File' )
    srclab.config(font=bolded)
    srclab.grid(row=0, column=0, padx=(70,0),pady=(20,0) )

    lb1 = Listbox(popupwin, borderwidth=3, width=15, height=10, exportselection=0)
    lb1.config(font=bolded)
    lb1.grid(row=1, column=0,padx=(70,0), pady=(0,0))
    load_listbox(lb1)


    destlab = Label(popupwin,text='Destination File' )
    destlab.config(font=bolded)
    destlab.grid(row=0, column=1, padx=(175,0),pady=(20,0))

    lb2 = Listbox(popupwin, borderwidth=3, width=15, height=10, exportselection=0)
    lb2.config(font=bolded)
    lb2.grid(row=1, column=1,padx=(175,0), pady=(0,0))
    load_listbox(lb2)


    opts = ['']
    opts2 = ['']
    vars1 = StringVar(popupwin)
    vars1.set('Character')

    vars2 = StringVar(popupwin)
    vars2.set('Character')

    dropdown1 = OptionMenu(popupwin, vars1, *opts)
    dropdown1.grid(row=4,column=0, padx=(70,0), pady=(20,0))

    dropdown2 = OptionMenu(popupwin, vars2, *opts2)
    dropdown2.grid(row=4,column=1, padx=(175,0), pady=(20,0))

    but_select1 = Button(popupwin, text='Select', command=lambda: get_char_names(lb1, dropdown1,vars1))
    but_select1.grid(row=3,column=0, padx=(70,0), pady=(10,0))

    but_select2 = Button(popupwin, text='Select', command=lambda: get_char_names(lb2,dropdown2,vars2))
    but_select2.grid(row=3,column=1, padx=(175,0), pady=(10,0))

    but_copy = Button(popupwin, text='Copy', command=do_copy)
    but_copy.config(font=bolded)
    but_copy.grid(row=5,column=1, padx=(175,0), pady=(50,0))

    but_cancel = Button(popupwin, text='Cancel', command=cancel)
    but_cancel.config(font=bolded)
    but_cancel.grid(row=5,column=0, padx=(70,0), pady=(50,0))

    mainloop()



def quick_restore():
    lst_box_choice =  fetch_listbox_entry(lb)[0]
    if len(lst_box_choice) < 1:
        popup('No listbox item selected.')
        return
    cmd = "Xcopy .\\data\\temp\\{} {}{} /E /H /C /I /Y".format(lst_box_choice,savedir,lst_box_choice)
    x = run_command(cmd)
    if x[0] != 'error':
        popup('Successfully restored backup.')



def quick_backup():
    lst_box_choice =  fetch_listbox_entry(lb)[0]
    if len(lst_box_choice) < 1:
        popup('No listbox item selected.')
        return
    cmd = "Xcopy {}{} .\\data\\temp\\{} /E /H /C /I /Y".format(savedir,lst_box_choice,lst_box_choice)
    x = run_command(cmd)
    if x[0] != 'error':
        popup('Successfully created backup.')

def rename_characters():




    def do():
        choice = vars.get()
        choice_real = choice.split('. ')[1]
        slot_ind = int(choice.split('.')[0])
        new_name = name_ent.get()
        if len(new_name) > 16:
            popup('Name too long. Maximum of 16 characters')
            return


        # Duplicate names check
        dest_names = names
        dest_names.pop(slot_ind - 1)

        if new_name in dest_names:
            popup('Save can not have duplicate names')
            return


        hexedit.change_name(path,new_name,slot_ind)
        popup('Successfully Renamed Character')
        drop['menu'].delete(0,'end')
        rwin.destroy()





    name = fetch_listbox_entry(lb)[0]
    path = f'{savedir}{name}\{user_steam_id}\ER0000.sl2'
    names = hexedit.get_names(path)
    chars = []
    for ind,i in enumerate(names):
        if i != None:
            chars.append(f'{ind +1}. {i}')

    rwin = Toplevel(root)
    rwin.title("Rename Character")
    rwin.resizable(width=False, height=False)
    rwin.geometry("200x150")

    bolded = FNT.Font(weight='bold') # will use the default font
    x = root.winfo_x()
    y = root.winfo_y()
    rwin.geometry("+%d+%d" %(x+200,y+200))

    opts = chars
    vars = StringVar(rwin)
    vars.set('Character')

    drop = OptionMenu(rwin, vars, *opts)
    drop.grid(row=0,column=0, padx=(35,0), pady=(10,0))

    name_ent = Entry(rwin,borderwidth=5)
    name_ent.grid(row=1, column=0, padx=(35,0), pady=(10,0))

    but_go = Button(rwin, text='Rename', borderwidth=5, command=do)
    but_go.grid(row=2,column=0, padx=(35,0), pady=(10,0))


def changelog():
    out = run_command("notepad ./data/changelog.txt")


# ----- MAIN GUI CONTENT -----


root = Tk()
root.resizable(width=False, height=False)
root.title('{} {}'.format(app_title, version))
root.geometry('785x541')
root.iconbitmap(icon_file)


bg_img = ImageTk.PhotoImage(image=Image.open(background_img))
background = Label(root, image=bg_img)

background.place(x=bk_p[0], y=bk_p[1], relwidth=1, relheight=1)




menubar = Menu(root) # Create menubar attached to main window
root.config(menu=menubar) # menu is a parameter that lets you set a menubar for any given window

filemenu = Menu(menubar, tearoff=0) # Create file menu attached to menubar
filemenu.add_command(label="Save Backup", command=save_backup)
filemenu.add_command(label="Restore Backup", command=load_backup)
filemenu.add_command(label="Import Save File", command=import_save)
filemenu.add_separator()
filemenu.add_command(label="Force quit EldenRing", command=forcequit)
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu) # add_cascade creates a new hierarchical menu by associating a given menu to a parent menu



editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Change Default Directory", command=change_default_dir)
editmenu.add_command(label="Reset To Default Directory", command=reset_default_dir)
editmenu.add_command(label="Check for updates", command=update_app)
menubar.add_cascade(label='Edit', menu=editmenu)

toolsmenu = Menu(menubar, tearoff=0)
toolsmenu.add_command(label='Character Manager', command=char_manager)
menubar.add_cascade(label='Tools', menu=toolsmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Readme", command=help_me)
helpmenu.add_command(label='About', command=about)
helpmenu.add_command(label='Changelog', command=changelog)
menubar.add_cascade(label="Help", menu=helpmenu)



create_save_lab = Label(root,text='Create Save:' )
create_save_lab.grid(row=0, column=0, padx=(80,10), pady=(0,260))

cr_save_ent = Entry(root,borderwidth=5)
cr_save_ent.grid(row=0, column=1, pady=(0,260))

but_go = Button(root, text='Done', borderwidth=5, command=create_save)
but_go.grid(row=0,column=2, padx=(10,0), pady=(0,260))

lb = Listbox(root, borderwidth=3, width=25, height=16)
bolded = FNT.Font(weight='bold') # will use the default font
lb.config(font=bolded)
lb.grid(row=0, column=3, padx=(110,0), pady=(30,0))


#-----------------------------------------------------------
# right click popup menu in listbox

def do_popup(event):
	try:
		rt_click_menu.tk_popup(event.x_root, event.y_root) # Grab x,y position of mouse cursor
	finally:
		rt_click_menu.grab_release()

def open_notes():
    name = fetch_listbox_entry(lb)[0]
    if len(name) < 1:
        popup('Select a save slot first.')
        return
    cmd = f'notepad {savedir}{name}\\notes.txt'
    out = run_command(cmd)


rt_click_menu = Menu(lb, tearoff = 0)
rt_click_menu.add_command(label="Edit Notes", command=open_notes)
rt_click_menu.add_command(label="Rename Save", command=rename_slot)
rt_click_menu.add_command(label="Rename Characters", command=rename_characters)
rt_click_menu.add_command(label="Update", command=update_slot)
rt_click_menu.add_command(label='Quick Backup', command=quick_backup)
rt_click_menu.add_command(label="Quick Restore", command=quick_restore)
rt_click_menu.add_command(label="Open File Location", command=open_folder)
#rt_click_menu.add_command(label=)
lb.bind("<Button-3>", do_popup) # button 3 is right click, so when right clicking inside listbox, do_popup is executed at cursor position


load_listbox(lb) # populates listbox with saves on runtime

but_load_save = Button(root, text='Load Save', borderwidth=5, command=load_save_from_lb)
but_delete_save = Button(root, text='Delete Save', borderwidth=5, command=delete_save)

but_load_save.grid(row=3, column=3, pady=(12,0))
but_delete_save.grid(row=3, column=3, padx=(215,0), pady=(12,0))

user_steam_id = get_steamid()
root.mainloop()
