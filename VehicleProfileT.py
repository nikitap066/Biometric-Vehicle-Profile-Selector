import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import HandTrackingModule as htm
import time
import threading

# PROFILES
profiles = {
    1: {"name": "Mum", "seat_recline": 15, "heating": 20, "ambient_light": "medium"},
    2: {"name": "Dad", "seat_recline": 25, "heating": 22, "ambient_light": "low"},
    3: {"name": "Nikita", "seat_recline": 30, "heating": 21, "ambient_light": "medium"},
    4: {"name": "Guest", "seat_recline": 10, "heating": 19, "ambient_light": "high"},
}

numberOfFingers = 0  # shared finger variable

# LOAD PROFILE FUNCTION
def load_profile(pid=None): 
    if pid == 5: # guest for both 4 and 5 fingers
        pid = 4 

    profile = profiles.get(pid)
    if not profile:
        return  # no profile for this number

    name_var.set(f"{profile['name']}'s Profile")
    recline_var.set(f"{profile['seat_recline']}°")
    heat_var.set(f"{profile['heating']}°C")
    ambient_light_var.set(profile["ambient_light"].capitalize())


# TKINTER UI SETUP
root = tk.Tk()
root.title("Discovery Dashboard Pivi Pro Prototype")
root.geometry("800x420")
root.configure(bg="#0c0d0d")

# tk.Label(root, text="Enter Profile Number:", fg="white", bg="#0c0d0d").pack(pady=0)
# entry = tk.Entry(root, font=("Helvetica", 16))
# entry.pack()
# tk.Button(root, text="Load Profile", command=load_profile, bg="#2c2f30", fg="white").pack(pady=5)

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


# HAND TRACKING THREAD
def run_hand_tracking():
    global numberOfFingers

    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    wCam, hCam = 500, 420

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0

    detector = htm.handDetector(detectionCon=0.7)

    while True:
        success, img = cap.read()
        if not success:
            break

        fingers = {"4": 0, "8": 0, "12": 0, "16": 0, "20": 0}
        img = detector.findHands(img)
        landmarks, bbox = detector.findPosition(img, draw=False)

        if len(landmarks) != 0:
            if landmarks[4][1] > landmarks[3][1]: fingers["4"] = 1
            if landmarks[8][2] <= landmarks[6][2]: fingers["8"] = 1
            if landmarks[12][2] <= landmarks[10][2]: fingers["12"] = 1
            if landmarks[16][2] <= landmarks[14][2]: fingers["16"] = 1
            if landmarks[20][2] <= landmarks[18][2]: fingers["20"] = 1

        numberOfFingers = sum(fingers.values())

        # draw finger count
        cv2.rectangle(img, (25, 150), (100, 400), GREEN, cv2.FILLED)
        cv2.putText(img, f'{numberOfFingers}', (35, 300), cv2.FONT_HERSHEY_PLAIN, 6, BLUE, 2)

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime) if cTime != pTime else 0
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, BLUE, 2)

        cv2.imshow("Camera", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# AUTO UPDATE FUNCTION
def auto_update():
    if numberOfFingers in [1, 2, 3, 4, 5]:
        load_profile(numberOfFingers)
    root.after(1000, auto_update)  # check every 1 second


# START THREADS + LOOP
threading.Thread(target=run_hand_tracking, daemon=True).start()
root.after(1000, auto_update)  # start auto-updating the UI
root.mainloop()
