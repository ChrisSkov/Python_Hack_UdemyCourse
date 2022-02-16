import subprocess
import tkinter as tk


def eow(ting):
    print(ting.get())


print('starting window')
window = tk.Tk()
window.title('Script kiddie toolbox')
window.geometry('300x300')
greeting = tk.Label(window, text='Hi there, hello')
greeting.pack()
target_field = tk.Entry(window)
target_field.insert(1,'Enter target here')
target_field.pack()
start_scan_btt = tk.Button(window, text='Start scan', command=lambda tf=target_field: eow(tf))
start_scan_btt.pack()

window.mainloop()


def start_nmap(target):
    cmd = 'nmap'

    temp = subprocess.Popen([cmd, target])
    out = str(temp.communicate())
    print(out)

# if __name__ == '__main__':
#   setup()
#  start_nmap('192.168.88.132')
