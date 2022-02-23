import time

import PySimpleGUI as sg
import subprocess
import time

layout = [[sg.Text('Enter Scan target')],
          [sg.Input(key='-INPUT-', pad=(12, 0)), sg.Button('Scan!', bind_return_key=True), sg.Button('Never-mind')],
          [sg.Checkbox('OS Detection', default=False, auto_size_text=True)],
          [sg.Text(size=(50, 60), key='-OUTPUT-', auto_size_text=True, expand_y=True, expand_x=True)]]

layout[-1].append(sg.Sizegrip())

window = sg.Window('Script Kiddie Toolbox', layout, location=(1080, 50), resizable=True)


# process-factory.dk
def start_nmap(args):
    # arg_string = ''
    # for arg in args:
    #   arg_string += ' ' + str(arg)

    sp = subprocess.run(['nmap' + ' ' + str(args)], shell=True, text=True)# capture_output=True, text=True)
    # sp = subprocess.Popen(['nmap'] + [arg_string], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    scan_output = sp.stdout
    print(sp)
    window['-OUTPUT-'].update(scan_output)


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Never-mind':
        break
    elif event == 'Scan!' or event == 'Return':
        start_nmap(values['-INPUT-'])

# window['-OUTPUT-'].update('Starting scan')

window.close()

# if __name__ == '__main__':
