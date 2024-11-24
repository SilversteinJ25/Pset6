import pandas as pd
from shiny import App, render, ui, reactive

# Define UI
app_ui = ui.page_fluid(
    ui.input_select(
        id='Type',  # input for choosing the type of alert
        label='Choose a type:',  
        choices=[],  # options will be populated dynamically
    ),
    ui.output_table("subsetted_data_table")  # table to display the filtered data
)

# Define Server logic
def server(input, output, session):
    
    # Read the CSV file and process it reactively
    @reactive.calc
    def full_data():
        return pd.read_csv('/Users/justinesilverstein/Desktop/Pset6/top_alerts_map/basic-app/top_alerts_map.csv')
    
    # Dynamically populate the 'choices' in the select input
    @reactive.calc
    def alert_types():
        df = full_data()
        # Get unique alert types from the 'updated_type' column
        return df['updated_type'].unique().tolist()

    # Update choices for the select input
    @output
    @render.ui
    def update_select_choices():
        # Set the choices in the input select to the unique alert types
        return ui.input_select(
            id='Type',  # input for choosing the type of alert
            label='Choose a type:',  
            choices=alert_types()  # Populate with the unique alert types
        )
    
    # Filter data based on the selected type
    @reactive.calc
    def subsetted_data():
        df = full_data()
        selected_type = input.Type()  # Get the selected type
        return df[df['updated_type'] == selected_type]

    # Render the filtered data table
    @output
    @render.table
    def subsetted_data_table():
        return subsetted_data()


# Create the app
app = App(app_ui, server)



