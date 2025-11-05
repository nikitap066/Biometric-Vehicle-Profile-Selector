import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# PROFILES
profiles = {
    1: {"name": "Mum", "seat_recline": 15, "heating": 20, "ambient_light": "medium"},
    2: {"name": "Dad", "seat_recline": 25, "heating": 22, "ambient_light": "low"},
    3: {"name": "Nikita", "seat_recline": 30, "heating": 21, "ambient_light": "medium"},
    4: {"name": "Guest", "seat_recline": 10, "heating": 19, "ambient_light": "high"},
}

# LOAD PROFILE FUNCTION
def load_profile(pid=None):
    if pid is None:  # called by the button
        try:
            pid = int(entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

    profile = profiles.get(pid)
    if not profile:
        messagebox.showerror("Error", "Profile not found.")
        return

    name_var.set(f"{profile['name']}'s Profile")
    recline_var.set(f"{profile['seat_recline']}°")
    heat_var.set(f"{profile['heating']}°C")
    ambient_light_var.set(profile["ambient_light"].capitalize())



# TKINTER UI SETUP
root = tk.Tk()
root.title("Discovery Dashboard Pivi Pro Prototype")
root.geometry("800x420")
root.configure(bg="#0c0d0d")

tk.Label(root, text="Enter Profile Number:", fg="white", bg="#0c0d0d").pack(pady=0)
entry = tk.Entry(root, font=("Helvetica", 16))
entry.pack()
tk.Button(root, text="Load Profile", command=load_profile, bg="#2c2f30", fg="white").pack(pady=5)

name_var = tk.StringVar(value="—")
recline_var = tk.StringVar(value="—")
heat_var = tk.StringVar(value="—")
ambient_light_var = tk.StringVar(value="—")

# navigation frame
left_frame = tk.Frame(root, bg="#1e1f20", bd=1, relief="ridge")
left_frame.pack(side="left", padx=0, pady=0, fill="both", expand=True)
left_frame.pack_propagate(False)
bg_image_left = Image.open("images/winding_road.jpg").resize((266, 500))
bg_photo_left = ImageTk.PhotoImage(bg_image_left)
canvas_left = tk.Canvas(left_frame, width=266, height=400, highlightthickness=0)
canvas_left.pack(fill="both", expand=True)
canvas_left.create_image(0, 0, image=bg_photo_left, anchor="nw")
canvas_left.create_text(133, 50, text="Navigation", fill="#cfae1b",
                   font=("Helvetica", 20, "bold"), anchor="center")

# central profile frame
frame = tk.Frame(root, bg="#1e1f20", bd=1, relief="ridge")
frame.pack(side="left", padx=0, pady=0, fill="both", expand=True)
frame.pack_propagate(False)
tk.Label(frame, textvariable=name_var, fg="#ffffff", bg="#1e1f20", font=("Helvetica", 20, "bold")).pack(pady=30)
tk.Label(frame, text="Seat Recline:", fg="white", bg="#1e1f20", font=("Helvetica", 12)).pack()
tk.Label(frame, textvariable=recline_var, fg="#ffffff", bg="#1e1f20", font=("Helvetica", 12)).pack()
tk.Label(frame, text="Heating:", fg="white", bg="#1e1f20", font=("Helvetica", 12)).pack()
tk.Label(frame, textvariable=heat_var, fg="#ffffff", bg="#1e1f20", font=("Helvetica", 12)).pack()
tk.Label(frame, text="Ambient Lighting:", fg="white", bg="#1e1f20", font=("Helvetica", 12)).pack()
tk.Label(frame, textvariable=ambient_light_var, fg="#ffffff", bg="#1e1f20", font=("Helvetica", 12)).pack()

# media frame
right_frame = tk.Frame(root, bg="#1e1f20", bd=1, relief="ridge")
right_frame.pack(side="left", padx=0, pady=0, fill="both", expand=True)
right_frame.pack_propagate(False)
bg_image_right = Image.open("images/walking.jpg").resize((280, 420))
bg_photo_right = ImageTk.PhotoImage(bg_image_right)
canvas_right = tk.Canvas(right_frame, width=266, height=400, highlightthickness=0)
canvas_right.pack(fill="both", expand=True)
canvas_right.create_image(0, 0, image=bg_photo_right, anchor="nw")
canvas_right.create_text(133, 50, text="Media", fill="#cfae1b",
                   font=("Helvetica", 20, "bold"), anchor="center")

root.mainloop()

