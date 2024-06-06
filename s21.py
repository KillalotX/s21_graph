# Python
import glob
import plotly.express as px
import os
import pandas as pd

PATH_TO_FILES = "./data"

def import_and_graph(
        files_path: str
        ) -> None:
    
    # All file names to a list
    all_files = glob.glob(os.path.join(files_path, "*.prn"))
    # Column name in dataframe
    column_names = ['freq', 'dB', 'r']
    data_frames = []
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
    fig = px.line(combined_df, x='freq', y='dB', color='Source', title='S21 Log Mag')

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

    fig.update_xaxes(tickvals=tickvals, ticktext=ticktext, tickformat=".0e", type='log')
    fig.show()

if __name__ == "__main__":
    import_and_graph(PATH_TO_FILES)