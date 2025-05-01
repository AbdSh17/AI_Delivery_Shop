import copy
import math

import pandas as pd
import os
import PySimpleGUI as sg
import random
import time

from sympy import false


class Constants:
    TEMPERATURE = 1000
    COOLING_RATE = 0.99
    STOPPING_TEMPERATURE = 1
    EPOCHS = 1000
    PRIORITY_RATIO = 0.5
    RE_INITIATE_EPOCHS = 10
    DRAW_SLEEP_TIME = 0.4

    SWAP_IN_SAME_VEHICLE, SWAP_IN_DIFFERENT_VEHICLE, MOVE_TO_DIFFERENT_VEHICLE = [0], [1], [2]


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
    all_packages = packages.copy()
else:
    packages = pd.DataFrame(columns=['package_id', 'dest_x', 'dest_y', 'weight', 'priority', 'is_delivered'])
    packages.to_csv('packages.csv', index=False)
    all_packages = packages.copy()
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

def calculate_distance(x1, y1, x2, y2):
    return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5

def objective_function(state):

    total_distance, real_distance = 0, 0
    x1, x2 = 0, 0
    # Loop for each van
    for van in state.keys():
        van_distance = 0
        x1, x2, first_epoch = 0, 0, True

        van_priority = 0
        for pack in state[van][1::]:

            van_distance += (calculate_distance(x1, x2, pack[0], pack[1]))
            van_priority += ((Constants.PRIORITY_RATIO / (pack[2])) * van_distance)
            x1, x2 = pack[0], pack[1]

        total_distance += (van_priority + van_distance)
        real_distance += van_distance

            # total distance + return distance
    return total_distance + calculate_distance(x1, x2, 0, 0), real_distance + calculate_distance(x1, x2, 0, 0)

def make_valid_packages():

    global packages, vehicles

    sorted_packages = packages.sort_values(by=["priority", "weight"], ascending=[True, True])

    # drop any package can't fit in any van
    max_vehicle_capacity = vehicles["capacity"].max()
    packages = packages[packages["weight"] <= max_vehicle_capacity].reset_index(drop=True)

    # drop any van can't fit in any package
    min_package_weight = packages["weight"].min()
    vehicles = vehicles[vehicles["capacity"] >= min_package_weight].reset_index(drop=True)

    packages_weights = sum(packages["weight"].values)
    vehicles_capacity = sum(vehicles["capacity"].values)

    if vehicles_capacity >= packages_weights:
        packages["is_delivered"] = True # all the packages will be delivered
        return True

    while packages_weights > vehicles_capacity:
        if sorted_packages.empty:
           # if no packages left
            return False

        # drop the last package (lowest priority, highest weight)
        dropped_package = sorted_packages.iloc[-1] # get the last pack
        packages_weights -= dropped_package["weight"] # remove last pack weight
        sorted_packages = sorted_packages.iloc[:-1]  # remove the last package

    packages.drop(packages.index.difference(sorted_packages.index), inplace=True) # re-update packages
    packages["is_delivered"] = True # all the remain packages will be delivered

    return True

def random_next_state(state, weights_state):

    new_state = copy.deepcopy(state) # Deep Cloning
    choices = 3 # Either Switch between packs in the same vehicle or switch in other vehicles
    switching_method = random.randint(0, choices - 1)

    number_of_vehicles = len(vehicles["vehicle_id"])
    number_of_all_packs = len(packages["package_id"])

    if number_of_all_packs <= 1:
        print("Just one pack")
        exit(1)

    if number_of_vehicles == 0:
        print("No vehicles")
        exit(1)

    if number_of_vehicles == 1:
        switching_method = Constants.SWAP_IN_SAME_VEHICLE[0]

    found_vehicle1, found_vehicle2 = False, True

    # if no vehicle with more than one location than option 2 (can't SWAP_IN_SAME_VEHICLE)
    if switching_method in Constants.SWAP_IN_SAME_VEHICLE:

        for i in range(number_of_vehicles):
            vid = vehicles.iloc[i]["vehicle_id"]
            if len(new_state[f"{vid}"]) > 2:
                found_vehicle1 = True
                break

        if not found_vehicle1:
            switching_method = Constants.SWAP_IN_DIFFERENT_VEHICLE[0]

    # if all the packs are in the same vehicle (can't SWAP_IN_different_VEHICLE)
    if switching_method in Constants.SWAP_IN_DIFFERENT_VEHICLE:
        for i in range(number_of_vehicles):
            vid = vehicles.iloc[i]["vehicle_id"]
            if len(new_state[f"{vid}"]) - 1== number_of_all_packs:
                found_vehicle2 = False
                break

        if not found_vehicle2:
            switching_method = Constants.SWAP_IN_SAME_VEHICLE[0]

    package1_number, package2_number, vehicle1_number, vehicle2_number, package_number = 0, 0, 0, 0, 0

    if switching_method in Constants.SWAP_IN_SAME_VEHICLE:
        # ===== Random vehicle ======
        while True:
            vehicle_number = int(random.random() * number_of_vehicles)
            vid = vehicles.iloc[vehicle_number]["vehicle_id"]
            if len(new_state[f"{vid}"]) > 2:
                found_vehicle = True
                break
        # ===== Random vehicle ======

        # if no vehicle with two locations
        if found_vehicle:
            # ===== Random Package in the same vehicle ======
            number_of_packages = len(new_state[f"{vid}"])  # number of packs in a specific vehicle

            while package1_number == package2_number:
                package1_number, package2_number = random.randint(1, number_of_packages - 1), random.randint(1, number_of_packages - 1)
            # ===== Random Package in the same vehicle ======

            # ==== Swap ====
            temp_new_state = new_state[f"{vid}"][package1_number]
            new_state[f"{vid}"][package1_number] = new_state[f"{vid}"][package2_number]
            new_state[f"{vid}"][package2_number] = temp_new_state
            # ==== Swap ====

    if switching_method in Constants.SWAP_IN_DIFFERENT_VEHICLE:

        max_iterations = 0
        while True:
            # ===== Random two vehicles =====
            vehicle1_number, vehicle2_number = int(random.random() * number_of_vehicles), int(random.random() * number_of_vehicles)
            vid1 = vehicles.iloc[vehicle1_number]["vehicle_id"]
            vid2 = vehicles.iloc[vehicle2_number]["vehicle_id"]
            # ===== Random two vehicles =====

            # if the vehicle choice is legal
            if vehicle1_number != vehicle2_number and len(new_state[f"{vid1}"]) > 1 and len(new_state[f"{vid2}"]) > 1:
                # ==== Random Pack ====
                number_of_packages1, number_of_packages2 = len(new_state[f"{vid1}"]), len(new_state[f"{vid2}"])
                package1_number, package2_number = random.randint(1, number_of_packages1 - 1), random.randint(1, number_of_packages2 - 1)
                # ==== Random Pack ====
            else:
                continue

            # check if the weights are legal
            if  weights_state[f"{vid1}"][0] >= (weights_state[f"{vid1}"][1] + new_state[f"{vid2}"][package2_number][3])\
                and weights_state[f"{vid2}"][0] >= (weights_state[f"{vid2}"][1] + new_state[f"{vid1}"][package1_number][3]):
                weights_state[f"{vid1}"][1] -= new_state[f"{vid1}"][package1_number][3]
                weights_state[f"{vid1}"][1] += new_state[f"{vid2}"][package2_number][3]

                weights_state[f"{vid2}"][1] -= new_state[f"{vid2}"][package2_number][3]
                weights_state[f"{vid2}"][1] += new_state[f"{vid1}"][package1_number][3]
                break

            max_iterations += 1
            if max_iterations == number_of_vehicles * 4:
                return None

        # ==== Swap ====
        temp_new_state = new_state[f"{vid1}"][package1_number]
        new_state[f"{vid1}"][package1_number] = new_state[f"{vid2}"][package2_number]
        new_state[f"{vid2}"][package2_number] = temp_new_state
        # ==== Swap ====

    if switching_method in Constants.MOVE_TO_DIFFERENT_VEHICLE:
        max_iterations = 0
        while True:
            # ===== Random two vehicles =====
            vehicle1_number, vehicle2_number = int(random.random() * number_of_vehicles), int(random.random() * number_of_vehicles)
            vid1 = vehicles.iloc[vehicle1_number]["vehicle_id"]
            vid2 = vehicles.iloc[vehicle2_number]["vehicle_id"]
            # ===== Random two vehicles =====

            # if the vehicle choice is legal
            if vehicle1_number != vehicle2_number and len(new_state[f"{vid1}"]) > 1:
                # ==== Random Pack ====
                number_of_packages= len(new_state[f"{vid1}"])
                package_number = random.randint(1, number_of_packages - 1)
                # ==== Random Pack ====
            else:
                continue

                # check if the weights are legal (V2 Capacity > Current V2 + New Package Weight
            if weights_state[f"{vid2}"][0] >= (weights_state[f"{vid2}"][1] + new_state[f"{vid1}"][package_number][3]):
                weights_state[f"{vid1}"][1] -= new_state[f"{vid1}"][package_number][3]
                weights_state[f"{vid2}"][1] += new_state[f"{vid1}"][package_number][3]
                break

            max_iterations += 1
            if max_iterations == number_of_vehicles * 4:
                return None

        # ==== Move ====
        index_to_insert = random.randint(1, len(new_state[f"{vid2}"]))
        new_state[f"{vid2}"].insert(index_to_insert, new_state[f"{vid1}"][package_number])  # move the pack to V2
        new_state[f"{vid1}"].pop(package_number)  # Remove the pack from v1
        # ==== Move ====

    return new_state

def random_initial_state(state, weights_state):
    max_range = len(vehicles["vehicle_id"])  # range of random number to choose
    number_of_packages = len(packages["package_id"])

    for _, pack in packages.iterrows(): # to iterate throw its columns and rows (need rows)
        iterations_count = 0
        while True:
            vehicle_number = int(random.random() * max_range)  # random vehicle
            vid = vehicles.iloc[vehicle_number]["vehicle_id"]  # give me the vehicle with this index

            if weights_state[f"{vid}"][0] >= (weights_state[f"{vid}"][1] + pack["weight"]):
                break

            iterations_count += 1
            if iterations_count == (number_of_packages + 5):
                return False

        state[f"{vid}"].append((pack["dest_x"], pack["dest_y"], pack["priority"], pack["weight"]))
        weights_state[f"{vid}"][1] += pack["weight"]

    return True

def calculate_sa(print_input):
    global packages
    temp = Constants.TEMPERATURE # initial temp
    epochs = Constants.EPOCHS # max number of epochs
    cooling_rate = Constants.COOLING_RATE # temp *= cooling_rate (0.9 <= CR <= 0.99)

    initial_state = {} # empty state will be filled
    initial_weights_state = {}
    # copy_packages = packages.copy() # to drop packages

    for vid in vehicles["vehicle_id"].values:
        initial_state[vid] = [(0, 0, 0, 0)] # capacity
        initial_weights_state[vid]  = [vehicles.loc[vehicles["vehicle_id"] == vid]["capacity"].values[0], 0]

    state = copy.deepcopy(initial_state)
    weights_state = copy.deepcopy(initial_weights_state)
    # loop will give each package to random vehicle until it works

    print("entered")
    while not random_initial_state(state, weights_state):
        weights_state = copy.deepcopy(initial_weights_state)
        state = copy.deepcopy(initial_state)
        continue

    if print_input:
        print(state)
        print(weights_state)


    for i in range(epochs):

        if temp <= 1:
            break

        next_state = random_next_state(state, weights_state)

        if next_state is None: # if the assignation FAILED, retry another random
            continue

        current_state_objective, _ = objective_function(state)
        next_state_objective, _ = objective_function(next_state)
        if print_input:
            print(next_state)

        delta_e = next_state_objective - current_state_objective

        if i % 10 == 0 and print_input:
            print(f"{i}: objective = {int(current_state_objective)}")
            print(state)
            # print(weights_state)

        if delta_e < 0:
            state = next_state
        else:
            odds = math.exp(-delta_e / temp) # - delta because i want to minimise
            random_choose = random.random()
            if random_choose < odds:
                state = next_state

        temp *= cooling_rate

    #
    # print("Final State:", state)
    # print("Final Objective Value:", objective_function(state))
    return state, objective_function(state)

def calculate_minimum_sa():

    global packages, vehicles, all_packages

    make_valid_packages()

    print(packages)

    number_of_vehicles = len(vehicles["vehicle_id"])
    number_of_all_packs = len(packages["package_id"])

    if number_of_all_packs <= 1:
        print("Just one pack")
        packages = pd.read_csv('packages.csv')
        vehicles = pd.read_csv('vehicles.csv')
        all_packages = packages.copy()
        return None

    if number_of_vehicles == 0:
        print("No vehicles")
        packages = pd.read_csv('packages.csv')
        vehicles = pd.read_csv('vehicles.csv')
        all_packages = packages.copy()
        return None


    print(Constants.PRIORITY_RATIO)
    minimum_state, minimum_objective = calculate_sa(True)
    for _ in range(Constants.RE_INITIATE_EPOCHS):
        new_state, new_objective = calculate_sa(False)
        if minimum_objective[0] > new_objective[0]:
            minimum_state, minimum_objective = new_state, new_objective

    print(minimum_state)
    return minimum_state

import math

def visualize_routes_pysimplegui(state):
    graph_size = (800, 600)
    layout = [
        [sg.Graph(
            canvas_size=graph_size,
            graph_bottom_left=(0, 0),
            graph_top_right=(100, 100),
            background_color='#1E1E1E',
            key='-GRAPH-'
        )],
        [sg.Button('Close', button_color=('white', '#2E2E8B'), expand_x=True)]
    ]
    window = sg.Window('Delivery Routes', layout, finalize=True, background_color='#1E1E1E')
    graph = window['-GRAPH-']

    # Draw shop
    graph.DrawCircle((0, 0), radius=5, fill_color='white', line_color='black')
    graph.DrawText('Shop', (0, 0), color='black', font=('Arial Bold', 10), text_location=sg.TEXT_LOCATION_BOTTOM_LEFT)

    # Legend: map each vehicle ID to its color (top-right)
    colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33']
    legend_x, legend_y = 90, 95  # position near top-right
    for idx, vid in enumerate(state.keys()):
        col = colors[idx % len(colors)]
        y_offset = legend_y - idx * 4
        # small color box
        graph.DrawRectangle((legend_x, y_offset), (legend_x + 3, y_offset + 3), fill_color=col, line_color=col)
        # vehicle label
        graph.DrawText(f"{vid}", (legend_x + 5, y_offset + 1), color='white', font=('Arial', 8), text_location=sg.TEXT_LOCATION_LEFT)

    # Draw each vehicle’s animated path
    for idx, (vid, route) in enumerate(state.items()):
        color = colors[idx % len(colors)]
        prev_pt = (0, 0)

        for i, (x, y, priority, _) in enumerate(route):
            curr_pt = (x, y)

            if i > 0:
                # Draw van icon at curr_pt
                body_w, body_h = 4, 2
                bx0, by0 = x - body_w/2, y - body_h/2
                bx1, by1 = x + body_w/2, y + body_h/2
                graph.DrawRectangle((bx0, by0), (bx1, by1), fill_color=color, line_color='white')
                # Wheels
                wheel_r = 0.6
                graph.DrawCircle((bx0 + wheel_r, by0), radius=wheel_r, fill_color='black', line_color='black')
                graph.DrawCircle((bx1 - wheel_r, by0), radius=wheel_r, fill_color='black', line_color='black')
                # Cabin
                roof_w, roof_h = 2.5, 1.2
                rx0 = x - roof_w/2
                ry0 = by1
                graph.DrawRectangle((rx0, ry0), (rx0 + roof_w, ry0 + roof_h), fill_color=color, line_color='white')
                # Priority label
                graph.DrawText(str(priority), (x + 3, y + 3), color='white', font=('Arial Bold', 9))

                # Draw line to this stop (behind the van)
                graph.DrawLine(prev_pt, curr_pt, color=color, width=2)
                window.refresh()
                time.sleep(Constants.DRAW_SLEEP_TIME)

            prev_pt = curr_pt

        # Draw return-to-shop leg (solid gray), no animation
        if len(route) > 1:
            last_x, last_y, _, _ = route[-1]
            graph.DrawLine((last_x, last_y), (0, 0), color='gray', width=1)

    # Event loop
    while True:
        event, _ = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
    window.close()

def main():

    global packages, vehicles, all_packages

    layout = [
        # Main text
        [sg.Text('🚚 Logistics Management System', font=('Arial', 20),
                 justification='center', text_color='#E0E0E0',
                 background_color='#1E1E1E', expand_x=True, pad=(0, 20))],
        [sg.HorizontalSeparator(color='#4A148C')],

        # Two-column layout: Left column for packages/vehicles, Right column for settings
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
        ], justification='center', element_justification='center'),

            sg.VerticalSeparator(color='#4A148C'),

            sg.Column([
                # Optimization Algorithms Frame
                [sg.Frame('⚙️ Optimization Algorithms', [
                    [sg.Button('🔥 Simulated Annealing (SA)', size=(20, 2)),
                     sg.Button('🧬 Genetic Algorithm (GA)', size=(20, 2))]
                ], title_color='#E0E0E0', background_color='#1E1E1E',
                          element_justification='center', pad=(15, 15), border_width=1)],

                # Priority Ratio Slider Frame
                [sg.Frame('⚖️ Priority Settings', [
                    [sg.Text('Priority Ratio (%):', size=(15, 1), justification='right'),
                     sg.Slider(range=(0, 100), default_value=int(Constants.PRIORITY_RATIO * 10), resolution=1,
                               orientation='h', size=(20, 15), key='-PRIORITY-RATIO-SLIDER-')],
                ], title_color='#E0E0E0', background_color='#1E1E1E',
                          element_justification='center', pad=(15, 15), border_width=1)],
            ], justification='center', element_justification='center')],

        [sg.HorizontalSeparator(color='#4A148C')],

        # Exit button
        [sg.Button('❌ Exit', expand_x=True, size=(20, 1))]
    ]

    window = sg.Window('Logistics Manager', layout, size=(1000, 600),
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

            packages = pd.read_csv('packages.csv')
            vehicles = pd.read_csv('vehicles.csv')
            all_packages = packages.copy()

            # Update PRIORITY_RATIO based on slider value (map 0–100 to 0–10)
            Constants.PRIORITY_RATIO = values['-PRIORITY-RATIO-SLIDER-'] / 10
            if packages.empty or vehicles.empty:
                sg.popup('⚠️ Please add packages and vehicles first!', title='Error', background_color='#1E1E1E')
            else:
                # Run Simulated Annealing

                final_state = calculate_minimum_sa()
                if final_state is None:
                    sg.popup("⚠️ there's no packages that can be delivered, or there's only one pack", title='Error', background_color='#1E1E1E')
                else:
                    print("FINALLLL THING: ", objective_function(final_state)[0])
                    print(final_state)
                    visualize_routes_pysimplegui(final_state)
                    sg.popup(f'✅ Optimization Complete! Total Distance: {objective_function(final_state)[1]:.2f} km',
                             title='Result', background_color='#1E1E1E')

        elif event == '🧬 Genetic Algorithm (GA)':
            calculate_ga()

    window.close()

if __name__ == '__main__':
    main()
    # print(calculate_minimum_sa())