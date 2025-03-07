# File Blocker

This Windows application blocks the opening of potentially dangerous file extensions (like .js) and displays a warning window instead. The program collects information about the blocked file, stores it in a local log file and optionally sends this information to a syslog server. At the moment the syslog server is passed as a commandline argument to make it easy to test this functionality. If you want use this in a production setting, it's best to configure the syslog information in the python script, because association of extensions to a program with a commandline argument is more complex.

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
   pyinstaller --onefile --noconsole --icon=file_blocker.ico file_blocker.py
   ```

   The PyInstaller options used:
   - `--onefile`: Creates a single executable file
   - `--noconsole`: Prevents a console window from appearing
   - `--icon=file_blocker.ico`: Uses the custom icon

   After building:
   - The executable will be created in the `dist` folder
   - You can safely delete the `build` folder and `.spec` file

### Associating .js files

To associate .js files with the program:

1. Open Windows Explorer
2. Right-click on a .js file
3. Choose "Open with" > "Choose another app"
4. Check "Always use this app to open .js files"
5. Click "More apps" or "Look for another app"
6. Click "Browse" to locate an app on your PC
7. Navigate to the location of `file_blocker.exe` where you installed the program
8. Select `file_blocker.exe`
9. Click "Open"

## Configuration

The program saves all blocked files in a log file named `file_blocker.log`. This file is created in `C:\ProgramData\FileBlocker\`. The program will automatically create this directory if it doesn't exist.

## Command Line Options

The program supports the following command line options:

- `file`: The file to block (required when not using --register)
- `--syslog HOSTNAME`: Enable syslog and specify the syslog server hostname
- `--port PORT`: Specify the syslog server port (default: 514)
- `--register`: Register file association

Examples:
```
# Block a file with syslog enabled
file_blocker.exe "test.js" --syslog syslog.example.com

# Block a file with custom syslog port
file_blocker.exe "test.js" --syslog syslog.example.com --port 1514

# Register file association
file_blocker.exe --register
```

## Features

- Blocks opening of .js files
- Shows a warning window with:
  - Filename
  - SHA1 hash of the file
  - IP address of the computer
  - Time of blocking
- Stores all information in a central log file
- Optional syslog server support
- Closes automatically after closing the warning window
- Warning window cannot be minimized or maximized
- Warning window stays on top of other windows
- Works on any Windows system without additional software

## Log File

All blocked files are logged in `C:\ProgramData\FileBlocker\file_blocker.log` with the following information:
- Time of blocking
- Filename
- SHA1 hash of the file
- IP address of the computer

If syslog is enabled, the same information is also sent to the configured syslog server.

## Testing

To test the program, you can use the following command:
```
file_blocker.exe "path\to\test.js"
```

Or with syslog enabled:
```
file_blocker.exe "path\to\test.js" --syslog syslog.example.com
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
   - This README.md file
3. Users only need to extract the ZIP and follow the installation instructions 
