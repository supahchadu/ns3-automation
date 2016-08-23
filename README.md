### ns-3-automation
NS-3.x.x helper for automating  `waf commands` and computing the datas in it. The given data from two files should always have `two columns` separated by `tab-key`to compute their ratios from one another. The program will output the data for R.

#### Installation:
- Put the folder inside your Ns-3.x.x
- Rename this folder as `OUTPUT_FILES` to avoid having errors in the future
- Open the program `graph.py` and edit `directoryPath` variable to the path of your `ns-3.x.x` folder.
- By default, `os.system(wafcommand)` is commented. Uncomment it if your going to execute string of commands from `waf-commands.txt`

#### Directions when using the program:
- For Command automation, make sure you put the command inside `waf-commands.txt`
- Each commands are separated with `\n` or by hitting `Enter` or else the program won't read it.
- Put the name of the filename of the expected file you wish to compute inside the `files-to-graph.txt`


