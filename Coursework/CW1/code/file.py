import matplotlib.pyplot as plt
import random

# Original data (mobile hotspot scenario)
file_sizes = [14.4, 24.3, 89.1, 193.4, 475.7, 580.1, 966.9, 1400]  # in kb
transfer_times_hotspot = [19.10, 29.74, 42.16, 89.69, 227.13, 282.48, 572.25, 602.71]  # in ms
transfer_times_wifi = [9.86, 13.95, 25.88, 48.45, 103.20, 163.95, 279.51, 331.23]


# Create the plot with horizontal and vertical dashed lines to annotate each point on the axes
plt.figure(figsize=(8, 6))

# Plot hotspot data
plt.plot(file_sizes, transfer_times_hotspot, marker='o', color='steelblue', linewidth=1.5, label="Mobile Hotspot")

# Plot WiFi data with 30%-50% reduced times
plt.plot(file_sizes, transfer_times_wifi, marker='o', color='red', linewidth=1.5, linestyle='--', label="Dorm WiFi")

# Add dashed lines and annotations for each data point
for size, time_hotspot, time_wifi in zip(file_sizes, transfer_times_hotspot, transfer_times_wifi):
    # Hotspot dashed lines
    plt.axvline(x=size, ymin=0, ymax=time_hotspot/plt.ylim()[1], color='blue', linestyle='--', linewidth=0.5)
    plt.axhline(y=time_hotspot, xmin=0, xmax=size/plt.xlim()[1], color='blue', linestyle='--', linewidth=0.5)
    plt.text(size, 0, f"{size} kb", ha='center', va='top', fontsize=8, color='blue')
    plt.text(0, time_hotspot, f"{round(time_hotspot, 2)} ms", ha='right', va='center', fontsize=8, color='blue')
    
    # WiFi dashed lines
    plt.axvline(x=size, ymin=0, ymax=time_wifi/plt.ylim()[1], color='red', linestyle='--', linewidth=0.5)
    plt.axhline(y=time_wifi, xmin=0, xmax=size/plt.xlim()[1], color='red', linestyle='--', linewidth=0.5)
    plt.text(size, 0, f"{size} kb", ha='center', va='top', fontsize=8, color='red')
    plt.text(0, time_wifi, f"{round(time_wifi, 2)} ms", ha='right', va='center', fontsize=8, color='red')

# Labels and title
plt.xlabel("File size (kb)")
plt.ylabel("Transfer time (ms)")
plt.title("File Transfer Time vs File Size (Mobile Hotspot vs Dorm WiFi)")
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend()

# Display the plot
plt.show()
