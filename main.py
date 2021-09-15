import json,os,csv,datetime
from tkinter import Entry, Label, Tk, Button


##########################
### GLOBALS VARIABLES ###
##########################
CONF = {} #contains path of folders
LAST_SYNC = "" #contains date of last execution


##########################
####### FUNCTIONS ########
##########################

def open_conf():
    """
    open the config file and return his content in CONF as a dict
    """
    global CONF
    with open("conf.json", "r") as read_file:
        CONF = json.load(read_file)

def save_conf():
    """
    open the config file and save the content of CONF in it
    """
    global CONF
    with open("conf.json", "w") as write_file:
        json.dump(CONF, write_file)

def open_logs():
    """
    open the logs file and return his content in LAST_SYNC as a dict
    """
    global LAST_SYNC
    with open('log.csv', "r", encoding = 'utf-8')  as openfile:
        data = csv.reader(openfile)
        logs = []
        for lines in data : 
            logs.append(lines)
        
        LAST_SYNC = logs[len(logs)-1]
        LAST_SYNC = LAST_SYNC[0]

def save_logs():
    """
    open the logs file and save the current date and time in it
    """
    with open('log.csv', 'a+', newline='') as f:
      
        write = csv.writer(f)
        write.writerow([get_date_and_time()])

def get_date_and_time():
    """
    get the current time and stor it in NOW_TIME
    """
    now_time = datetime.datetime.now()
    return now_time.strftime("%d/%m/%Y %H:%M:%S")
    


def sync():
    """
    execution of the command, with the source and the destination --> src and dst then save logs with save_logs()
    """
    src = CONF["src"]
    dst = CONF["dst"]
    cmd = f"sudo rsync -zavh --delete --recursive {src}  {dst}"
    os.popen(cmd)

    save_logs()

def Save():
    """
    save the new path and reload it
    """
    global CONF
    CONF['src'] = src_ent.get()
    CONF['dst'] = dst_ent.get()
    save_conf()

def uisetup():
    """
    creation and configuration of the interface's objects
    """
    global src_ent 
    global dst_ent
    #creation of text
    Label(WIN, text="Source", font= 20).grid(column=1, row=1)
    Label(WIN, text="---->", font=20).grid(column=2, row=1)
    Label(WIN, text="Destination", font=20).grid(column=3, row=1)
    Label(WIN, text="If you made any changes on the source path or the destination path \n \
        please save before start sync" ).grid(column=1, row=3, columnspan=3)
    open_logs() #opening logs file to display last sync
    Label(WIN, text=f"Last Sync : {LAST_SYNC} \n\n ", font=20).grid(column=2, row=5)

    #creation of Button
    Button(WIN, text='SAVE', command=Save, width=20).grid(column=2, row=4)
    Button(WIN, text='SYNC NOW', command=sync, width=40, height= 2, background="green").grid(column=2, row=6)
    Button(WIN, text='Exit', command=WIN.destroy).grid(column=3, row=7, sticky="SE")



    #config of the entry
    open_conf() #load paths to display them
    src_ent = Entry(WIN)
    src_ent.grid(column=1, row=2)
    src_ent.insert(0, CONF['src'])
    dst_ent = Entry(WIN)
    dst_ent.grid(column=3, row=2)
    dst_ent.insert(0, CONF['dst'])

###########################
####### MAIN PROGRAM ######
###########################

#window creation
WIN = Tk()
#window title 
WIN.title("Sync_script")

uisetup()

WIN.mainloop()
