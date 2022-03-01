import time

import PySimpleGUI as sg
import subprocess
import time

# key must be the same as metadata but with an added '-' at the end
column = [sg.Checkbox('OS Detection', default=False, auto_size_text=True, key='-O-', metadata='-O'),
          sg.Checkbox('OS and version detection', key='-A-', metadata='-A'),
          sg.Checkbox('T4', key='-T4-', metadata='-T4')]
column_2 = [column]
full_column = sg.Column(column_2)

layout = [[sg.Text('Enter Scan target')],
          [sg.Input(key='-INPUT-', pad=(12, 0), expand_x=True),
           sg.Button('Scan!', bind_return_key=True),
           sg.Button('Never-mind')], [full_column],
          [sg.Text(size=(90, 90), key='-OUTPUT-', auto_size_text=True, expand_y=True, expand_x=True)]]

layout[-1].append(sg.Sizegrip())
window = sg.Window('Script Kiddie Toolbox', layout, location=(1080, 50), resizable=True)


def update_output_text(field_to_update, new_text):
    window[field_to_update].update(new_text)
    window.refresh()


# process-factory.dk
def start_nmap(args):
    arg_string = ''
    for arg in args:
        arg_string += ' ' + str(arg)
    command_to_run = 'nmap' + arg_string
    update_output_text('-OUTPUT-', 'Running command: ' + command_to_run)
    sp = subprocess.run(command_to_run, shell=True, text=True, capture_output=False)

    # sp = subprocess.Popen(['nmap'] + [arg_string], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    scan_output = sp.stdout

    print(sp)


while True:
    event, values = window.read()
    myArgs = []
    if event == sg.WINDOW_CLOSED or event == 'Never-mind':
        break
    elif event == 'Scan!' or event == 'Return':
        update_output_text('-OUTPUT-', 'yo')

        for checkbox in column:
            checkbox_val = str(checkbox.metadata + '-')
            if values[checkbox_val]:
                myArgs.append(checkbox.metadata)
        myArgs.append(values['-INPUT-'])
        start_nmap(myArgs)

window.close()

# if __name__ == '__main__':
