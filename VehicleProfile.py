heating = 0
recline = 0
seat_heating = 0
ambient_lighting = 0

def profileSelection(heating, recline, seat_heating, ambient_lighting):
    print("Heating: ", heating, ", Seat Recline: ", recline, 
          ", Seat Heating: ", seat_heating, ", Ambient Lighting: ", ambient_lighting)


num = input("Enter Number: ")
if num == "1":
    print("Profile 1 selected")
    profileSelection(5, 2, 10, 4)
elif num == "2":
    print("Profile 2 selected")
    profileSelection(2, 6, 7, 3)

