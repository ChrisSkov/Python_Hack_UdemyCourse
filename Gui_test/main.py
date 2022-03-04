#!/usr/bin/env python

import PySimpleGUI as sg
import subprocess
import email_scraper as es


def start_nmap(args):
    command_to_run = 'nmap' + args
    es.update_output_text(window=my_ui.window, field_to_update='-OUTPUT-',
                          new_text='Running command: ' + command_to_run)
    sp = subprocess.run(command_to_run, shell=True, text=True, capture_output=False)

    # sp = subprocess.Popen(['nmap'] + [arg_string], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    scan_output = sp.stdout

    print(sp)


class UITing:
    do_scrape = False

    # key must be the same as metadata but with an added '-' at the end
    column = [[sg.Checkbox('OS Detection', default=False, auto_size_text=True, key='-O-', metadata='-O'),
               sg.Checkbox('OS and version detection', key='-A-', metadata='-A'),
               sg.Checkbox('T4', key='-T4-', metadata='-T4'),
               sg.Checkbox('Treat all hosts as online', key='-Pn-', metadata='-Pn')],
              [sg.Checkbox('Fast mode', key='-F-', metadata='-F')]]

    mini_column = [[sg.Text(size=(150, 290), key='-OUTPUT-', auto_size_text=True, expand_y=True, expand_x=True)]]

    full_column = sg.Column(column)
    little_column = sg.Column(mini_column, scrollable=True, vertical_scroll_only=True, expand_x=True)

    layout = [[sg.Text('Enter Scan target')],
              [sg.Input(key='-INPUT-', pad=(12, 0), expand_x=True),
               sg.Button('Scan!', bind_return_key=True),
               sg.Button('Scrape emails'),
               sg.Button('Never-mind')], [full_column], [little_column]]

    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Script Kiddie Toolbox', layout, location=(1050, 300), resizable=True, size=(1000, 550))

    # process-factory.dk


if __name__ == '__main__':
    my_ui = UITing()
    while True:
        event, values = my_ui.window.read()
        if event == sg.WINDOW_CLOSED or event == 'Never-mind':
            break
        elif event == 'Scan!' or event == 'Return':
            es.update_output_text(window=my_ui.window, field_to_update='-OUTPUT-', new_text='yo')
            arg_string = ''
            for i in range(0, len(my_ui.column)):
                for checkbox in my_ui.column[i]:
                    checkbox_val = str(checkbox.metadata + '-')
                    if values[checkbox_val]:
                        arg_string += ' ' + checkbox.metadata
                        arg_string += ' ' + values['-INPUT-']
            start_nmap(arg_string)
        elif event == 'Scrape emails':
            scrape_me = es.EmailScraper()
            es.EmailScraper.scrape_emails(self=scrape_me, target=values['-INPUT-'], window=my_ui.window)
            # res = scraper.scrape_emails(values['-INPUT-'])
            # my_ui.update_output_text('-OUTPUT-', res)
    my_ui.window.close()
