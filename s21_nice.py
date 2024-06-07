# Python
import glob
import plotly.express as px
import os
import pandas as pd
from nicegui import ui
from tkinter import filedialog
from tkinter import filedialog, Tk

PATH_TO_LOGO = './assets/ljungtechlogo.png'

class DataParams():
    def __init__(self) -> None:
        self.plotly_theme = 'plotly'
        self.data_folder = None
        self.data_files = None
        self.norm_folder = None
        self.norm_file = None

def import_data_and_graph(
        files_path: str
        ) -> None:
    
    # All file names to a list
    all_files = glob.glob(os.path.join(files_path, "*.prn"))
    # Column name in dataframe
    column_names = ['freq', 'dB', 'r']
    data_frames = []
    # print('Parsing data, please wait...')
    for file in all_files:
        df = pd.read_csv(file, header=None, names=column_names)
        # Removes first two rows
        df = df.drop(index=[0, 1])
        # Removes extra column that is created due to csv format (ends with a ',' so importing creates an empty column)
        df = df.drop('r', axis=1)
        df = df.reset_index()
        # Converts the data to floats (from string)
        df['dB'] = df['dB'].astype(float)
        df['freq'] = df['freq'].astype(float)
        # Adds file name to df
        df['Source'] = os.path.basename(file)  # Add a source column to identify the file
        data_frames.append(df)

    combined_df = pd.concat(data_frames, ignore_index=True)
    if show_title_checkbox.value:
        title = f'Data from: {files_path}'
    else:
        title = 'S21 Log Mag'
    if dark.value:
        theme = 'plotly_dark'
    else:
        theme = 'plotly'
    fig = px.line(combined_df, x='freq', y='dB', color='Source', height=900, title=title, template=theme)
    # fig.update_layout(template='plotly_dark')
    # Sets tick interval for freq axis
    tickvals = list(range(30_000_000, 9_000_000_000, 1_000_000_000))
    # For tick text
    ticktext = []
    for i in range(len(tickvals)):
        if i == 0:
            # First one is MHz range
            ticktext.append(f"{tickvals[i]/1e6:.0f} MHz")
        else:
            # Subtracts 30M to get even GHz tick marks
            tickvals[i] = tickvals[i] - 30_000_000
            ticktext.append(f"{tickvals[i]/1e9:.0f} GHz")
    # Range function does not add last element
    tickvals.append(9_000_000_000)
    ticktext.append("9 GHz")

    fig.update_xaxes(tickvals=tickvals, ticktext=ticktext, tickformat=".0e", type='log', tickangle=45)
    ui.notify(f'Parsed {len(all_files)} file(s)', close_button='Close')
    return fig
    
def open_folder_dialog_data():
    folder = open_folder_dialog()
    if folder:
        files = glob.glob(os.path.join(folder, "*.prn"))
        file_names = [os.path.basename(file) for file in files]

        data_params.data_files = file_names
        data_params.data_folder = folder
        
        data_folder.set_value(data_params.data_folder)
        file_names = '\n'.join(data_params.data_files)
        data_files.set_value(file_names)
        
        tool_tip_dis.delete()
        generate_button.tooltip("Click To Generate Graph").style('font-size: 90%')
        generate_button.enable()

def open_folder_dialog_norm():
    file = open_file_dialog()

    if file:
        data_params.norm_file = os.path.basename(file.name)
        data_params.norm_folder = os.path.dirname(file.name)
        norm_file.set_value(data_params.norm_file)
        norm_folder.set_value(f'{data_params.norm_folder}')

def open_folder_dialog():
    root = Tk()
    root.attributes('-topmost', True)
    root.withdraw() 
    folder_selected = filedialog.askdirectory()
    root.deiconify()
    root.destroy()
    return folder_selected

def open_file_dialog():
    root = Tk()
    root.attributes('-topmost', True)
    root.withdraw() 
    file_selected = filedialog.askopenfile(filetypes=[('Print to File', '*.prn')])
    root.deiconify()
    root.destroy()
    return file_selected


    if folder_selected:
        fig = import_data_and_graph(folder_selected)
        if delete_checkbox.value:
            graph_card.clear()
        with graph_card:
            ui.plotly(fig).classes('w-full')

def update_theme(theme):
    if theme:
        theme = 'plotly_dark'
        dark.enable()
    else:
        theme = 'plotly'
        dark.disable()

if __name__ in {"__main__", "__mp_main__"}:

    data_params = DataParams()

    dark = ui.dark_mode()
    dark.disable()

    with ui.header(elevated=True).style('background-color: #338185').classes('items-center justify-between') as header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        ui.label('S21 Log Mag Graph Generator')
        ui.image(source=PATH_TO_LOGO).style('width: 200px; height: auto;')

    with ui.left_drawer(fixed=False).style('background-color: #338185').props('width=600 bordered') as left_drawer:
        with ui.card().classes('w-full') as select_data_folder:
            with ui.row().classes('w-full items-center justify-between'):
                ui.button('Select Data Folder', on_click=open_folder_dialog_data).classes('ml-auto').classes('w-3/4').props('color=cyan-9')
                ui.button('Clear').classes('ml-auto').classes('w-1/5').props('color=cyan-9')
            data_files = ui.textarea(label='File(s)').classes('w-full').props('clearable')
            data_folder = ui.input(label='Folder').classes('w-full').props('clearable')

        with ui.card().classes('w-full') as select_norm_file:
            with ui.row().classes('w-full items-center justify-between'):
                ui.button('Select Norm. File', on_click=open_folder_dialog_norm).classes('ml-auto').classes('w-3/4').props('color=cyan-9')
                ui.button('Clear').classes('ml-auto').classes('w-1/5').props('color=cyan-9')
            norm_file = ui.input(label='File').classes('w-full').props('clearable')
            norm_folder = ui.input(label='Folder').classes('w-full').props('clearable')
            ui.label('Selected file will be used to normalized data').style('font-size: 90%')
        
        with ui.card().classes('w-full') as generate_card:
            with ui.button('Generate Graph').classes('w-full').props('color=cyan-9') as generate_button:
                tool_tip_dis = ui.tooltip('Please Select A Data Folder First').style('font-size: 90%')#.classes('bg-cyan-9')
        generate_button.disable()
        
        with ui.card().classes('w-full') as settings:
            ui.label('Settings')
            delete_checkbox = ui.checkbox('Delete Previous Graph(s)', value=True).props('color=cyan-9')
            show_title_checkbox = ui.checkbox('Show File Path In Graph', value=True).props('color=cyan-9')
            open_with_plotly = ui.checkbox('Open With Plotly', value=False).props('color=cyan-9')
            with ui.row().classes('w-full items-center justify-between'):
                ui.button('Dark', on_click=lambda:update_theme(True)).classes('w-2/5').props('color=cyan-9')
                ui.button('Light', on_click=lambda:update_theme(False)).classes('w-2/5').props('color=cyan-9')

    with ui.card().classes('w-full') as graph_card:
        ui.label(text='Please select a folder using the button')

    ui.run(title='Ljungtech')