#!/usr/bin/env python

import PySimpleGUI as sg
import subprocess
import email_scraper as es
import threading


def start_nmap(arguments):
    command_to_run = 'nmap' + arguments
    es.update_output_text(window=my_ui.window, field_to_update='-OUTPUT-',
                          new_text='Running command: ' + command_to_run)
    # sg.popup(command_to_run, keep_on_top=False)
    sp = subprocess.run(command_to_run, shell=True, text=True, capture_output=False)
    # sp = subprocess.Popen(['nmap'] + [arg_string], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    scan_output = sp.stdout

    print(sp)


def do_scrape(val):
    es.reset_scrape_flag()
    es.scrape_emails(target=val['-INPUT-'], window=my_ui.window)


def do_scan(val):
    args = get_scan_args() + ' ' + val['-INPUT-']
    start_nmap(args)


class UILayout:
    go_button = sg.Button('Scan!', bind_return_key=True, key='-GO-')
    cross_tab_layout = [[[sg.Text('Enter target', font='15')], sg.Input(key='-INPUT-', pad=(8, 0), expand_x=False),
                         go_button, sg.Button('Never-mind')]]
    # key must be the same as metadata
    column = [[sg.Checkbox('OS Detection', default=False, auto_size_text=True, key='-O', metadata='-O'),
               sg.Checkbox('OS and version detection', key='-A', metadata='-A'),
               sg.Checkbox('T4', key='-T4', metadata='-T4'),
               sg.Checkbox('Treat all hosts as online', key='-Pn', metadata='-Pn')],
              [sg.Checkbox('Fast mode', key='-F', metadata='-F')]]

    output_column = [[sg.Column([[sg.Output(size=(90, 90), key='-OUTPUT-', expand_y=True, expand_x=True)]],
                                expand_x=True, expand_y=True)]]
    scan_tab = [[sg.Column(column)]]
    scrape_tab = [[sg.Text('Scrape emails.... or don\'t. im not your mom')]]
    layout = cross_tab_layout
    tabs = [[sg.Tab('Scanning (nmap)', scan_tab, key='-SCAN_TAB-', metadata=('-SCAN_TAB-', do_scan))],
            [sg.Tab('Web scraping', scrape_tab, key='-SCRAPE_TAB-', metadata=('-SCRAPE_TAB-', do_scrape))]]
    my_tab_group = sg.TabGroup(tabs, key='-TAB_GROUP-', enable_events=True)
    layout += [[my_tab_group]]
    layout += output_column
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Script Kiddie Toolbox', layout, location=(1050, 300), resizable=True, size=(1000, 550))

    # process-factory.dk


def get_scan_args():
    arg_string = ''
    for i in range(0, len(my_ui.column)):
        for checkbox in my_ui.column[i]:
            if values[checkbox.metadata]:
                arg_string += ' ' + checkbox.metadata
    return arg_string


def change_go_button_text():
    if values[event] is not None:
        my_text = str(values[event])
        update_text = my_text[1:my_text.find('_')]
        update_text = update_text[0:1] + update_text[1:].lower() + '!'
        my_ui.go_button.update(text=update_text)


def dict_setup():
    for tab in my_ui.tabs:
        for t in tab:
            key = t.metadata[0]
            k_val = t.metadata[1]
            my_dict[key] = k_val


if __name__ == '__main__':
    my_dict = {}
    my_ui = UILayout()
    dict_setup()
    current_tab = ''
    t1 = threading

    while True:
        # print(es.EmailScraper.ting)
        event, values = my_ui.window.read()
        if event == sg.WINDOW_CLOSED:  # or event == 'Never-mind':
            break
        elif event == 'Scan!' or event == 'Return' or event == '-GO-':
            my_ui.yes_no = True
            function_to_execute = my_dict[my_ui.my_tab_group.Get()]
            global func
            func = my_ui.window.perform_long_operation(lambda: function_to_execute(values), '-END_KEY-')
        elif event == 'Never-mind':
            func.join(0.2)
            es.stop_scrape()
        else:
            change_go_button_text()

    my_ui.window.close()
