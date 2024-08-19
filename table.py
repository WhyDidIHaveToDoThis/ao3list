from nicegui import ui
import library
import pandas as pd

df = pd.read_csv('library.csv')

def get_df_col(df):
    """Store the columns and its headerName as the upper case of the field name in a list"""
    return [{
        "headerName": col.upper(),
        "field": col,
        "cellStyle": {"whiteSpace": "normal", "overflow": "visible", "textOverflow": "clip"},  # Wrap text and prevent overflow
        "autoHeight": True,  # Auto-adjust row height to fit content
        "minWidth": 150,  # Set a minimum width for columns
        "flex": 1  # Make columns flexible to use available space
    } for col in df.columns]

def get_df_row(df):
    """Return the data of your dataframe"""
    return df.to_dict('records')

# Read the dataframe as a ui.aggrid object
ui.aggrid({
    'columnDefs': get_df_col(df=df),
    'rowData': get_df_row(df=df),
    'domLayout': 'normal',  # Automatically adjust height
    'pagination': True,  # Enable pagination if needed
    'paginationPageSize': 20,  # Adjust page size for pagination if needed
    'defaultColDef': {
        'resizable': True,  # Allow columns to be resized
    }
}).classes('w-full h-screen overflow-x-auto')  # Ensure the table can scroll horizontally

custom_css = """
<style>
    .ag-theme-alpine {
        height: 100vh;  /* Make sure Ag-Grid takes full viewport height */
        display: flex;
        flex-direction: column;
    }
    .ag-root {
        flex: 1;  /* Allow the Ag-Grid to expand within the container */
    }
</style>
"""

ui.add_css(custom_css)

# ui.label('This is testing')




def refresh():
    """rebuild database"""
    newdf = library.create_database('library/')
    newdf.to_csv('library.csv', index=False)
    ui.notify('Done!')


ui.button('Reload', on_click=refresh)
ui.run()



