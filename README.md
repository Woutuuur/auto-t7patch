# Black Ops III auto patcher for T7 Patch
Script that launches both the T7 Patch and Black Ops III together and closes the T7 patch once you quit the game.

The T7 patch is a community patch for Call of Duty: Black Ops III that patches a number of RCE exploits and fixes smaller miscellaneous issues with the game. It is available for download here here: https://github.com/shiversoftdev/t7patch.

### Usage
First, isntall the required dependencies:
```ps1
pip install -r requirements.txt
```

Then, run the script:
```ps1
python launch_patched.py --t7 "C:\path\to\t7_patch.exe"
```

The above command assumes default Steam and game installation locations. The command below shows how to run the script with different locations for the game and Steam:
```ps1
python launch_patched.py --t7 "C:\path\to\t7_patch.exe" --game "X:\path\to\BlackOps3.exe" --steam "Y:\path\to\Steam.exe"
```

Note: you can run `python launch_patched.py --help` for more information.

### Adding to Steam
The easiest way to add the script to Steam is by converting the script to an executable and creating a shortcut to it. Converting the script to an executable requires `pyinstaller`, which you can install by running `pip install pyinstaller`. 

1. Convert the script to a `.exe`:
    ```ps1
    pyinstaller --onefile .\launch_patched.py --uac-admin --noconsole
    ```
    Note: Your anti-virus might flag the `.exe` as a virus. Either disable it or add an exception for this file / directory.
2. Right click `launch_patched.exe` in the `dist` directory and click "properties". In the "target" field, at the end of the existing string, add your command line arguments. Adding your t7 executable using `--t7` is required (see [usage](#usage)).
3. Add a random `.exe` to Steam. Follow Steam's instructions on how to do this [here](https://help.steampowered.com/en/faqs/view/4B8B-9697-2338-40EC).
4. Right click the newly added item, go to properties and change the "target" to point to your shortcut (`.lnk` file).

