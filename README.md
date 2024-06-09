# S21 graph concept
Using NiceGUI library to create a simple webpage that can visualize measurement data
### Light theme
![image](https://github.com/KillalotX/s21_graph/assets/101448966/05edd2e3-3500-4c56-b55a-01a260227fce)

### Dark Theme
![image](https://github.com/KillalotX/s21_graph/assets/101448966/91009822-1876-4ffa-8939-052e55cb508c)

## How to use
Run script:

`python s21_nice.py`

- A webpage will open, select a folder for measurement data
- Select a file if data should be normalized
  - ~~If selected, it will not normalize any file that contains the words "**Through**" or "**50dB**" and of course the file selected...~~
  - Now possible to add custom keywords in a text box that should be excluded (Default is still "**Through**" and "**50dB**")
- Click 'Generate Graph'

## Features
- Set custom title of graph
- Adding a custom text to the graph area (upper left corner)
- Possible to keep previously generated graphs
- Switch between Dark and Light mode (Note: graph will not auto-update to new theme, needs to be regenerated)

## Prerequisite
`pip install pandas`

`pip install plotly`

`pip install nicegui`

## Know issues
- Plotly graph not always shown in the full width of screen, resize to fix this
- Selecting a folder/file not always updates the GUI, reload page to fix 

## Other
- `CTRL-C` to exit
