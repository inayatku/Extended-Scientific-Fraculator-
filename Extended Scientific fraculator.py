from tkinter import *
from tkinter import messagebox
from math import *
from time import *
from sympy import *
from sympy.solvers.solveset import solvify
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
root = Tk()
root.tk.call('tk', 'scaling', 1.6)
root.geometry('+200+0')
root.title("Scientific Fraculator With Extended Features")
label1 = """Memory Section: You can type values of the variables here, or press these buttons to store your last 
answer from the output screen in these variables"""
label2 = """Input Screen: Place cursor in middle line to start writing any expression or equation. 
Press tab to start entering numerator,press tab again to enter denominator then press tab to end fraction."""
memSec = LabelFrame(root, text=label1, labelanchor='n')
memSec.pack()
calcType = LabelFrame(root, text='Type of Screen Buttons', labelanchor='n')
calcType.pack()
inputscreen = LabelFrame(root, text=label2, labelanchor='n')
inputscreen.pack()
naviSec = Frame(inputscreen)
naviSec.pack(side=RIGHT)
multilineOutputScreen = LabelFrame(
    root, text="Multi-line output screen", labelanchor='n')
multilineOutputScreen.pack()
outputscreen = LabelFrame(
    root, text="Single line output screen", labelanchor='n')
outputscreen.pack()
buttonsSec = LabelFrame(root, text='Buttons', labelanchor='n')
buttonsSec.pack()
keys = []
invifact = b'\xe2\x80\x8e'.decode('UTF-8')
invicross = b'\xfe\xff'.decode('UTF-16 BE')
global cursor
def clearframe(frame):
    for widget in frame.winfo_children():
        widget.destroy()
def createnaviSec():
    btnup = Button(naviSec, text="🠝", command=lambda event=None: up(event))
    btnup.pack(ipady=1)
    btndown = Button(naviSec, text="🠟", command=lambda event=None: down(event))
    btndown.pack(side=BOTTOM, ipady=1)
    btnleft = Button(naviSec, text="🠜", command=lambda event=None: left(event))
    btnleft.pack(side=LEFT, padx=10, ipadx=5)
    btnright = Button(naviSec, text="🠞",
                      command=lambda event=None: right(event))
    btnright.pack(side=RIGHT, padx=10, ipadx=5)
    inputdisp.bind('<Up>', up)
    inputdisp.bind('<Down>', down)
    inputdisp.bind('<Left>', left)
    inputdisp.bind('<Right>', right)
def up(event):
    if int(inputdisp.index(INSERT).split('.')[1]) >= 2:
        inputdisp.see('insert-1d line')
    if int(inputdisp.index(INSERT).split('.')[0]) > 1:
        inputdisp.mark_set(INSERT, 'insert-1d line')
    return 'break'
def down(event):
    inputdisp.see('insert-1d line')
    if int(inputdisp.index(INSERT).split('.')[0]) < 3:
        inputdisp.mark_set(INSERT, 'insert+1d line')
    return 'break'
def left(event):
    if int(inputdisp.index(INSERT).split('.')[1]) >= 3:
        inputdisp.see('insert-3d char')
    if int(inputdisp.index(INSERT).split('.')[1]) > 0:
        inputdisp.mark_set(INSERT, 'insert-1d char')
    return 'break'
def right(event):
    inputdisp.see('insert+3d char')
    inputdisp.mark_set(INSERT, 'insert+1d char')
    return 'break'
def simple():
    global keys
    keys = ["𝑎²", "𝑎³", "𝑎ⁿ", "√𝑎", "𝑎⁻¹", "𝑎⁻²", "𝑎⁻³", "³√𝑎", "CE", "DEL",
            "7", "8", "9", "0", "-", "/", "ⁿCₘ", " ", "'─'", " ",
            "4", "5", "6", ".", "+", "×", " ", "d→f", "f→d", "𝑎\n─\n𝑏",
            "1", "2", "3", " ", "()", " ", " ", " ", "Compute", " "]
    createbuttonsSec()
def scientific():
    global keys
    keys = ["sin", "cos", "tan", "csc", "sec", "cot", "logₑ", "eⁿ", "CE", "DEL",
            "x", "y", "z", "𝑎²", "𝑎³", "𝑎ⁿ", "√𝑎", "𝑎⁻¹", "𝑎⁻²", "𝑎⁻³",
            "7", "8", "9", "0", "-", "/", "³√𝑎", "°", "'─'", "𝑎\n─\n𝑏",
            "4", "5", "6", ".", "+", "×", "()!", "d→f", "f→d", " ",
            "1", "2", "3", "π", "()", "Solve\nfor x", "=", ",", "∫dx", "𝜕/𝜕x",
            "×10ⁿ", " ", "ⁿCₘ", "Gamma", "Simplify 1", " ", "Simplify 2", " ", "Simplify 3", " ",
            "Factorize", " ", "Expand", " ", "Solve System\nof Equations", " ", "M-Line\nOutput→Edit", " ", "Compute", " ",
            "Trignometric\nSimplify", " ", "Combinatorial\nSimplify", " ", "Invisible\nMultiplication", "", "S-line\nOutput→Edit", "", "", ""]
    createbuttonsSec()
def createbuttonsSec():
    clearframe(naviSec)
    clearframe(buttonsSec)
    btn = []
    createnaviSec()
    for i in range(len(keys)):
        btn.append(Button(buttonsSec, bd=6, text=keys[i], font=(
            'Courier', '12', 'bold'), command=lambda i=i: func(i), width=2, height=1))
        btn[i].grid(row=i//10, column=i % 10, ipadx=25, ipady=0)
    btn[29].grid(rowspan=2, ipady=30)
    btn[39].destroy()
    for i in range(45, 54):
        btn[i].config(font=('courier', '12', 'bold'), width=6)
        btn[i].grid(ipadx=1, ipady=1)
    for i in range(54, 79, 2):
        btn[i].config(font=('courier', '12', 'bold'), width=10)
        btn[i].grid(columnspan=2)
        btn[i+1].destroy()
    btn[78].destroy()
    btn[79].destroy()
    btn[68].grid(rowspan=2, columnspan=2, ipady=26)
    inputdisp.bind('<Return>', enter)
    inputdisp.bind('<Tab>', tab)
    inputdisp.bind('<Escape>', escape)
    inputdisp.bind('<BackSpace>', backspace)
def escape(event):
    inputdisp.delete(1.0, END)
    inputdisp.insert(1.0, ' '*200+'\n'+' '*200+'\n'+' '*200+'\n')
    mlinedisp.delete(1.0, END)
    mlinedisp.insert(1.0, ' '*200+'\n'+' '*200+'\n'+' '*200+'\n')
    mlinedisp.mark_set(INSERT, 2.0)
    slinedisp.delete(0, END)
    inputdisp.mark_set(INSERT, 2.0)
    return 'break'
def safe_sympify(expression):
    try:
        result = sympify(expression)
        return result
    except Exception as e:
        return f"Error: {e}"
def enter(event):
    slinedisp.delete(0, END)
    x, y, z = symbols("x y z")
    result= safe_sympify(dispread(inputdisp))
    if "Error" in str(result):
        messagebox.showerror("Unknown Operation", "Always start typing the expression in middle (second) line of input display.\nRemember: For multiplication between variables, numbers and factors, use '*','×' or press invisible multiplication button on keypad")
    else:
        disp = result
        dispwrite(slinedisp, str(disp.subs(x, sympify(dispread(xvalue))).subs(
                y, sympify(dispread(yvalue))).subs(z, sympify(dispread(zvalue)))))
        dispresult(mlinedisp, dispread(slinedisp))
    return 'break'
def tab(event):
    dispfrac()
    return 'break'
def backspace(event):
    display = root.focus_get()
    if int(display.index(INSERT).split('.')[1]) > 0:
        display.delete('insert-1d char')
    return 'break'
def func(i):
    try:
        display = root.focus_get()
        if keys[i] == "Compute":
            enter(None)
        elif keys[i] == "CE":
            escape(None)
        elif keys[i] == "DEL":
            backspace(None)
        elif keys[i] == "𝑎²":
            display.insert(INSERT, '²')
        elif keys[i] == "𝑎³":
            display.insert(INSERT, '³')
        elif keys[i] == "𝑎⁻²":
            display.insert(INSERT, '⁻²')
        elif keys[i] == "𝑎⁻³":
            display.insert(INSERT, '⁻³')
        elif keys[i] == "√𝑎":
            display.insert(INSERT, '√()')
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "³√𝑎":
            display.insert(INSERT, "³√()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "𝑎⁻¹":
            display.insert(INSERT, '⁻¹')
        elif keys[i] == "sin":
            display.insert(INSERT, "sin()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "cos":
            display.insert(INSERT, "cos()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "tan":
            display.insert(INSERT, "tan()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "csc":
            display.insert(INSERT, "csc()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "sec":
            display.insert(INSERT, "sec()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "cot":
            display.insert(INSERT, "cot()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "Gamma":
            display.insert(INSERT, "gamma()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "logₑ":
            display.insert(INSERT, "log()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "eⁿ":
            display.insert(INSERT, "e^()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "()":
            display.insert(INSERT, "()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "()!":
            display.insert(INSERT, invifact+"()!")
            display.mark_set(INSERT, 'insert-2d char')
        elif keys[i] == "𝑎ⁿ":
            display.insert(INSERT, "^()")
            display.mark_set(INSERT, 'insert-1d char')
        elif keys[i] == "×10ⁿ":
            display.insert(INSERT, "×10^()")
            display.mark_set(INSERT, 'insert-1d char')
    #    elif keys[i]=="Rand#": None
        elif keys[i] == "Invisible\nMultiplication":
            display.insert(INSERT, invicross)
        elif keys[i] == "x":
            display.insert(INSERT, "x")
        elif keys[i] == "y":
            display.insert(INSERT, "y")
        elif keys[i] == "z":
            display.insert(INSERT, "z")
    #    elif keys[i]=="save":displines(inputdisp)
        elif keys[i] == "𝑎\n─\n𝑏":
            tab(None)
        elif keys[i] == "'─'":
            if inputdisp.index(INSERT).split('.')[0] == '1' and inputdisp.index(INSERT).split('.')[1] == '0':
                inputdisp.insert(INSERT+'+1d line', '─')
            elif inputdisp.index(INSERT).split('.')[0] == '3' and inputdisp.index(INSERT).split('.')[1] == '0':
                inputdisp.insert(INSERT+'-1d line', '─')
            elif inputdisp.index(INSERT).split('.')[0] == '1' and int(inputdisp.index(INSERT).split('.')[1]) > 0:
                inputdisp.insert(INSERT+'+1d line-1d char', '─')
            elif inputdisp.index(INSERT).split('.')[0] == '3' and int(inputdisp.index(INSERT).split('.')[1]) > 0:
                inputdisp.insert(INSERT+'-1d line-1d char', '─')
            else:
                inputdisp.insert(INSERT, '─')
        elif keys[i] == "d→f":
            try:
                s1 = sympify(dispread(slinedisp))
                slinedisp.delete(0, END)
                slinedisp.insert(END, Rational(s1).limit_denominator(1000000))
                dispresult(mlinedisp, dispread(slinedisp))
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Evaluate an expression first. Output screen should show a number.\n\n"+f"Error:{e}")
        elif keys[i] == "f→d":
            try:    
                s2 = sympify(dispread(slinedisp))
                slinedisp.delete(0, END)
                slinedisp.insert(END, round(s2.evalf(), 10))
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Evaluate an expression first. Output screen should show a number.\n\n"+f"Error:{e}")    
        elif keys[i] == "ⁿCₘ":
            display.insert(INSERT, "comb(,)")
            display.mark_set(INSERT, 'insert-2d char')
        elif keys[i] == "Expand":
            try:
                slinedisp.delete(0, END)
                x, y, z = symbols("x y z")
                dispwrite(slinedisp, str(expand(dispread(inputdisp))))
                dispresult(mlinedisp, dispread(slinedisp))
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Enter an expression first.\n\n"+f"Error:{e}")
        elif keys[i] == "Factorize":
            try:
                slinedisp.delete(0, END)
                x, y, z = symbols("x y z")
                dispwrite(slinedisp, str(factor(dispread(inputdisp))))
                dispresult(mlinedisp, dispread(slinedisp))
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Enter an expression first.\n\n"+f"Error:{e}")
        elif keys[i] == "Trignometric\nSimplify":
            try:
                slinedisp.delete(0, END)
                x, y, z = symbols("x y z")
                dispwrite(slinedisp, str(trigsimp(dispread(inputdisp))))
                dispresult(mlinedisp, dispread(slinedisp))
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Enter an expression first.\n\n"+f"Error:{e}")
        elif keys[i] == "∫dx":
            slinedisp.delete(0, END)
            x, y, z = symbols("x y z")
            try:
                dispwrite(slinedisp, str(integrate(dispread(inputdisp), x)))
                dispresult(mlinedisp, dispread(slinedisp))
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Enter expression first, then press ∫dx\n\n"+f"Error:{e}")
        elif keys[i] == "𝜕/𝜕x":
            slinedisp.delete(0, END)
            x, y, z = symbols("x y z")
            try:
                dispwrite(slinedisp, str(diff(dispread(inputdisp), x)))
                dispresult(mlinedisp, dispread(slinedisp))
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Enter expression first, then press 𝜕/𝜕x\n\n"+f"Error:{e}")
        elif keys[i] == "M-Line\nOutput→Edit":
            s = mlinedisp.get('1.0', END)
            if len(s.strip())!=0:
                escape(None)
                inputdisp.insert(1.0, s)
                inputdisp.mark_set(INSERT, 'insert+4d char')
            else:
                messagebox.showerror("Redundant Operation", "Multi-line output screen might be empty")
        elif keys[i] == "Simplify 1":
            try:
                slinedisp.delete(0, END)
                x, y, z = symbols("x y z")
                dispwrite(slinedisp, str(sympify(dispread(inputdisp))))
                dispresult(mlinedisp, dispread(slinedisp))
            except Exception as e:
                messagebox.showerror("Invalid Expression", "Enter a valid expression.\n\n"+f"Error:{e}")
        elif keys[i] == "Simplify 2":
            try:
                slinedisp.delete(0, END)
                x, y, z = symbols("x y z")
                dispwrite(slinedisp, str(cancel(dispread(inputdisp))))
                dispresult(mlinedisp, dispread(slinedisp))
            except Exception as e:
                messagebox.showerror("Invalid Expression", "Enter a valid expression to simplify.\n\n"+f"Error:{e}")    
        elif keys[i] == "Simplify 3":
            try:
                slinedisp.delete(0, END)
                x, y, z = symbols("x y z")
                dispwrite(slinedisp, str(simplify(dispread(inputdisp))))
                dispresult(mlinedisp, str(dispread(slinedisp)))
            except Exception as e:
                messagebox.showerror("Invalid Expression", "Enter a valid expression to simplify.\n\n"+f"Error:{e}")
        elif keys[i] == "Solve\nfor x":
            slinedisp.delete(0, END)
            x, y, z = symbols("x y z")
            try: 
                eq = dispread(inputdisp).split('=', 1)
                if len(eq) == 1:
                    eq = sympify(eq)
                    equ = eq[0]
                    dispwrite(slinedisp, str(solvify(equ, x, Complexes)))
                elif len(eq) == 2:
                    eq = sympify(eq)
                    equ = Eq(eq[0], eq[1])
                    dispwrite(slinedisp, str(solvify(equ, x, Complexes)))
                else:
                    dispwrite(slinedisp, "Error!! Incorrect Equation Format")
                    dispresult(mlinedisp, dispread(slinedisp), 1)
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Enter an equation or expression first.\nAn expression would be automatically coverted to homogeneous equation by setting itself equal to zero.\n\n"+f"Error:{e}")
        elif keys[i] == "Combinatorial\nSimplify":
            try:
                slinedisp.delete(0, END)
                x, y, z = symbols("x y z")
                dispwrite(slinedisp, str(combsimp(sympify(dispread(inputdisp)))))
                dispresult(mlinedisp, dispread(slinedisp))
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Enter an expression first.\n\n"+str(e))
        elif keys[i] == "S-line\nOutput→Edit":
            s = slinedisp.get()
            if len(s)!=0:
                escape(None)
                s = s.strip('[').strip(']')
                inputdisp.insert(2.0, s)
                inputdisp.mark_set(INSERT, 'insert+2d char')
            else:
                messagebox.showerror("Invalid Operation", "Single line output screen might be empty")
        elif keys[i] == "Solve System\nof Equations":
            slinedisp.delete(0, END)
            x, y, z = symbols("x y z")
            eq = dispread(inputdisp).split(',')
            memSec = []
            try:
                if eq[0].find('=') == -1:
                    eq = sympify(eq)
                    for i in range(len(eq)):
                        memSec.append(eq[i].free_symbols)
                else:
                    for i in range(len(eq)):
                        eq[i] = (eq[i].split('=')[0], eq[i].split('=')[1])
                        eq[i] = sympify(eq[i])
                        eq[i] = Eq(eq[i][0], eq[i][1])
                        memSec.append(eq[i].free_symbols)
                    dispwrite(slinedisp, str(solve(eq, set().union(*memSec))).replace(':', ' = '))
                    dispresult(mlinedisp, dispread(slinedisp).replace(':', ' = '), 1)
            except Exception as e:
                messagebox.showerror("Invalid Operation", "Enter collection of equations or expressions seperated by commas first.\nA collection of expressions would be automatically coverted to collection of homogeneous equations by setting themselves equal to zero.\n\n"+f"Error:{e}")
        else:
            inputdisp.insert(INSERT, keys[i])
    except Exception as e:
                messagebox.showerror("Invalid Operation","It might be error in the expression\n\n"+f"Error:{e}")

def cubrt(x):
    return x**(1/3)
def send(v):
    # read the output screen and assign that output to variable v
    if v == 'x':
        x = slinedisp.get()
        xvalue.delete(0, END)
        xvalue.insert(END, x)
    elif v == 'y':
        y = slinedisp.get()
        yvalue.delete(0, END)
        yvalue.insert(END, y)
    elif v == 'z':
        z = slinedisp.get()
        zvalue.delete(0, END)
        zvalue.insert(END, z)
def dispread(display):
    # reads the display string and convert it into python notations
    if display == inputdisp:
        # if display is input display then first convert it into string
        dispr = displines(inputdisp)
    else:
        dispr = display.get()
    dispr = dispr.replace('^', '**')
    dispr = (dispr).replace('comb', 'binomial')
    dispr = (dispr).replace('π', 'pi')
    dispr = (dispr).replace("×", '*')
    dispr = (dispr).replace("³√", "cubrt")
    dispr = (dispr).replace("√", 'sqrt')
    dispr = (dispr).replace(invicross, '*')
    dispr = (dispr).replace(invifact, 'factorial')
    dispr = (dispr).replace('!', '')
    dispr = (dispr).replace("°", '*pi/180')
    dispr = (dispr).replace("sin⁻¹", 'asin')
    dispr = (dispr).replace("cos⁻¹", 'acos')
    dispr = (dispr).replace("tan⁻¹", 'atan')
    dispr = (dispr).replace("csc⁻¹", 'acsc')
    dispr = (dispr).replace("sec⁻¹", 'asec')
    dispr = (dispr).replace("cot⁻¹", 'acot')
    dispr = (dispr).replace("⁻¹", '**(-1)')
    dispr = (dispr).replace("⁻²", '**(-2)')
    dispr = (dispr).replace("⁻³", '**(-3)')
    dispr = (dispr).replace("²", '**2')
    dispr = (dispr).replace("³", '**3')
    return dispr
    
def displines(display):     
    # read lines of input display and convert it to a string
    strexp = ''
    line = display.get('1.0', END).splitlines()
    while len(line[1].split('─', 1)) != 1:
        strexp += line[1].split('─', 1)[0]
        line[1] = line[1].split('─', 1)[1]
        line[1] = line[1].lstrip('─')
        line[0] = line[0].lstrip()
        line[2] = line[2].lstrip()
        strexp += '('+line[0].split('  ', 1)[0] + \
            ')/('+line[2].split('  ', 1)[0]+')'
        line[0] = line[0].split('  ', 1)[1]
        line[2] = line[2].split('  ', 1)[1]
    strexp += line[1].rstrip()
    return strexp
def dispfrac():
# this function executes when we press tab. and it starts writing fraction when current location is line 1. it go
# to line 0 then if we press it again it go to line 2 and then it go to line 1.
    global cursor, length
    if inputdisp.index(INSERT).split('.')[0] == '2':
        cursor = inputdisp.index(INSERT)
        inputdisp.mark_set(INSERT, cursor+'-1d line+2d char')
    elif inputdisp.index(INSERT).split('.')[0] == '1':
        s1 = inputdisp.get(cursor+'-1d line+2d char', 'insert')
        n = len(s1)
        length = n
        inputdisp.delete(cursor, cursor+'+'+str(length+3)+'d char')
        inputdisp.insert(cursor+'+1d char', "─"*(length+2))
        inputdisp.mark_set(INSERT, cursor+'+1d line+2d char')
    elif inputdisp.index(INSERT).split('.')[0] == '3':
        s2 = inputdisp.get(cursor+'+1d line+2d char', 'insert')
        d = len(s2)
        if d > length:
            length = d
        numerator = inputdisp.get(
            cursor+'-1d line+2d char', cursor+'-1d line'+'+'+str(length+2)+'d char').strip()
        denominator = inputdisp.get(
            cursor+'+1d line+2d char', cursor+'+1d line'+'+'+str(length+2)+'d char').strip()
        printfrac(inputdisp, cursor, numerator, denominator)
def printfrac(display, loc, num, den):
# writes a fraction on display at location loc
    nlen = len(num)
    invinlen = num.count(invicross)+num.count(invifact)
    rnlen = nlen-invinlen
    dlen = len(den)
    invidlen = den.count(invicross)+den.count(invifact)
    rdlen = dlen-invidlen
    rlen = rnlen
    tlen = nlen
    if rdlen > rlen:
        rlen = rdlen
    if dlen > nlen:
        tlen = dlen
    display.delete(loc+'-1d line', loc+'-1d line'+'+'+str(tlen+3)+'d char')
    display.delete(loc, loc+'+'+str(tlen+3)+'d char')
    display.delete(loc+'+1d line', loc+'+1d line'+'+'+str(tlen+3)+'d char')
    if nlen > dlen:
        num = num.center(tlen+2)
        den = den.center(rlen+2)
    elif dlen > nlen:
        num = num.center(rlen+2)
        den = den.center(tlen+2)
    else:
        num = num.center(tlen+2)
        den = den.center(tlen+2)
    display.insert(loc+'-1d line+1d char', num)
    display.insert(loc+'+1d char', "─"*(rlen+2))
    display.insert(loc+'+1d line+1d char', den)
    display.mark_set(INSERT, loc+'+'+str(rlen+4)+'d char')
def dispresult(display, equstr, solve=0):
    mlinedisp.delete(1.0, END)
    mlinedisp.insert(1.0, ' '*200+'\n'+' '*200+'\n'+' '*200+'\n')
    mlinedisp.mark_set(INSERT, 2.0)
    equstr = convert(equstr)
    if solve == 1:
        equstr = equstr[1:-1]
        equstr = equstr.replace('I', 'i')
    splitstr = list(equstr)
    for i in range(2):
        splitstr.append(" ")
    i = 0
    while i < len(splitstr)-2:
        count = 0
        while splitstr[i] != '(':
            if splitstr[i] == '-' or splitstr[i] == '+' or splitstr[i] == '/' or splitstr[i] == ',' or splitstr[i] == '=':
                splitstr.insert(i, '@')
                splitstr.insert(i+2, '@')
                i += 2
            else:
                i += 1
            if i >= len(splitstr)-2:
                break
        count = 1
        while count != 0:
            i += 1
            if splitstr[i] == '(':
                count += 1
            if splitstr[i] == ')':
                count -= 1
            if i >= len(splitstr)-2:
                break
        i += 1
        if i >= len(splitstr)-2:
            break
    equstr = ""
    equstr = equstr.join(splitstr)
    equstr = equstr.split("@")
    for i in range(len(equstr)):
        if equstr[i] == '/':
            equstr.pop(i)
            equstr.insert(i-1, '/')
    j = 0
    display.mark_set(INSERT, '2.0')
    if solve == 1:
        display.insert(INSERT, '{')
    for i in range(len(equstr)):
        if equstr[i] == '/':
            j = i
            equstr[j+1] = equstr[j+1].strip()
            equstr[j+2] = equstr[j+2].strip()
            printfrac(display, INSERT, equstr[j+1], equstr[j+2])
            j += 3
        if i == j:
            display.insert(INSERT, equstr[i])
            j = i
            j += 1
    if solve == 1:
        display.insert(INSERT, '}')
    display.mark_set(INSERT, '2.0')
def dispwrite(display, dispw):
# write the output string to display
    dispw = convert(dispw)
    dispw = display.insert(END, dispw)
def convert(dispw):
# convert python output to user friendly output
    dispw = dispw.replace('**2', "²")
    dispw = (dispw).replace('**3', "³")
    dispw = (dispw).replace('**(-1)', "⁻¹")
    dispw = (dispw).replace('**(-2)', "⁻²")
    dispw = (dispw).replace('**(-3)', "⁻³")
    dispw = dispw.replace('**', '^')
    dispw = (dispw).replace('pi', 'π')
    dispw = (dispw).replace('*pi/180', "°")
    dispw = (dispw).replace('*', "×")
    dispw = (dispw).replace('sqrt', "√")
    dispw = (dispw).replace('asin', "sin⁻¹")
    dispw = (dispw).replace('acos', "cos⁻¹")
    dispw = (dispw).replace('atan', "tan⁻¹")
    dispw = dispw.replace(" ", "")
    dispw = dispw.replace("×", invicross)
    return (dispw)
Button(memSec, text="𝑥 =", font=('Courier', '15', 'bold'),
       command=lambda: send('x')).grid(row=0, column=0)
xvalue = Entry(memSec, bd=6, justify=RIGHT, font=(
    'Courier', '15', 'bold'), width=10)
xvalue.grid(row=0, column=1)
xvalue.insert(END, 'x')
Button(memSec, text="𝑦 =", font=('Courier', '15', 'bold'),
       command=lambda: send('y')).grid(row=0, column=2)
yvalue = Entry(memSec, bd=6, justify=RIGHT, font=(
    'Courier', '15', 'bold'), width=10)
yvalue.grid(row=0, column=3)
yvalue.insert(END, 'y')
Button(memSec, text="𝑧 =", font=('Courier', '15', 'bold'),
       command=lambda: send('z')).grid(row=0, column=4)
zvalue = Entry(memSec, bd=6, justify=RIGHT, font=('Courier', '15', 'bold'), 
                width=10)
zvalue.grid(row=0, column=5)
zvalue.insert(END, 'z')
inputdisp = Text(inputscreen, bd=4, font=('Courier New', '15', 'bold'), 
                 height=3, width=50, wrap='none',insertwidth=15)
                # ,spacing1=0, spacing3=0)
inputdisp.pack()
sbh1 = Scrollbar(inputscreen, orient=HORIZONTAL,
                 command=inputdisp.xview, width=12)
inputdisp.config(xscrollcommand=sbh1.set)
sbh1.pack(fill=X)
cursor = inputdisp.index(INSERT)
mlinedisp = Text(multilineOutputScreen, bd=2, font=('Courier New', '15', 'bold'),
                 height=3, width=70, wrap='none', cursor='arrow', relief=SUNKEN, bg='light grey')
mlinedisp.pack()
sbh2 = Scrollbar(multilineOutputScreen, orient=HORIZONTAL,
                 command=mlinedisp.xview, width=12)
mlinedisp.config(xscrollcommand=sbh2.set)
sbh2.pack(fill=X)
slinedisp = Entry(outputscreen, justify=RIGHT, bd=2, font=(
    'Courier', '12', 'bold'), width=60, bg='light grey')
slinedisp.grid(row=0, column=0, columnspan=2)
inputdisp.focus_set()
escape(None)
scientific()
Button(calcType, text="Simple Calculator", command=simple).pack(side=LEFT)
Button(calcType, text="Scientific Calculator",
       command=scientific).pack(side=LEFT)
root.mainloop()
