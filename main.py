from get_drinks import get as get_drinks
from pump_control import pump_control
drinks = get_drinks()

def get_item(items, path: list):
    return 

def show_item(items, path):
    if "items" in item:  # if items in dict, then this is a category
        show_category(item)
    else:
        show_drink(item)

def show_category(item):
    