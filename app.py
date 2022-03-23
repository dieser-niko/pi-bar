from flask import Flask, redirect, url_for, jsonify, render_template, send_file
from markupsafe import escape

from get_drinks import get

app = Flask(__name__)

data = get()

def convert_to_link(path):
    return "/".join([text.replace("/", "%2F").replace("?", "%3F") for text in path])

def convert_from_link(path):
    return [text.replace("%2F", "/").replace("%3F", "?") for text in path.split("/")]



@app.route("/")
def generate():
    global data
    data = get()
    # do stuff
    return redirect(url_for("drinks_redir"))

@app.route("/drinks/")
def drinks_redir():
    return route_item("/")

@app.route("/drinks/<path:item>")
def route_item(item):
    if item.endswith("/"):
        return manage_menu(item[:-1])
    else:
        return manage_drink(item)


def get_cat(item, path: list):
    return get_cat([x for x in item["items"] if x["filename"] == path[0] and "items" in x][0], path[1:]) if path else item

def manage_menu(raw_path):
    path = convert_from_link(raw_path) if raw_path else []
    items = get_cat(data, path)["items"]
    return render_template("menu.htm",
                           items=[{"description": item["name"],
                                   "picture": ("/img/" + "/".join(path + [item["filename"]]) + ("/" if "items" in item else "")) if item["preview"] else None,
                                   "link": "/drinks/" + "/".join(path + [item["filename"]]) + ("/" if "items" in item else "")} for item in items])


def get_drink(item, path: list):
    return get_drink([x for x in item["items"] if x["filename"] == path[0] and ("items" in x) ^ (len(path) == 1)][0], path[1:]) if path else item

def manage_drink(raw_path):
    path = convert_from_link(raw_path)
    return escape(get_drink(data, path))


@app.route("/img/<path:item>")
def route_img(item):
    path = convert_from_link(item)
    return send_file((get_cat(data, path[:-1]) if item.endswith("/") else get_drink(data, path))["preview"], mimetype="image/png")



@app.route("/api/<path:item>/start")
def start_drink(item):
    print(item.split("/"))
    return escape(item)

@app.route("/api/<path:item>/stop")
def stop_drink(item):
    print(item.split("/"))
    return "", 204


#@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("generate"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)