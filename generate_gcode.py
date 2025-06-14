
def generate_gcode(length, width, depth_of_cut, tool_diameter, stepover, multiple_depths, feed_rate):
    # Calculate the number of passes needed
    num_passes = int(width / (tool_diameter - stepover)) + 1
    
    # Initialize G-code list
    gcode = []
    
    # Start G-code
    gcode.append("G21 ; Set units to mm")
    gcode.append("G17 ; Select XY plane")
    gcode.append("T1 M6")
    gcode.append("G90 ; Absolute positioning")
    gcode.append("G0 Z5 ; Move to safe Z height")
    gcode.append("M3 S6000 ; Start spindle at 6000 RPM")

    # Loop through each pass
    for j in range(multiple_depths):
         print("pass", j + 1, "of", multiple_depths)
         # for i in range(num_passes):
         current_depth = (depth_of_cut*(j+1))
        
         # Zigzag pattern for face milling
         y = -stepover
         to_zero = False
         gcode.append(f"G1 X{-stepover:.2f} Y{y:.2f} F{feed_rate} ; Move to starting position of first row 0")
         gcode.append(f"G1 Z-{current_depth:.2f} F100 ; Plunge to depth")
         while y <= width + stepover:
            if to_zero:
                gcode.append(f"G1 X{-stepover:.2f} Y{y:.2f} F{feed_rate}; Move to start of row {y}")
                gcode.append(f"G1 X{-stepover:.2f} Y{y + (tool_diameter-stepover):.2f} F{feed_rate} ; Move across to next row")
                to_zero = False
            else:
                gcode.append(f"G1 X{length + stepover:.2f} Y{y:.2f} F{feed_rate} ; Move to end of row {y}")
                gcode.append(f"G1 X{length + stepover:.2f} Y{y + (tool_diameter-stepover):.2f} F{feed_rate} ; Move across to next row")
                to_zero = True
            y += tool_diameter - stepover  
        
         gcode.append("G0 Z5 ; Move to safe Z height")
    
    # End G-code
    gcode.append("G0 Z15 ; Move to safe Z height")
    gcode.append(f"G0 X0 Y0 F{feed_rate}; Move to home position")
    gcode.append("M5 ; Stop spindle")
    gcode.append("M30 ; End of program")
    
    return gcode

# Fill in Parameters for face milling operation
# length of stock, width of stock, depth of cut, tool diameter, stepover, and number of depths passes * depth of cut e.g. 5 passes of 1mm each = 5mm deep
length = 1055  # Length of the stock in mm
width = 250 # Width of the stock in mm
depth_of_cut = 1 # Depth of cut in mm
tool_diameter = 50 # Diameter of the milling tool in mm
stepover = 15 # Stepover in mm
multiple_depths = 2 # Number of depth passes (e.g., 5 passes of 1mm each = 5mm deep)
feed_rate = 1000  # Feed rate in mm/min

gcode = generate_gcode(length, width, depth_of_cut, tool_diameter, stepover, multiple_depths, feed_rate)

# Save G-code to file
with open("face_milling.tap", "w") as f:
    for line in gcode:
        f.write(line + "\n")

print("G-code file 'face_milling.tap' has been generated.")
