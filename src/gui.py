import tkinter as tk
import customtkinter  # Import customtkinter for a modern looking GUI
from PIL import Image, ImageTk  # For image manipulation if needed
import sys
import subprocess  # To run the external Python script
import threading  # To run the script in a separate thread and keep the GUI responsive

# Initialize the process variable globally to keep track of the external process
process = None
log_file_path = (
    "script_log.txt"  # Path to save the log file for output and error messages
)


def run_script():
    """
    Function to start the external Python script ('jFlipper.py').
    It retrieves parameters from the GUI, runs the script, and logs its output.
    """
    global process  # We declare 'process' as global so we can stop it later

    def target():
        """
        Inner function to run the external script in a separate thread.
        This allows the GUI to remain responsive.
        """
        global process
        # Get values from the GUI for click and sleep delays
        click_delay = delay_spinbox.get()
        sleep_delay = sleep_spinbox.get()

        # Convert click_delay and sleep_delay to float, set default if invalid input
        try:
            click_delay = float(click_delay)
        except ValueError:
            click_delay = 0.7  # Default click delay if input is invalid

        try:
            sleep_delay = float(sleep_delay)
        except ValueError:
            sleep_delay = 0.7  # Default sleep delay if input is invalid

        # Define the path to the script to be executed
        script_path = "jFlipper.py"  # Replace with the path to your script

        # Open the log file in write mode ("w" overwrites the file each time)
        with open(log_file_path, "w") as log_file:
            # Run the script using subprocess and pass click_delay and sleep_delay as arguments
            process = subprocess.Popen(
                ["python", script_path, str(click_delay), str(sleep_delay)],
                stdout=subprocess.PIPE,  # Capture standard output
                stderr=subprocess.PIPE,  # Capture error output
                text=True,  # Ensure output is captured as text, not bytes
            )

            # Write standard output from the script to the log file
            for line in process.stdout:
                log_file.write(line)

            # Write error output (if any) to the log file
            for line in process.stderr:
                log_file.write(line)

            # Close stdout and stderr after capturing output
            process.stdout.close()
            process.stderr.close()
            process.wait()  # Wait for the process to finish

    # Run the external script in a separate thread to prevent the GUI from freezing
    thread = threading.Thread(target=target)
    thread.start()  # Start the thread


def stop_script():
    """
    Function to stop the running script (if it is still running).
    It also writes a "Script stopped" message to the log file.
    """
    global process  # Reference the global process variable
    if process and process.poll() is None:  # Check if the process is running
        process.terminate()  # Terminate the running process
        # Append the "Script stopped" message to the log file
        with open(log_file_path, "a") as log_file:
            log_file.write("\nScript stopped.\n")


# GUI Setup using customtkinter for a modern interface
customtkinter.set_appearance_mode("dark")  # Set dark mode appearance
customtkinter.set_default_color_theme("dark-blue")  # Use dark-blue theme

# Create the main window
root = customtkinter.CTk()
root.geometry("720x60")  # Set window size

root.title("jFlipper")  # Set the window title

root.iconbitmap("images/logo.ico")  # Set the window icon (replace with your icon path)

# ASCII art for display in console (optional)
ascii_art = """
<ASCII art here>
"""

print(ascii_art)  # Print the ASCII art in the console (not in the GUI)

# Create a frame to hold the buttons
button_frame = customtkinter.CTkFrame(master=root)
button_frame.pack(pady=10, padx=10)  # Add padding around the frame

# Create the Run button, which starts the script when clicked
run_button = customtkinter.CTkButton(
    button_frame, text="Run Script", command=run_script
)
run_button.pack(side="left", padx=10, pady=10)  # Add padding to position the button

# Create the Stop button, which stops the script when clicked
stop_button = customtkinter.CTkButton(
    button_frame, text="Stop Script", command=stop_script
)
stop_button.pack(side="left", padx=10, pady=10)  # Add padding to position the button

# Create a frame to hold the delay-related widgets (click and sleep delay spinboxes)
delay_frame = customtkinter.CTkFrame(master=button_frame)
delay_frame.pack(side="right", padx=10, pady=10, anchor="e")  # Anchor to the right

# Label for click delay input
delay_label = customtkinter.CTkLabel(delay_frame, text="Click Delay (sec):")
delay_label.pack(side="left", padx=5)

# Spinbox for click delay (default is 0.7, range is 0.7 to 3 seconds)
delay_spinbox = tk.Spinbox(
    delay_frame,
    from_=0.7,  # Minimum value
    to=3,  # Maximum value
    increment=0.1,  # Step size
    format="%.1f",  # Format as 1 decimal float
    width=8,  # Width of the spinbox
)
delay_spinbox.pack(side="left", padx=5)  # Add padding
delay_spinbox.delete(0, tk.END)  # Clear default text in the spinbox
delay_spinbox.insert(0, "0.7")  # Insert the default value

# Add another frame for sleep delay input
sleep_frame = customtkinter.CTkFrame(master=button_frame)
sleep_frame.pack(side="right", padx=10, pady=10, anchor="e")  # Anchor to the right

# Label for sleep delay input
sleep_label = customtkinter.CTkLabel(sleep_frame, text="Sleep Delay (sec):")
sleep_label.pack(side="left", padx=5)

# Spinbox for sleep delay (default is 1.0, range is 0.1 to 5 seconds)
sleep_spinbox = tk.Spinbox(
    sleep_frame,
    from_=0.1,  # Minimum value
    to=5,  # Maximum value
    increment=0.1,  # Step size
    format="%.1f",  # Format as 1 decimal float
    width=8,  # Width of the spinbox
)
sleep_spinbox.pack(side="left", padx=5)  # Add padding
sleep_spinbox.delete(0, tk.END)  # Clear default text in the spinbox
sleep_spinbox.insert(0, "1.0")  # Insert the default value

# Bind events to get updated click and sleep delays when user changes the spinbox values
delay_spinbox.bind("<FocusOut>", lambda e: get_click_delay())
sleep_spinbox.bind("<FocusOut>", lambda e: get_sleep_delay())


# Function to get and update the click delay from the spinbox
def get_click_delay():
    global click_delay  # Reference the global variable for click delay
    try:
        click_delay = float(delay_spinbox.get())  # Get the value from the spinbox
    except ValueError:
        click_delay = 0.7  # Set default if the input is invalid


# Function to get and update the sleep delay from the spinbox
def get_sleep_delay():
    global sleep_delay  # Reference the global variable for sleep delay
    try:
        sleep_delay = float(sleep_spinbox.get())  # Get the value from the spinbox
    except ValueError:
        sleep_delay = 0.7  # Set default if the input is invalid


# Ensure the initial values for click and sleep delays are fetched at the start
get_click_delay()
get_sleep_delay()

# Start the main event loop for the GUI
root.mainloop()
