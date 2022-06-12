from lib2to3.pgen2.token import RIGHTSHIFTEQUAL
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import sqlite3
import shutil
import bar



conn=sqlite3.connect("barcodes.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS BARCODES(
EAN TEXT PRIMARY KEY NOT NULL,
NAME_PL TEXT NOT NULL, 
NAME_OR TEXT,
DESC TEXT NOT NULL)
""")
# ean = '034000702459'
# namepl = "Reese's babeczki czekoladowe z masłem orzechowym"
# nameor = "Reese's peanut butter cups"
# desc = """Wyprodukowano w Meksyku dla The Hershey Company przez: Hersmex S. de R.I. de C.V.Av."""
# data_insert = (ean, namepl, nameor, desc)
# query_insert = 'INSERT INTO BARCODES values(?,?,?,?)'
# conn.execute(query_insert, data_insert)
conn.commit()
conn.close()



ean_clicked = '0'
# display_screen = 0

def DisplayForm():
    #creating window
    global display_screen
    display_screen = Tk()
    #setting width and height for window
    display_screen.geometry("800x300")
    #setting title for window
    display_screen.title("projekt 61895")
    global tree
    global SEARCH
    SEARCH = StringVar()
    #creating frame
    TopViewForm = Frame(display_screen, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(display_screen, width=300)
    LeftViewForm.pack(side=LEFT, fill=Y)
    LeftCenterViewForm = Frame(display_screen, width=300)
    LeftCenterViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(display_screen, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="Baza kodów kreskowych")
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Szukaj")
    lbl_txtsearch.pack(side=TOP, anchor=W)

    search = Entry(LeftViewForm, textvariable=SEARCH)
    search.pack(side=TOP, padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Szukaj", command=SearchRecord)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_search = Button(LeftViewForm, text="Pokaż wszystkie", command=DisplayData)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_search = Button(LeftViewForm, text="Generuj zaznaczony", command=Generate)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)

    btn_database = Button(LeftCenterViewForm, text="Eksportuj", command=ExportDb)
    btn_database.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_database = Button(LeftCenterViewForm, text="Importuj", command=ImportDb)
    btn_database.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_database = Button(LeftCenterViewForm, text="Dodaj kod", command=AddData)
    btn_database.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_database = Button(LeftCenterViewForm, text="Usuń zaznaczony", command=RemoveData)
    btn_database.pack(side=TOP, padx=10, pady=10, fill=X)

    #setting scrollbar
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm,columns=("EAN", "Name_pl", "Name_or", "Desc"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    #setting headings for the columns
    tree.heading('EAN', text="EAN", anchor=W)
    tree.heading('Name_pl', text="Nazwa (PL)", anchor=W)
    tree.heading('Name_or', text="Nazwa (oryginał)", anchor=W)
    tree.heading('Desc', text="opis", anchor=W)
    #setting width of the columns
    tree.column('#0', stretch=NO, minwidth=0, width=14)
    tree.column('#1', stretch=NO, minwidth=0, width=80)
    tree.column('#2', stretch=NO, minwidth=0, width=80)
    tree.column('#3', stretch=NO, minwidth=0, width=150)
    tree.bind('<ButtonRelease-1>', selectItem)
    tree.pack()
    DisplayData()
#function to search data

def SearchRecord():
    #checking search text is empty or not
    if SEARCH.get() != "":
        #clearing current display data
        tree.delete(*tree.get_children())
        #open database
        conn = sqlite3.connect('barcodes.db')
        #select query with where clause
        cursor=conn.execute("SELECT * FROM BARCODES WHERE NAME_PL LIKE ?", ('%' + str(SEARCH.get()) + '%',))
        #fetch all matching records
        fetch = cursor.fetchall()
        #loop for displaying all records into GUI
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

#defining function to access data from SQLite database
def DisplayData():
    #clear current data
    tree.delete(*tree.get_children())
    # open databse
    conn = sqlite3.connect('barcodes.db')
    #select query
    cursor=conn.execute("SELECT * FROM BARCODES")
    #fetch all data from database
    fetch = cursor.fetchall()
    #loop for displaying all data in GUI
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    
def AddData():
    global display_screen
    add_screen = Toplevel(display_screen)
    add_screen.geometry("300x500")
    add_screen.title("Dodaj kod")
    ViewForm = Frame(add_screen, width=250)
    ViewForm.pack(side=TOP, fill=Y)
    lbl_add = Label(ViewForm, text="Podaj dane")
    lbl_add.pack(side=TOP, padx=10, pady=20)

    lbl_ean = Label(ViewForm, text="EAN")
    lbl_ean.pack(side=TOP, padx=10, pady=5)
    ean = Entry(ViewForm)
    ean.pack(side=TOP, padx=10, fill=X)

    lbl_namepl = Label(ViewForm, text="Nazwa pl")
    lbl_namepl.pack(side=TOP, padx=10, pady=5)
    namepl = Entry(ViewForm)
    namepl.pack(side=TOP, padx=10, fill=X)

    lbl_nameor = Label(ViewForm, text="Nazwa oryginalna")
    lbl_nameor.pack(side=TOP, padx=10, pady=5)
    nameor = Entry(ViewForm)
    nameor.pack(side=TOP, padx=10, fill=X)

    lbl_desc = Label(ViewForm, text="Opis")
    lbl_desc.pack(side=TOP, padx=10, pady=5)
    desc = Text(ViewForm, height=8)
    desc.pack(side=TOP, padx=10, fill=X)
    
    btn_add = Button(ViewForm, text="Dodaj", command=lambda:[AddEntry(ean.get(), namepl.get(),
     nameor.get(), desc.get("1.0",'end-1c')), 
     DisplayData()])
    btn_add.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_decline = Button(ViewForm, text="Wróć", command=add_screen.destroy)
    btn_decline.pack(side=TOP, padx=10, pady=10, fill=X)

def AddEntry(ean, namepl, nameor, desc):
    err = False
    if ean == '':
        messagebox.showerror("Błąd", "Pusty EAN.")
        err = True
    elif namepl == '':
        messagebox.showerror("Błąd", "Pusta nazwa pl.")
        err = True
    elif desc == '':
        messagebox.showerror("Błąd", "Pusty opis.")
        err = True
    if err == True:
        return
    elif bar.validate(ean):
        conn=sqlite3.connect("barcodes.db")
        data_insert = (ean, namepl, nameor, desc)
        query_insert = 'INSERT INTO BARCODES values(?,?,?,?)'
        conn.execute(query_insert, data_insert)
        conn.commit()
        conn.close()
        DisplayData()
    else:
        messagebox.showerror("Błąd", "Błędny EAN.")
        return
    

def RemoveData():
    global ean_clicked
    if ean_clicked != '0':
        ean_remove = ean_clicked
        remove_screen = Toplevel(display_screen)
        remove_screen.geometry("350x250")
        remove_screen.title("Na pewno?")
        ViewForm = Frame(remove_screen, width=350)
        ViewForm.pack(side=TOP, fill=Y)
        lbl_remove = Label(ViewForm, text="Czy na pewno usunąć kod {0} z bazy?".format(ean_remove))
        lbl_remove.pack(side=TOP, padx=10, pady=20)
        btn_accept = Button(ViewForm, text="Usuń", command=lambda:[RemoveEntry(ean_remove), DisplayData()])
        btn_accept.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_decline = Button(ViewForm, text="Wróć", command=remove_screen.destroy)
        btn_decline.pack(side=TOP, padx=10, pady=10, fill=X)

def RemoveEntry(ean):
    conn = sqlite3.connect('barcodes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM BARCODES WHERE EAN LIKE ?", ('%' + str(ean),))
    conn.commit()
    cursor.close()
    conn.close()

def ExportDb():
    filename = fd.asksaveasfilename(filetypes=[("Baza danych sqlite","*.db")], defaultextension = "*.db")
    if filename:
        shutil.copy('barcodes.db',filename)

def ImportDb():
    filename = fd.askopenfilename(filetypes=[("Baza danych sqlite","*.db")], defaultextension = "*.db")
    if filename:
        shutil.copy(filename,'barcodes.db')
    DisplayData()

def Generate():
    if ean_clicked == '0':
        return
    ean = ean_clicked
    gen_screen = Toplevel(display_screen)
    gen_screen.geometry("250x250")
    gen_screen.title("Wygeneruj etykietę")
    dimstring = StringVar(gen_screen)
    barbool = BooleanVar(gen_screen)
    dimensions = ['100x150',
    '90x70',
    '90x55',
    '70x50']
    for value in dimensions:
        Radiobutton(gen_screen, text=value, variable=dimstring, padx = 20, value=value).pack(anchor=W)

    chk = ttk.Checkbutton(gen_screen, variable=barbool, text="Kod kreskowy")
    chk.pack(side=TOP, padx=10, pady=10, fill=X)

    conn = sqlite3.connect("barcodes.db")
    cursor = conn.execute("SELECT EAN, NAME_PL, DESC FROM BARCODES WHERE EAN LIKE ?", ('%' + str(ean),))
    fetch = cursor.fetchall()
    cursor.close()
    conn.close()
    for data in fetch:
        print(data)

    btn_accept = Button(gen_screen, text="Generuj", command=lambda:[bar.generate(dimstring.get(),
    barbool.get(),
    data[0],
    data[1],
    data[2]),
    DisplayData()])
    btn_accept.pack(side=TOP, padx=10, pady=10, fill=X)

def selectItem(a):
    global ean_clicked
    curItem = tree.focus()
    if isinstance(tree.item(curItem), dict):
        ean_clicked = tree.item(curItem).get('values')[0]

#calling function
DisplayForm()
if __name__=='__main__':
#Running Application
 mainloop()