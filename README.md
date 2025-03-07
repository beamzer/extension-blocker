# File Blocker

This Windows application blocks the opening of potentially dangerous file extensions (like .js) and displays a warning window instead. The program collects information about the blocked file and stores it in a local log file.

## Installation

### For users
1. Download the latest release of this application
2. Extract the ZIP file to your desired location
3. Follow the instructions under "Associating .js files"

### For developers
If you want to modify or build the program yourself:

1. Install Python 3.8 or higher (Anaconda recommended)
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   pip install pyinstaller
   ```
3. Build the executable:
   ```
   pyinstaller --onefile --noconsole --icon=NONE file_blocker.py
   ```

   The PyInstaller options used:
   - `--onefile`: Creates a single executable file
   - `--noconsole`: Prevents a console window from appearing
   - `--icon=NONE`: Uses default icon (you can specify a custom .ico file)

   After building:
   - The executable will be created in the `dist` folder
   - You can safely delete the `build` folder and `.spec` file
   - Copy `run_blocker.bat` to the same folder as the executable

### Associating .js files

To associate .js files with the program:

1. Open Windows Explorer
2. Right-click on a .js file
3. Choose "Open with" > "Choose another app"
4. Check "Always use this app to open .js files"
5. Click "More apps" or "Look for another app"
6. Click "Browse" to locate an app on your PC
7. Navigate to the location of `run_blocker.bat` where you installed the program
8. Select `run_blocker.bat`
9. Click "Open"

## Configuration

The program saves all blocked files in a local log file named `file_blocker.log`. This file is created in the same directory as the program.

## Features

- Blocks opening of .js files
- Shows a warning window with:
  - Filename
  - SHA1 hash of the file
  - IP address of the computer
  - Time of blocking
- Stores all information in a local log file
- Closes automatically after closing the warning window
- Warning window cannot be minimized or maximized
- Warning window stays on top of other windows
- Works on any Windows system without additional software

## Log File

All blocked files are logged in `file_blocker.log` with the following information:
- Time of blocking
- Filename
- SHA1 hash of the file
- IP address of the computer

## Testing

To test the program, you can use the following command:
```
run_blocker.bat "path\to\test.js"
```

## Removing File Association

To remove the file association, you can either manually modify the Windows Registry or run the following PowerShell command:

```powershell
Remove-Item -Path "HKCU:\Software\Classes\.js" -Recurse
Remove-Item -Path "HKCU:\Software\Classes\JSFile.Blocker" -Recurse
```

## Distribution

To distribute the application:

1. Build the executable using PyInstaller as described above
2. Create a ZIP file containing:
   - The executable (`file_blocker.exe`) from the `dist` folder
   - The batch file (`run_blocker.bat`)
   - This README.md file
3. Users only need to extract the ZIP and follow the installation instructions 