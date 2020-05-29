import PySimpleGUI as sg
from sim import *

layout = [[sg.Text('Simulating Infectious Diseases', font=('Times New Roman', 20))],
          [sg.Text('Name your disease: '), sg.InputText(key='name')],    
          [sg.Text('Population', size=(20, 1)), sg.Slider(range=(20, 150), size=(20, 10), orientation='horizontal', default_value=50, key='population')],   
          [sg.Text('Transmission Rate (%)', size=(20, 1)), sg.Slider(range=(1, 100), size=(20, 10), orientation='horizontal', default_value=100, key='trans')],
          [sg.Text('Death Rate (%)', size=(20, 1)), sg.Slider(range=(1, 100), size=(20, 10), orientation='horizontal', default_value=0, key='death')],
          [sg.Text('Infection Duration (Days)', size=(20, 1)), sg.Slider(range=(1, 24), size=(20, 10), orientation='horizontal', default_value=7, key='duration')],
          [sg.Text('Social Distancing (%)', size=(20, 1)), sg.Slider(range=(0, 100), size=(20, 10), orientation='horizontal', default_value=0, key='sd')],
          [sg.Button('Simulate')]]      

window = sg.Window('Simulating Infectious Diseases', layout)    

event, values = window.read()    
window.close()

main(Disease(str(values['name']), values['trans'], int(values['death']), int(values['duration']), int(values['population'])), Environment(int(values['population']), int(values['sd'])))
