import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, ImageFilter, ImageTk


class BlurScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("BlurScreen Control")
        
        # Enable Select Mode button with Ctrl+E shortcut
        self.select_button = tk.Button(root, text="Enable Select Mode (Ctrl+E)", command=self.enable_select_mode)
        self.select_button.pack(pady=10)

        # Remove All Blurs button with Ctrl+R shortcut
        self.clear_button = tk.Button(root, text="Remove All Blurs (Ctrl+R)", command=self.remove_blur_windows)
        self.clear_button.pack(pady=10)

        # Keyboard shortcuts
        self.root.bind('<Control-e>', lambda event: self.enable_select_mode())
        self.root.bind('<Control-r>', lambda event: self.remove_blur_windows())

        self.select_mode = False
        self.select_overlay = None
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.blur_windows = []

    def enable_select_mode(self):
        if not self.select_mode:
            self.select_mode = True
            self.select_overlay = tk.Toplevel(self.root)
            self.select_overlay.withdraw()  # Hide the window
            self.select_overlay.attributes('-fullscreen', True)  # Fullscreen to cover the screen
            self.select_overlay.attributes('-alpha', 0.5)  # Transparent overlay
            self.select_overlay.bind("<Button-1>", self.on_button_press)
            self.select_overlay.bind("<B1-Motion>", self.on_mouse_drag)
            self.select_overlay.bind("<ButtonRelease-1>", self.on_button_release)

            # Capture the initial screen image
            self.screenshot = ImageGrab.grab()
            self.display_image()

            # Show the window after configuration
            self.select_overlay.deiconify()

    def display_image(self):
        # Display the screenshot on the overlay
        self.tk_image = ImageTk.PhotoImage(self.screenshot)
        self.select_overlay_canvas = tk.Canvas(self.select_overlay, width=self.screenshot.width, height=self.screenshot.height)
        self.select_overlay_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.select_overlay_canvas.pack(fill=tk.BOTH, expand=True)

    def on_button_press(self, event):
        # Store the starting coordinates for the rectangle
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.select_overlay_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        # Update the rectangle as the mouse is dragged
        self.select_overlay_canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        # Once the mouse button is released, hide the selection overlay and create the blur overlay
        x1, y1, x2, y2 = self.select_overlay_canvas.coords(self.rect)
        self.create_blur_overlay(int(x1), int(y1), int(x2), int(y2))

        # Close the selection overlay
        self.select_overlay.destroy()
        self.select_mode = False

    def create_blur_overlay(self, x1, y1, x2, y2):
        # Create a new transparent window for the blur effect
        blur_window = tk.Toplevel(self.root)
        blur_window.withdraw()  # Hide the window
        blur_window.geometry(f"{x2-x1}x{y2-y1}+{x1}+{y1}")
        blur_window.overrideredirect(True)  # Remove window decorations
        blur_window.attributes('-alpha', 1.0)  # Fully opaque
        blur_window.attributes('-topmost', True)  # Keep on top

        # Capture the blurred area from the screenshot
        area = self.screenshot.crop((x1, y1, x2, y2))
        blurred_area = area.filter(ImageFilter.GaussianBlur(10))
        blurred_image = ImageTk.PhotoImage(blurred_area)

        # Display the blurred image in the new window
        label = tk.Label(blur_window, image=blurred_image)
        label.image = blurred_image  # Keep a reference to avoid garbage collection
        label.pack()

        # Store the window reference
        self.blur_windows.append(blur_window)

        # Allow for new selections
        self.select_button.config(state=tk.NORMAL)

        # Show the window after configuration
        blur_window.deiconify()

    def remove_blur_windows(self):
        # Destroy all blur windows and clear the list
        for window in self.blur_windows:
            window.destroy()
        self.blur_windows.clear()
        print("All blur windows removed.")


# Create the main application window
root = tk.Tk()
app = BlurScreen(root)
root.mainloop()
