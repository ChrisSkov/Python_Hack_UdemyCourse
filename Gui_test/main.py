#!/usr/bin/env python

import PySimpleGUI as sg
import subprocess
import email_scraper as es


def start_nmap(arguments):
    command_to_run = 'nmap' + arguments
    es.update_output_text(window=my_ui.window, field_to_update='-OUTPUT-',
                          new_text='Running command: ' + command_to_run)
    # sg.popup(command_to_run, keep_on_top=False)
    sp = subprocess.run(command_to_run, shell=True, text=True, capture_output=False)

    # sp = subprocess.Popen(['nmap'] + [arg_string], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    scan_output = sp.stdout

    print(sp)


class UITing:
    do_scrape = False

    # key must be the same as metadata
    column = [[sg.Checkbox('OS Detection', default=False, auto_size_text=True, key='-O', metadata='-O'),
               sg.Checkbox('OS and version detection', key='-A', metadata='-A'),
               sg.Checkbox('T4', key='-T4', metadata='-T4'),
               sg.Checkbox('Treat all hosts as online', key='-Pn', metadata='-Pn')],
              [sg.Checkbox('Fast mode', key='-F', metadata='-F')]]

    mini_column = [sg.Text(size=(150, 290), key='-OUTPUT-', auto_size_text=True, expand_y=True, expand_x=True)]
    full_column = sg.Column(column)

    little_column = sg.Column([mini_column], scrollable=True, vertical_scroll_only=True, expand_x=True)

    cross_tab_layout = [[[sg.Text('Enter target', font='15')], sg.Input(key='-INPUT-', pad=(8, 0), expand_x=False),
                         sg.Button('Never-mind')]]

    scan_tab = [[full_column], [sg.Button('Scan!', bind_return_key=True)], [little_column]]
    scrape_tab = [[sg.Button('Scrape emails')]]
    layout = cross_tab_layout
    layout += [[sg.TabGroup([
        [sg.Tab('Scan tings', scan_tab, key='-SCAN_TAB-')],
        [sg.Tab('Scrape tings', scrape_tab, key='-SCRAPE_TAB-')]],
        key='-TAB_GROUP-', enable_events=True)]]

    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Script Kiddie Toolbox', layout, location=(1050, 300), resizable=True, size=(1000, 550))

    # process-factory.dk


def get_scan_args():
    arg_string = ''
    for i in range(0, len(my_ui.column)):
        for checkbox in my_ui.column[i]:
            # checkbox_val = str(checkbox.metadata + '-')
            if values[checkbox.metadata]:
                arg_string += ' ' + checkbox.metadata
    return arg_string


if __name__ == '__main__':
    my_ui = UITing()
    while True:
        event, values = my_ui.window.read()
       # print(values[event])
        if event == sg.WINDOW_CLOSED or event == 'Never-mind':
            break
        elif event == 'Scan!' or event == 'Return':
            args = get_scan_args()
            args += ' ' + values['-INPUT-']
            start_nmap(args)
        elif event == 'Scrape emails':
            scrape_me = es.EmailScraper()
            es.EmailScraper.scrape_emails(self=scrape_me, target=values['-INPUT-'], window=my_ui.window)
            # res = scraper.scrape_emails(values['-INPUT-'])
            # my_ui.update_output_text('-OUTPUT-', res)
    my_ui.window.close()
