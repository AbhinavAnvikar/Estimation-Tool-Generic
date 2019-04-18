from tkinter import *
from PIL import ImageTk,Image

cnt=0

def foo(FirstLB,SecondLB,lb):
    global cnt
    message=""
    cnt+=1
    str1 = str(FirstLB.get(ACTIVE)) +" | "+ str(SecondLB.get(ACTIVE))
    message = "Success - " +str1
    lb.insert(cnt,str1)

    #messagebox.showinfo('Test',message)

def clear_list(lb):
    try:
        str = lb.curselection()
        lb.delete(str)
    except:
        pass

def createGUI():
    master = Tk()
    master.title("Estimation Tool")
    master.geometry("300x400")

    Label(master, text="Complexity (Level 1)   ", height=4).grid(row=0, column=0)
    FirstLBSelect = ["Simple", "Medium", "Complex"]
    FirstLB = Listbox(master, selectmode='single', exportselection=0, height=5, width=20)
    FirstLB.insert(END, *FirstLBSelect)
    FirstLB.grid(row=0, column=1)
    # e1.insert(1,"Simple")
    # e1.insert(2,"Medium")
    # e1.insert(3,"Complex")

    Label(master, text="Complexity (Level 2)   ").grid(row=1, column=0)
    SecondLBSelect = ["1", "2", "3", "4", "5"]
    SecondLB = Listbox(master, exportselection=0, height=6, width=20)
    SecondLB.insert(END, *SecondLBSelect)
    SecondLB.grid(row=1, column=1)
    lb = Listbox(master, height=10, width=20)
    lb.grid(row=3, column=1)
    btn_Calc = Button(master, text="Calculate LOE", command=foo(FirstLB,SecondLB,lb))
    btn_Calc.grid(row=2, column=0)
    btn_clear = Button(master, text="Clear List", command=clear_list(lb))
    btn_clear.grid(row=2, column=1)
    mainloop()

createGUI()


# image = Image.open("math.jpg")
# image = image.resize((200,200),Image.ANTIALIAS)
# img = ImageTk.PhotoImage(image)


# e2.insert(1,"1")
# e2.insert(2,"2")
# e2.insert(3,"3")
# e2.insert(4,"4")
# e2.insert(5,"5")

