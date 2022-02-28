import time

import PySimpleGUI as sg
import subprocess
import time


column = [sg.Checkbox('OS Detection', default=False, auto_size_text=True, key='-OS-', metadata='-O'),
          sg.Checkbox('OS and version detection', key='-A-', metadata='-A'),
           sg.Checkbox('T4', key='-T4-', metadata='-T4')]
column_2 = [column]
full_column = sg.Column(column_2)

layout = [[sg.Text('Enter Scan target')],
          [sg.Input(key='-INPUT-', pad=(12, 0), expand_x=True), sg.Button('Scan!', bind_return_key=True), sg.Button('Never-mind')],
          [full_column],
          [sg.Text(size=(90, 90), key='-OUTPUT-', auto_size_text=True, expand_y=True, expand_x=True)]]

layout[-1].append(sg.Sizegrip())
window = sg.Window('Script Kiddie Toolbox', layout, location=(1080, 50), resizable=True)


# process-factory.dk
def start_nmap(args):
    arg_string = ''
    for arg in args:
        arg_string += ' ' + str(arg)

    sp = subprocess.run(['nmap' + arg_string], shell=True, text=True, capture_output=False)
    # sp = subprocess.Popen(['nmap'] + [arg_string], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    scan_output = sp.stdout
    print(sp)
    window['-OUTPUT-'].update(sp)


while True:
    event, values = window.read()
    myArgs = []
    if event == sg.WINDOW_CLOSED or event == 'Never-mind':
        break
    elif event == 'Scan!' or event == 'Return':
        for checkbox in column:
            print(checkbox.metadata)

      #  if values['-OS-']:
      #      myArgs.append('-O')
     #       myArgs.append(values['-INPUT-'])
     #       start_nmap(myArgs)
    #    else:
    #        myArgs.append(values['-INPUT-'])
     #       start_nmap(myArgs)

# window['-OUTPUT-'].update('Starting scan')

window.close()

# if __name__ == '__main__':
