import numpy as np
import matplotlib.pyplot as plt

# Function to update the visualization with new signal strengths
def update_visualization(A, B, C, AT_strength, BT_strength, CT_strength):
    plt.clf()  # Clear the current figure
    ax = plt.gca()  # Get the current axes instance
    ax.set_aspect('equal')  # Set equal scaling by changing axis limits

    # Plot the circles representing signal strength for each node
    circle_A = plt.Circle(A, AT_strength, color='blue', fill=False)
    circle_B = plt.Circle(B, BT_strength, color='green', fill=False)
    circle_C = plt.Circle(C, CT_strength, color='red', fill=False)
    ax.add_artist(circle_A)
    ax.add_artist(circle_B)
    ax.add_artist(circle_C)

    # Plot the triangle connecting nodes A, B, and C
    plt.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'b-')

    # Dynamically adjust the limits of the plot to ensure all elements are visible
    x_values = [A[0], B[0], C[0]]
    y_values = [A[1], B[1], C[1]]
    plt.xlim(min(x_values) - 5, max(x_values) + 5)
    plt.ylim(min(y_values) - 5, max(y_values) + 5)

    plt.pause(0.01)  # Pause to update the plot


# Main function to initialize and update the visualization
def main():
    plt.ion()  # Enable interactive plotting
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    plt.show()

    # Initialize the positions of nodes A, B, and C
    A = np.array([0, 0])
    B = np.array([0, 0])
    C = np.array([0, 0])

    # Define signal strength boundaries
    max_signal_strength = -30  # Maximum signal strength in dBm
    min_signal_strength = -90  # Minimum signal strength in dBm

    # Main loop to read and update signal strength data
    while True:
        with open("signal_strength_data.txt", "r") as file:
            lines = file.readlines()

        # Parse the signal strength data from the file
        AB_strength = int(lines[1].strip())
        BC_strength = int(lines[3].strip())
        CA_strength = int(lines[5].strip())
        AT_strength = int(lines[7].strip())
        BT_strength = int(lines[9].strip())
        CT_strength = int(lines[11].strip())

        # Convert signal strength from dBm to a percentage for visualization
        AB_percentage = ((AB_strength - max_signal_strength) / (min_signal_strength - max_signal_strength)) * 100
        BC_percentage = ((BC_strength - max_signal_strength) / (min_signal_strength - max_signal_strength)) * 100
        CA_percentage = ((CA_strength - max_signal_strength) / (min_signal_strength - max_signal_strength)) * 100
        AT_percentage = ((AT_strength - max_signal_strength) / (min_signal_strength - max_signal_strength)) * 100
        BT_percentage = ((BT_strength - max_signal_strength) / (min_signal_strength - max_signal_strength)) * 100
        CT_percentage = ((CT_strength - max_signal_strength) / (min_signal_strength - max_signal_strength)) * 100

        # Use the Law of Cosines to calculate the angles of the triangle formed by nodes A, B, and C
        angle_A = np.arccos((BC_percentage ** 2 + CA_percentage ** 2 - AB_percentage ** 2) / (2 * BC_percentage * CA_percentage))
        angle_B = np.arccos((CA_percentage ** 2 + AB_percentage ** 2 - BC_percentage ** 2) / (2 * CA_percentage * AB_percentage))
        angle_C = np.pi - angle_A - angle_B  # The sum of angles in a triangle is 180 degrees

        # Update the positions of nodes A, B, and C based on the calculated angles and distances
        A = np.array([0, 0])  # Node A remains at the origin
        B = np.array([AB_percentage, 0])  # Node B is along the x-axis
        C = np.array([CA_percentage * np.cos(angle_B), CA_percentage * np.sin(angle_B)])  # Position of node C based on angle B

        # Update the visualization with the new positions and signal strengths
        update_visualization(A, B, C, AT_percentage, BT_percentage, CT_percentage)

# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()