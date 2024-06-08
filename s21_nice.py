# Python
import glob
import plotly.express as px
from plotly.graph_objs import Figure
import os
import pandas as pd
from nicegui import ui
from tkinter import filedialog, Tk

PATH_TO_LOGO = './assets/ljungtechlogo.png'

class DataParams():
    def __init__(self) -> None:
        self.plotly_theme = 'plotly'
        self.data_folder = None
        self.data_files = None
        self.norm_folder = None
        self.norm_file = None
        self.exepmt_textarea_visible = False

def extract_data(
        files_path: str,
        single: bool = False
        ) -> list[pd.DataFrame]:
    
    # Column name in dataframe
    column_names = ['freq', 'dB', 'r']
    data_frames = []
    if not single:
        all_files = glob.glob(os.path.join(files_path, "*.prn"))
    else:
        all_files = [files_path + '\\' + data_params.norm_file]
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
        df['Source'] = os.path.basename(file)  # Add a source column to identify the file
        data_frames.append(df)
    return data_frames

def subtract_through_data(
        main_df: list[pd.DataFrame], 
        through_df: list[pd.DataFrame]
        ) -> list[pd.DataFrame]:

    exempt_list = exepmt_textarea_input.value.split('\n')
    # for item in exempt_list:
    #     if item == '':
    exempt_list = [item for item in exempt_list if item]
    print(repr(exempt_list))

    df_list = []    
    for df in main_df:
        if (df.iloc[0]['Source'] != through_df[0].iloc[0]['Source']
            and not any(exempt in df.iloc[0]['Source'] for exempt in exempt_list)):

            df['dB'] = df['dB'] - through_df[0]['dB']
            pass
        df_list.append(df)
    return df_list

def create_fig(
        dataframe: pd.DataFrame
        ) -> Figure:
    if custom_title_input.value:
        title = custom_title_input.value
    else:
        title = 'S21 Log Mag'
    if dark.value:
        theme = 'plotly_dark'
    else:
        theme = 'plotly'
    fig = px.line(dataframe, x='freq', y='dB', color='Source', height=900, title=title, template=theme)
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
    ui.notify(f'Parsed {len(data_params.data_files)} file(s)', close_button='Close')
    # fig.add_annotation()
    return fig
    
def open_folder_dialog_data():
    folder = open_folder_dialog()
    if folder:
        files = glob.glob(os.path.join(folder, "*.prn"))
        file_names = [os.path.basename(file) for file in files]

        data_params.data_files = file_names
        data_params.data_folder = folder
        
        data_folder_text_input.set_value(data_params.data_folder)
        file_names = '\n'.join(data_params.data_files)
        data_files_text_area.set_value(file_names)

        generate_button.tooltip('').style('font-size: 90%')
        generate_button.tooltip("Click To Generate Graph").style('font-size: 90%')
        generate_button.enable()

def open_folder_dialog_norm():
    file = open_file_dialog()
    if file:
        data_params.norm_file = os.path.basename(file.name)
        data_params.norm_folder = os.path.dirname(file.name)
        norm_file_text_area.set_value(data_params.norm_file)
        norm_folder_text_input.set_value(data_params.norm_folder)

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

def update_theme(dark_mode):
    if dark_mode:
        dark.enable()
    else:
        dark.disable()

def generate_graph():
    df = extract_data(data_params.data_folder)
    if enable_norm_data.value:
        norm_df = extract_data(data_params.norm_folder, single=True)
        df = subtract_through_data(df, norm_df)
    combined_df = pd.concat(df, ignore_index=True)

    fig = create_fig(combined_df)
    fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=5),
        )
    if custom_text_input.value:
        fig.add_annotation(
            text=custom_text_input.value,
            xref='paper', yref='paper',
            x=0.02, y=0.98,
            showarrow=False,
            font=dict(size=12, color='black'),
            bgcolor='lightgrey',
            bordercolor='black',
            borderwidth=1
        )
    if delete_checkbox.value:
        graph_card.clear()
    with graph_card:
        ui.plotly(fig).classes('w-full')
    graph_card.update()

def clear_data_input():
    data_files_text_area.set_value(None)
    data_folder_text_input.set_value(None)
    data_params.data_files = None
    data_params.data_folder = None
    data_files_text_area.update()
    data_folder_text_input.update()
    generate_button.tooltip("Please Select A Data Folder").style('font-size: 90%')
    generate_button.disable()

def clear_norm_input():
    norm_file_text_area.set_value(None)
    norm_folder_text_input.set_value(None)
    data_params.norm_file = None
    data_params.norm_folder = None
    norm_file_text_area.update()
    norm_folder_text_input.update()

if __name__ in {"__main__", "__mp_main__"}:

    data_params = DataParams()

    dark = ui.dark_mode()
    dark.disable()

    with ui.header(elevated=True).style('background-color: #338185').classes('items-center justify-between') as header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        ui.label('S21 Log Mag Graph Generator')
        ui.image(source=PATH_TO_LOGO).style('width: 200px; height: auto;')

    with ui.left_drawer(fixed=False).style('background-color: #338185').props('width=450') as left_drawer:
        with ui.card().classes('w-full') as select_data_folder:
            with ui.row().classes('w-full items-center justify-between'):
                ui.button('Select Data Folder', on_click=open_folder_dialog_data).classes('ml-auto').classes('w-3/4').props('color=cyan-9')
                data_clear_button = ui.button('Clear', on_click=clear_data_input).classes('ml-auto').classes('w-1/5').props('color=cyan-9')
            data_files_text_area = ui.textarea(label='File(s)').classes('w-full')
            data_folder_text_input = ui.input(label='Folder').classes('w-full')

        with ui.card().classes('w-full') as select_norm_file:
            enable_norm_data = ui.checkbox('Normalize Data', value=False).props('color=cyan-9')
            with ui.row().classes('w-full items-center justify-between').bind_visibility_from(enable_norm_data, 'value'):
                ui.button('Select Norm. File', on_click=open_folder_dialog_norm).classes('ml-auto').classes('w-3/4').props('color=cyan-9')
                norm_clear_button = ui.button('Clear', on_click=clear_norm_input).classes('ml-auto').classes('w-1/5').props('color=cyan-9')
            norm_file_text_area = ui.input(label='File').classes('w-full').bind_visibility_from(enable_norm_data, 'value')
            norm_folder_text_input = ui.input(label='Folder').classes('w-full').bind_visibility_from(enable_norm_data, 'value')
            # ui.label('Selected File Will Be Used To Normalize Data').style('font-size: 80%; font-style: italic;').bind_visibility_from(enable_norm_data, 'value')
            ui.separator().props('color=cyan-9').bind_visibility_from(enable_norm_data, 'value')
            ui.label('Exempt List (New Line Separated):').bind_visibility_from(enable_norm_data, 'value')
            exepmt_textarea_input = ui.textarea(value='Through\n50dB').classes('w-full').bind_visibility_from(enable_norm_data, 'value').tooltip('Any File Containing A Word From this List Will Not Be Modified With Above Selected File')
        
        with ui.card().classes('w-full') as generate_card:
            with ui.button('Generate Graph', on_click=generate_graph).classes('w-full').props('color=cyan-9').tooltip('Please Select A Data Folder') as generate_button:
                pass
            custom_title_input = ui.input(placeholder='Enter A Custom Title').classes('w-full').tooltip('DeFault Title: S21 Log Mag')
            custom_text_input = ui.input(placeholder='Enter A Custom Text To Be Displayed In The Plot').classes('w-full')
        generate_button.disable()
        
        with ui.card().classes('w-full') as settings:
            ui.label('Settings')
            delete_checkbox = ui.checkbox('Delete Previous Graph(s)', value=True).props('color=cyan-9')
            with ui.row().classes('w-full items-center justify-between'):
                ui.button('Dark', on_click=lambda:update_theme(True)).classes('w-2/5').props('color=cyan-9')
                ui.button('Light', on_click=lambda:update_theme(False)).classes('w-2/5').props('color=cyan-9')

    with ui.card().classes('w-full') as graph_card:
        ui.label(text='Please Select A Folder')

    ui.run(title='Ljungtech')