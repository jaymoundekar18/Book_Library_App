# Creating an Executable Application using Pyinstaller
#### Converting the VBL Python code into an executable program, you can use PyInstaller. Follow these steps:

## Prerequisites:
* Ensure PyInstaller is installed. You can install it using pip:
   ```bash
   python -m pip install pyinstaller
   ```

### Add the CTkDatePicker to the python packages
* Move the CTkDatePicker directory to your installed python's site-package directory
* The site-package will be as
  ```
  Python/
  ├── DLL
  ├── Doc
  ├── include
  :
  :
  :
  ├── Lib
      └── .....
      └── .....
      └── site-packages
              └── .....
              └── .....
              └── CTkDatePicker
  ├── share
  ├── tcl
  ├── Tools
  ```

### Generating the Executable:
1. Open the Command Prompt or terminal and navigate to the directory where the VBL_App.py is located.
2. Run the following command: 
  ```bash
    pyinstaller --add-data "Python\Lib\site-packages\CTkDatePicker":"CTkDatePicker" --add-data "Python\Lib\site-packages\pandas":"pandas" --add-data "Python\Lib\site-packages\pandastable":"pandastable" --add-data "Python\Lib\site-packages\PIL":"PIL" --add-data "Python\Lib\site-packages\cv2":"cv2" --add-data "Python\Lib\site-packages\pygame":"pygame" --add-data "Python\Lib\sqlite3":"sqlite3" --add-data "Python\Lib\datetime.py":"datetime" --add-data "Python\Lib\textwrap.py":"textwrap" --add-data "Book Reading\Connect_DB.py":"Connect_DB" -i bicon.ico -w --onefile VBL_App.py
  ``` 
  Replace **path to** with the actual path to the module on your system.<br>
*or*<br>
**Refer ``` pyinstaller.txt```** 

3. The **VBL_App.py** file will be converted into an executable. After the process completes:
   * The executable will be located in the dist folder of the project directory.
   * Additional files might appear in the build folder.
  
### Project Directory Structure After Generating Executable
```
  Book Reading/
  ├── img
  ├── VBL_App.py
  ├── Connect_DB.py
  ├── VBL_App.spec
  ├── bicon.ico
  ├── build/
        └── .....
  ├── dist/
        └── VBL_App.exe
  
  ```
### Running the Executable:
   * Navigate to the dist folder:
     ```bash
     cd dist/
     ```
   * Run the executable:
     ```bash
     VBL_App.exe
     ```


## Important Note:
1. Ensure that all required modules *(e.g., sqlite3, pandastable, CTkDatePicker)* are properly installed in your Python environment before creating the executable.
2. If you're using a virtual environment, specify the correct paths to the libraries in the *--add-data* flags.
3. After the executable is create and while running the executable program the app is getting crashed, then used the below command to get make the windowed executable to see the error logs
   ```bash
    pyinstaller --add-data "Python\Lib\site-packages\CTkDatePicker":"CTkDatePicker" --add-data "Python\Lib\site-packages\pandas":"pandas" --add-data "Python\Lib\site-packages\pandastable":"pandastable" --add-data "Python\Lib\site-packages\PIL":"PIL" --add-data "Python\Lib\site-packages\cv2":"cv2" --add-data "Python\Lib\site-packages\pygame":"pygame" --add-data "Python\Lib\sqlite3":"sqlite3" --add-data "Python\Lib\datetime.py":"datetime" --add-data "Python\Lib\textwrap.py":"textwrap" --add-data "Book Reading\Connect_DB.py":"Connect_DB" -i bicon.ico VBL_App.py
   ```
