import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display, clear_output, HTML

# Load and preprocess data
df = pd.read_csv("ElectricCarData_Norm.csv")
df['Accel'] = df['Accel'].str.replace(' sec', '').astype(float)
df['TopSpeed'] = df['TopSpeed'].str.replace(' km/h', '').astype(int)
df['Range'] = df['Range'].str.replace(' km', '').astype(int)

# Define the recommendation function
def find_best_cars_v2(desired_accel_range, desired_speed_range, desired_range_range, desired_powertrain):
    filtered_df = df[
        (df['PowerTrain'] == desired_powertrain) &
        (df['Accel'] >= desired_accel_range[0]) &
        (df['Accel'] <= desired_accel_range[1]) &
        (df['TopSpeed'] >= desired_speed_range[0]) &
        (df['TopSpeed'] <= desired_speed_range[1]) &
        (df['Range'] >= desired_range_range[0]) &
        (df['Range'] <= desired_range_range[1])
    ]
    filtered_df['score'] = (
        (1 / (abs((filtered_df['Accel'] - desired_accel_range[0] + filtered_df['Accel'] - desired_accel_range[1]) / 2) + 1)) +
        (1 / (abs((filtered_df['TopSpeed'] - desired_speed_range[0] + filtered_df['TopSpeed'] - desired_speed_range[1]) / 2) + 1)) +
        (1 / (abs((filtered_df['Range'] - desired_range_range[0] + filtered_df['Range'] - desired_range_range[1]) / 2) + 1))
    )
    top_cars = filtered_df.sort_values(by='score', ascending=False).head(2)
    return top_cars[['Brand', 'Model', 'Accel', 'TopSpeed', 'Range', 'PowerTrain']]

# Define the visualization function
def plot_comparison(cars_df):
    attributes = ['Accel', 'TopSpeed', 'Range']
    fig, axes = plt.subplots(nrows=len(attributes), ncols=1, figsize=(10, 8))
    for i, attribute in enumerate(attributes):
        cars_df.set_index('Model')[attribute].plot(kind='bar', ax=axes[i], color=['blue', 'green'])
        axes[i].set_ylabel(attribute)
        axes[i].set_xlabel('')
        axes[i].grid(axis='y')
    plt.tight_layout()
    plt.show()

# Create widgets and define their functionality
accel_widget = widgets.Dropdown(options=accel_options, description='Acceleration:')
speed_widget = widgets.Dropdown(options=speed_options, description='Top Speed:')
range_widget = widgets.Dropdown(options=range_options, description='Range:')
powertrain_widget = widgets.Dropdown(options=sorted(df['PowerTrain'].unique()), description='PowerTrain:')
recommendation_button = widgets.Button(description="Get Recommendations", button_style='success')
output = widgets.Output()

def on_button_click(button):
    with output:
        clear_output(wait=True)
        top_cars = find_best_cars_v2(accel_widget.value, speed_widget.value, range_widget.value, powertrain_widget.value)
        if top_cars.empty:
            display(HTML("<div style='color: red; font-size: 20px;'>No cars found matching the criteria.</div>"))
        else:
            display(HTML("<div style='font-size: 20px;'>Top Recommendations:</div>"))
            display(top_cars.style.set_properties(**{'text-align': 'center'}))
            plot_comparison(top_cars)

recommendation_button.on_click(on_button_click)

# Display widgets
form_item_layout = widgets.Layout(display='flex', flex_flow='row', justify_content='space-between', width='50%')
form_items = [
    widgets.Box([accel_widget], layout=form_item_layout),
    widgets.Box([speed_widget], layout=form_item_layout),
    widgets.Box([range_widget], layout=form_item_layout),
    widgets.Box([powertrain_widget], layout=form_item_layout),
    widgets.Box([recommendation_button], layout=form_item_layout)
]
form = widgets.VBox(form_items, layout=widgets.Layout(display='flex', flex_flow='column', align_items='center', width='50%'))
display(form, output)
