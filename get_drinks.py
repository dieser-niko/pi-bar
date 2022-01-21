import os
from ast import literal_eval
import exceptions

keywords = ("warten", "abwarten")


def walk(path="./"):
    folder = os.listdir(path)
    result = [{}, []]
    for item in folder:
        itempath = os.path.join(path, item)
        if os.path.isfile(itempath):
            result[1].append(item)
        else:
            result[0][item] = walk(itempath)
    return result


def get(main_folder="./drinks"):
    try:
        items = walk(main_folder)
    except:
        raise exceptions.WalkError
    try:
        items[1].pop(items[1].index("drinks.txt"))
    except ValueError:
        raise exceptions.PumpCheckError
    if "background.txt" in items[1]:
        items[1].pop(items[1].index("background.txt"))
    try:
        with open(os.path.join(main_folder, "drinks.txt"), "r", encoding="utf-8") as fobj:
            file = fobj.read().split("\n")
    except:
        raise exceptions.DrinkReadError
    drinks = process_drink_config(file)
    try:
        result = {"items": Category(**import_infos(items, main_folder)).export(drinks), "drinks": drinks}
    except:
        raise exceptions.ExportError
    return result


def import_cat_config(path):
    with open(path, "r", encoding="utf-8") as fobj:
        process = fobj.read().split("\n")
    return {"name": process[0], "text": (process[1] != "hidden"), "order": literal_eval(process[2])}


def import_drink_config(path):
    with open(path, "r", encoding="utf-8") as fobj:
        process = fobj.read().split("\n")
    return {"name": process[0], "text": (process[1] == "shown"), "order": literal_eval(process[2]),
            "config": process_drink_config(process[3:])}


def process_drink_config(config) -> dict:
    return {" ".join(x.split(" ")[1:]): x.split(" ")[0] for x in config}


def import_infos(items, path):
    result = {"items": []}

    # first, all the folders are being converted to classes, then added to the "items" list.
    for item in items[0]:
        result["items"].append(
            Category(**{**{"name": item}, **import_infos(items[0][item], os.path.join(path, item))}))

    # then all files are getting processed
    for item in items[1]:
        # preview.png and .txt are special files that are meant for the category we are currently in.
        # if they get found, they get added to the result and the configuration will be read and added.
        if item == "preview.png":
            result["preview"] = os.path.join(path, "preview.png")
        elif item == "preview.txt":
            result.update(import_cat_config(os.path.join(path, "preview.txt")))
        elif item.endswith(".txt"):
            # the filename of the preview has to be the same name as the .txt (but with .png instead)
            preview = ".".join(os.path.join(path, item).split(".")[:-1]) + ".png"
            # if it doesn't exist, then just don't use a preview.
            if not os.path.isfile(preview):
                preview = ""

            # {**{[...]}, **{[...]}} this is a way to merge two dictionaries together.
            result["items"].append(Drink(**{"preview": preview}, **import_drink_config(os.path.join(path, item))))
    return result


class Item:
    def __init__(self, name, preview, order, text):
        self.name = name
        self.preview = preview
        self.order = order
        self.text = text


class Category(Item):
    def __init__(self, name="", preview="", order=None, text=True, items=None):
        super().__init__(name, preview, order, text)

        self.items = list() if items is None else items

    def export(self, drinks):
        """
        The list sorting is kinda complicated, so here the explanation:
        First, the for loop creates a tuple in a big tuple, which includes itself.
        First item is name, the second one goes deeper (recursive function).
        Then it gets sorted. If the order is given, then it will be sorted after the order. Can be a float or int.
        If the order is None, then it will be sorted after the name of the category.
        Then both sorted dictionaries will be merged, so that the orders are still in front of the names.
        
        Both drinks and categories are in the same dictionary
        """
        export = [x.export(drinks) for x in self.items]
        if any(export):
            return {"name": self.name,
                    "preview": self.preview,
                    "order": self.order,
                    "text": self.text,
                    "items": sorted((x for x in export if x and x["order"] is not None), key=lambda a: a["order"]) + \
                             sorted((x for x in export if x and x["order"] is None), key=lambda a: a["name"])}


class Drink(Item):
    def __init__(self, name="", preview="", config="", order=None, text=True):
        super().__init__(name, preview, order, text)
        self.config = config

    def export(self, drinks):
        if all([any([x == y or y in keywords for x in drinks]) for y in self.config]):
            return {"name": self.name,
                    "preview": self.preview,
                    "config": self.config,
                    "order": self.order,
                    "text": self.text}

