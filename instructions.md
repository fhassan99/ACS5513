# How to Enable Running Scripts and Commands in VS Code Terminal

1. **Open the Terminal**  
   - Go to `View` > `Terminal` or press <kbd>Ctrl</kbd>+<kbd>`</kbd>.

2. **Select the Correct Shell**  
   - Click the dropdown arrow in the terminal tab and select your preferred shell (e.g., Command Prompt, PowerShell, Bash).

3. **Allow Script Execution (Windows PowerShell Only)**  
   - If you see a policy error, run the following command in the terminal:
     ```
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
   - Type `Y` to confirm.

4. **Run Your Script or Command**  
   - Type your command (e.g., `python run.py`) and press <kbd>Enter</kbd>.

5. **(Optional) Configure Default Shell**  
   - Open Command Palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>), search for `Terminal: Select Default Profile`, and choose your shell.

Now you can run scripts and commands directly in the VS Code terminal.
