import pandas as pd
import os
import PySimpleGUI as sg
import random

class Constants:
    TEMPERATURE = 1000
    COOLING_RATE = 0.9
    STOPPING_TEMPERATURE = 1
    EPOCHS = 100

# ============================ Dark Violet Theme ============================
dark_violet_theme = {
    'BACKGROUND': '#1E1E1E',      # Dark gray background
    'TEXT': '#E0E0E0',            # Light gray text
    'INPUT': '#3A3A3A',           # Dark charcoal input fields
    'TEXT_INPUT': '#FFFFFF',      # White text in inputs
    'BUTTON': ('white', '#720e9e'),  # White text on dark violet
    'BUTTON_HOVER': ('white', '#4A148C'),  # Lighter violet on hover
    'PROGRESS': ('#720e9e', '#1E1E1E'),
    'BORDER': 1,
    'SCROLL': '#4A148C',
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
    'COLOR_LIST': ['#1E1E1E', '#720e9e', '#3A3A3A']
}

sg.theme_add_new('DarkVioletTheme', dark_violet_theme)
sg.theme('DarkVioletTheme')
# =============================================================================

# ============================ Global ============================
# Initialize dataframes
if os.path.exists('vehicles.csv'):
    vehicles = pd.read_csv('vehicles.csv')
else:
    vehicles = pd.DataFrame(columns=['vehicle_id', 'capacity', 'is_available'])
    vehicles.to_csv('vehicles.csv', index=False)

if os.path.exists('packages.csv'):
    packages = pd.read_csv('packages.csv')
else:
    packages = pd.DataFrame(columns=['package_id', 'dest_x', 'dest_y', 'weight', 'priority', 'is_delivered'])
    packages.to_csv('packages.csv', index=False)
# ============================ Global ============================

def add_package():
    global packages
    try:
        pack_id = len(packages) + 1
    except Exception:
        pack_id = 1

    layout = [
        [sg.Text('📦 Add New Package', font=('Arial', 14))],
        [sg.Text('X Coordinate (0-100):'), sg.Input(key='-X-', size=(10, 1))],
        [sg.Text('Y Coordinate (0-100):'), sg.Input(key='-Y-', size=(10, 1))],
        [sg.Text('Weight (kg):'), sg.Input(key='-WEIGHT-', size=(10, 1))],
        [sg.Text('Priority (1-5):'), sg.Input(key='-PRIORITY-', size=(10, 1))],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    window = sg.Window('Add Package', layout, modal=True, element_padding=(10, 10))

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == 'Submit':
            try:
                x = int(values['-X-'])
                y = int(values['-Y-'])
                weight = int(values['-WEIGHT-'])
                priority = int(values['-PRIORITY-'])

                if not (0 <= x <= 100 and 0 <= y <= 100):
                    sg.popup_error('Coordinates must be between 0-100', title='Error')
                    continue
                if not 1 <= priority <= 5:
                    sg.popup_error('Priority must be between 1-5', title='Error')
                    continue

                new_package = pd.DataFrame({
                    "package_id": [f"p{pack_id}"],
                    "dest_x": [x],
                    "dest_y": [y],
                    "weight": [weight],
                    "priority": [priority],
                    "is_delivered": [False]
                })

                packages = pd.concat([packages, new_package], ignore_index=True)
                packages.to_csv("packages.csv", index=False)
                sg.popup(f'✅ Package p{pack_id} added successfully!', title='Success')
                break
            except ValueError:
                sg.popup_error('Please enter valid numbers', title='Error')

    window.close()

def drop_package():
    global packages
    if packages.empty:
        sg.popup('⚠️ No packages available', title='Info')
        return

    layout = [
        [sg.Text('🗑️ Drop Package', font=('Arial', 14))],
        [sg.Text('Enter Package ID (e.g., p1):'), sg.Input(key='-ID-')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    window = sg.Window('Drop Package', layout, modal=True, element_padding=(10, 10))

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == 'Submit':
            pack_id = values['-ID-'].strip()
            if pack_id in packages["package_id"].values:
                packages = packages[packages["package_id"] != pack_id]
                packages.to_csv("packages.csv", index=False)
                sg.popup(f'✅ Package {pack_id} removed', title='Success')
                break
            else:
                sg.popup_error('❌ Invalid package ID', title='Error')

    window.close()

def add_vehicle():
    global vehicles
    try:
        vehicle_id = len(vehicles) + 1
    except Exception:
        vehicle_id = 1

    layout = [
        [sg.Text('🚛 Add New Vehicle', font=('Arial', 14))],
        [sg.Text('Capacity (kg):'), sg.Input(key='-CAPACITY-', size=(10, 1))],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    window = sg.Window('Add Vehicle', layout, modal=True, element_padding=(10, 10))

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == 'Submit':
            try:
                capacity = int(values['-CAPACITY-'])
                new_vehicle = pd.DataFrame({
                    "vehicle_id": [f"v{vehicle_id}"],
                    "capacity": [capacity],
                    "is_available": [True]
                })

                vehicles = pd.concat([vehicles, new_vehicle], ignore_index=True)
                vehicles.to_csv("vehicles.csv", index=False)
                sg.popup(f'✅ Vehicle v{vehicle_id} added successfully!', title='Success')
                break
            except ValueError:
                sg.popup_error('Please enter valid capacity', title='Error')

    window.close()

def drop_vehicle():
    global vehicles
    if vehicles.empty:
        sg.popup('⚠️ No vehicles available', title='Info')
        return

    layout = [
        [sg.Text('🛻 Drop Vehicle', font=('Arial', 14))],
        [sg.Text('Enter Vehicle ID (e.g., v1):'), sg.Input(key='-ID-')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    window = sg.Window('Drop Vehicle', layout, modal=True, element_padding=(10, 10))

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == 'Submit':
            vehicle_id = values['-ID-'].strip()
            if vehicle_id in vehicles["vehicle_id"].values:
                vehicles = vehicles[vehicles["vehicle_id"] != vehicle_id]
                vehicles.to_csv("vehicles.csv", index=False)
                sg.popup(f'✅ Vehicle {vehicle_id} removed', title='Success')
                break
            else:
                sg.popup_error('❌ Invalid vehicle ID', title='Error')

    window.close()

def calculate_ga():
    pass

def calculate_distance(index1, index2):
    if index1 == -1:
        return ((packages["dest_x"][index2] ** 2) + (packages["dest_y"][index2] ** 2)) ** 0.5
    return (((packages["dest_x"][index2] - packages["dest_x"][index1]) ** 2) + ((packages["dest_y"][index2] - packages["dest_y"][index1]) ** 2)) ** 0.5

def objective_function(state):
    pass

def random_next_state(state):
    pass

def calculate_sa():
    global packages
    temp = Constants.TEMPERATURE
    epochs = Constants.EPOCHS
    cooling_rate = Constants.COOLING_RATE

    state = {}
    max_range = len(packages["package_id"])
    copy_packages = packages.copy()

    for vid in vehicles["vehicle_id"].values:
        if max_range <= 0:
            break
        random_index = int(random.random() * max_range)
        max_range -= 1
        state[f"{vid}"] = [(0,0), (copy_packages["dest_x"][random_index],copy_packages["dest_y"][random_index])]
        copy_packages.drop(random_index, axis=0, inplace=True)
        copy_packages.reset_index(inplace=True, drop=True)

    print(state)

    for i in range(epochs):
        if temp < 1 :
            break
        temp *= cooling_rate

        next_state =


def main():
    layout = [
        # Main text
        [sg.Text('🚚 Logistics Management System', font=('Arial', 20),
                 justification='center', text_color='#E0E0E0',
                 background_color='#1E1E1E', expand_x=True, pad=(0, 20))],
        [sg.HorizontalSeparator(color='#4A148C')],
        # Centered column with all three frames
        [sg.Column([
            # Packages Frame
            [sg.Frame('📦 Packages', [
                [sg.Button('➕ Add Package', size=(20, 2)),
                 sg.Button('🗑️ Drop Package', size=(20, 2))],
                [sg.Button('📜 View Packages', size=(43, 2))]
            ], title_color='#E0E0E0', background_color='#1E1E1E',
                      element_justification='center', pad=(15, 15), border_width=1)],
            # Vehicles Frame
            [sg.Frame('🚛 Vehicles', [
                [sg.Button('➕ Add Vehicle', size=(20, 2)),
                 sg.Button('🛻 Drop Vehicle', size=(20, 2))],
                [sg.Button('📜 View Vehicles', size=(43, 2))]
            ], title_color='#E0E0E0', background_color='#1E1E1E',
                      element_justification='center', pad=(15, 15), border_width=1)],
            # Optimization Algorithms Frame
            [sg.Frame('⚙️ Optimization Algorithms', [
                [sg.Button('🔥 Simulated Annealing (SA)', size=(20, 2)),
                 sg.Button('🧬 Genetic Algorithm (GA)', size=(20, 2))]
            ], title_color='#E0E0E0', background_color='#1E1E1E',
                      element_justification='center', pad=(15, 15), border_width=1)]
        ], justification='center', element_justification='center')],
        [sg.HorizontalSeparator(color='#4A148C')],
        # Exit button
        [sg.Button('❌ Exit', expand_x=True, size=(20, 1))]
    ]

    window = sg.Window('Logistics Manager', layout, size=(800, 600),
                       resizable=True, finalize=True, element_padding=(12, 12),
                       background_color='#1E1E1E')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '❌ Exit':
            break
        elif event == '➕ Add Package':
            add_package()
        elif event == '🗑️ Drop Package':
            drop_package()
        elif event == '📜 View Packages':
            if not packages.empty:
                sg.Window('Packages List', [[sg.Table(values=packages.values.tolist(),
                                                      headings=packages.columns.tolist(),
                                                      auto_size_columns=True,
                                                      display_row_numbers=False,
                                                      num_rows=25,
                                                      background_color='#3A3A3A',
                                                      text_color='#E0E0E0')]],
                         modal=True, background_color='#1E1E1E').read(close=True)
            else:
                sg.popup('⚠️ No packages available', title='Info', background_color='#1E1E1E')
        elif event == '➕ Add Vehicle':
            add_vehicle()
        elif event == '🛻 Drop Vehicle':
            drop_vehicle()
        elif event == '📜 View Vehicles':
            if not vehicles.empty:
                sg.Window('Vehicles List', [[sg.Table(values=vehicles.values.tolist(),
                                                      headings=vehicles.columns.tolist(),
                                                      auto_size_columns=True,
                                                      display_row_numbers=False,
                                                      num_rows=25,
                                                      background_color='#3A3A3A',
                                                      text_color='#E0E0E0')]],
                         modal=True, background_color='#1E1E1E').read(close=True)
            else:
                sg.popup('⚠️ No vehicles available', title='Info', background_color='#1E1E1E')
        elif event == '🔥 Simulated Annealing (SA)':
            calculate_sa()
        elif event == '🧬 Genetic Algorithm (GA)':
            calculate_ga()

    window.close()

if __name__ == '__main__':
    # main()
    calculate_sa()