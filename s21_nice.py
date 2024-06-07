# Python
import glob
import plotly.express as px
import os
import pandas as pd
from nicegui import ui
from tkinter import filedialog
from tkinter import filedialog, Tk

PATH_TO_FILES = "./data"

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
    
def open_folder_dialog():
    root = Tk()
    root.attributes('-topmost', True)
    root.withdraw() 
    folder_selected = filedialog.askdirectory()
    root.deiconify()
    root.destroy()

    if folder_selected:
        fig = import_data_and_graph(folder_selected)
        if delete_checkbox.value:
            graph_card.clear()
        with graph_card:
            ui.plotly(fig).classes('w-full')
def update_theme():
    if dark.value:
        theme = 'plotly_dark'
        dark.disable()
    else:
        theme = 'plotly'
        dark.enable()
    

if __name__ in {"__main__", "__mp_main__"}:
    # fig = px.line()
    dark = ui.dark_mode()
    # print(dark.value)

    dark.disable()
    with ui.row() as top_row:
        ui.button('Select Folder', on_click=open_folder_dialog)
        delete_checkbox = ui.checkbox('Delete previous graph(s)', value=True)
        show_title_checkbox = ui.checkbox('Show file path as title', value=True)
        # ui.label('Theme:').classes('center-content')
        ui.button('Dark', on_click=update_theme)
        ui.button('Light', on_click=update_theme)
    with ui.card() as graph_card:
        ui.label(text='Please select a folder using the button')
    graph_card.classes('w-full')
    ui.run()