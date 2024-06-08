# S21 graph concept
Using NiceGUI library to create a simple webpage that can visualize measurement data
### Light theme
![image](https://github.com/KillalotX/s21_graph/assets/101448966/3b2d524f-6885-47a4-8ae5-fb63688455da)
### Dark Theme
![image](https://github.com/KillalotX/s21_graph/assets/101448966/19a72e27-4a01-402b-8778-2f5a7babd9a7)



## How to use
Run script:

`python s21_nice.py`

- A webpage will open, select a folder for measurement data
- Select a file if data should be normalized
- Click 'Generate Graph'

## Features
- Adding a custom text to the graph area (upper left corner)
- Possible to keep previously generated graphs
- Swicth Title of graph to selected data folder
- Switch between Dark and Light mode (Note: graph will not auto-update to new theme, needs to be regenerated)

## Prerequisite
`pip install pandas`

`pip install plotly`

`pip install nicegui`

## Know issues
- Plotly graph not always shown in the full width of screen, resize to fix this
- Selecting a folder/file not always updates the GUI, reload page to fix 

## Other
- `CTRL-C` twive in terminal to exit
