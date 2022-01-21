# pi-bar
The Pi-Bar is a script, which includes a GUI and the ability to use pumps.
The idea behind this is a coffee maker-like machine but for cocktails.

## How to configure

### The main folder is `drinks`

Categories and drinks are being stored just as folders and files.
To create a category, just create a folder, for drinks, create text files.

But of course there are some exceptions. To configure the drinks and configurations, you also have to use files.
The namings of those files are: 
- `preview.txt`: is being used to configure the categories. The file has to be in the category which you want to configure.
- `drinks.txt`: is being used to configure which drinks is on which pump. This file is just in the main folder.

There are also some other special files:
- `background.png`: if detected, this will be your background. This file has to be in the main folder
- `<your_drink>.txt`: contains all the info to create the drink aswell some config. Can be anywhere
- `<your_drink>.png`: the name of the file has to be the same as the name of the .txt file of your drink. But more on that later
- `preview.png`: if detected, this will be the icon of the category the file is in

Now let's go..

### configure the available drinks
In my case I have 6 pumps connected.

Create a new file called `drinks.txt` in your main folder, if there's none.
Then open it and use the following format:

```
<pump number> <Name of the drink>
<pump number> <Name of the drink>
...
```

The first pump is always `1`. If you don't want to use a specific pump, just don't mention it.
In the end it should look something like that:
```
1 Cola
2 Vodka
3 Jack Daniels
4 Water
5 Red Bull
6 Almdudler
```
I wasn't very creative...

For the name you should be able to use any character you want, normally that shouldn't break the app.

### create a category
As mentioned before, to create a category, you just have to create a folder. So just do that.

To configure the name (if you want to use special characters for example) go into that folder and create a file called `preview.txt`.

Here's the format:
```
<category name>
<shown/hidden> (If the category name should be shown; this doesn't effect the icon)
<order> (if empty, it gets sorted by name)
```

And here's an example:
```
Softdrinks
shown
1
```

To add an icon to the category, just put a preview.png into the desired category/folder.

### create a drink
Now to the most important part. You can add drinks anywhere you want, even into the main folder.

To start, just create a .txt file. The name of that file is irrelevant, just don't use any of the ones mentioned above.

Now to the format:
```
<drink name>
<shown/hidden> (if the drink name should be shown; doesn't affect the icon)
<order> (if empty, it gets sorted by name)
<ingredients>
```

Now the ingredients are kinda special, so first here's a small example:

```
Vodka Bull
shown

50 Red Bull
1 warten
10 Vodka
```

In this example we're pouring in 50 cl Red Bull, wait one second, then 10 cl Vodka.
Here I've used one of the special "commands".
Here is a list of all them with explanation.

Command    | Description                                       | Example      | Explanation
---        | ---                                               | ---          | ---
`warten`   | waits the specified amount of time in seconds     | `2 warten`   | waits 2 seconsd
`abwarten` | waits for the last x amount of commands to finish | `3 abwarten` | waits until the last three other commands (includes `warten`) are finished

In the example above I didn't use `abwarten`, but I hope this explains it.

If you want to add an icon to the drink, just create a .png file. The name of that file should be the same as the .txt file.


## How to use the GUI
Since the development is not done yet, the details can change.
I won't make any updates to this file until everything is done.
