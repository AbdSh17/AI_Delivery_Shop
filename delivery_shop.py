from operator import index

import pandas as pd
import os

# ============================ Global ============================

# add
vehicles = pd.read_csv('vehicles.csv') if os.path.exists('vehicles.csv') else pd.DataFrame(
    columns=['vehicle_id', 'capacity']).to_csv('vehicles.csv', index=False)

packages = pd.read_csv("packages.csv") if os.path.exists('packages.csv') else pd.DataFrame(
    columns=['package_id', 'dest_x', 'dest_y', 'weight', 'priority']).to_csv('packages.csv', index=False)
# ============================ Global ============================

def add_package():
    global packages
    try:
        pack_id = len(packages) + 1
    except Exception:
        pack_id = 1

    try:
        dest_x = int(input("\nEnter X (0-100): "))
        if not 0 <= dest_x <= 100:
            print("Please 0 <= X <= 100\n")
            return False
    except Exception:
        print("Please enter an Destination as an Integer\n")
        return False

    try:
        dest_y = int(input("\nEnter Y (0 - 100): "))
        if not 0 <= dest_y <= 100:
            print("Please 0 <= Y <= 100\n")
            return False
    except Exception:
        print("Please enter an Destination as an Integer\n")
        return False

    try:
        weight = int(input("\nEnter the Weight: "))
    except Exception:
        print("Please enter an Weight as an Integer\n")
        return False

    try:
        priority = int(input("\nEnter The priority (1-5): "))
        if not 1 <= priority <= 5:
            print("Please enter a priority between 1-5\n")
            return False
    except Exception:
        print("Please enter an Priority as an Integer\n")
        return False

    new_package = pd.DataFrame({
        "package_id": [f"p{str(pack_id)}"],
        "dest_x": [dest_x],
        "dest_y": [dest_y],
        "weight": [weight],
        "priority": [priority],
        "is_delivered": [False]
    })
    packages = pd.concat([packages, new_package], ignore_index=True)
    packages.to_csv("packages.csv", index= False)
    return True

def drop_package(pack_id):
    global packages
    if pack_id not in packages["package_id"].values:
        return False

    packages = packages[packages["package_id"] != pack_id]
    packages.to_csv("packages.csv", index= False)
    return True

def add_vehicle():
    global vehicles
    try:
        vehicle_id = len(vehicles) + 1
    except Exception:
        vehicle_id = 1

    try:
        capacity = int(input("\nEnter capacity: "))
    except Exception:
        print("Please enter an capacity as an Integer\n")
        return False

    new_vehicle = pd.DataFrame({
        "vehicle_id": [f"v{str(vehicle_id)}"],
        "capacity": [capacity],
        "is_available": [True]
    })
    vehicles = pd.concat([vehicles, new_vehicle], ignore_index=True)
    vehicles.to_csv("vehicles.csv", index= False)
    return True

def drop_vehicle(vehicle_id):
    global vehicles
    if vehicle_id not in vehicles["vehicle_id"].values:
        return False

    vehicles = vehicles[vehicles["vehicle_id"] != vehicle_id]
    vehicles.to_csv("vehicles.csv", index= False)
    return True

if __name__ == '__main__':

    while True:
        print("\n1. Add package\n2. Drop package\n3. Add vehicle\n4. Drop vehicle\n5. Break")
        choice = input("Choose (1 or 2): ")
        if choice == '1':
            print(packages)
            print(packages) if add_package() else print("Failed to add the package")

        elif choice == '2':
            print(packages)
            pack_id = input("\nEnter pack ID: ")
            print(packages) if drop_package(pack_id) else print("Failed to drop the package")

        elif choice == '3':
            print(vehicles)
            print(vehicles) if add_vehicle() else print("Failed to add the Vehicle")

        elif choice == '4':
            print(vehicles)
            vehicle_id = input("\nEnter pack ID: ")
            print(vehicles) if drop_vehicle(vehicle_id) else print("Failed to drop the vehicle")


        elif choice == '5' or choice == 'q':
            break
        else:
            print("Not a valid option\n")