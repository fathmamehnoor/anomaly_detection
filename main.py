import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def data_stream_simulation(n_points, anomaly_rate=0.05):
    """
    Emulates a data stream with regular patterns, seasonal elements, and random noise.
    
    Args:
        n_points (int): Number of data points to generate.
        anomaly_rate (float): Probability of generating an anomaly for each data point.
    
    Yields:
        float: Simulated data point value, potentially with an anomaly.
    """
    for i in range(n_points):
        try:
            # regular sine wave pattern
            short_term_pattern = np.sin(i / 10)

            # seasonal pattern
            seasonal_pattern = np.sin(i / 200)

            # add random noise
            noise = np.random.normal(0, 0.2)
            value = short_term_pattern + seasonal_pattern + noise

            # simulate anomaly based on anomaly rate
            if np.random.rand() < anomaly_rate:
                value += np.random.uniform(-5, 5)
            
            yield value
            time.sleep(0.1)  # Adjusted for real-time performance
        except Exception as e:
            print(f"Error in data stream simulation: {e}")


def ema(window, alpha=0.1):
    """
    Calculate the Exponential Moving Average (EMA) over a sliding window.
    
    Args:
        window (list): Recent data values in the sliding window.
        alpha (float): Smoothing factor for EMA (0 < alpha < 1).
    
    Returns:
        float: Calculated EMA value.
    """
    ema_val = 0
    for value in window:
        ema_val = alpha * value + (1 - alpha) * ema_val
    return ema_val


def anomaly_detection(value, ema_val, std, threshold=3):
    """
    Detect anomalies based on the z-score method.
    
    Args:
        value (float): The current data point value.
        ema_val (float): The calculated EMA value.
        std (float): Standard deviation of the data window.
        threshold (float): Threshold for z-score anomaly detection.
    
    Returns:
        bool: True if the value is an anomaly, otherwise False.
    """
    z_score = abs((value - ema_val) / std) if std != 0 else 0 
    return z_score > threshold


# Initialize the figure for plotting
fig, ax = plt.subplots()
x_data, y_data = [], []
anomaly_x, anomaly_y = [], []  

# Global variables for window size and sliding window
window_size = 50  # Size of the sliding window
data_window = []  # To store recent values in the sliding window
threshold = 2  # Threshold for anomaly detection (z-score)

def update(frame):
    """
    Update the plot with the new data point and detect anomalies.
    
    Args:
        frame (int): Current frame number.
    
    Returns:
        Axes: Updated matplotlib Axes object for plotting.
    """
    global data_window 

    try:
        value = next(data_stream)  
    except StopIteration:
        print("Data stream ended.")
        return ax  

    x_data.append(frame) 
    y_data.append(value)  

    # Update sliding window
    data_window.append(value)
    if len(data_window) > window_size:
        data_window.pop(0)  # Remove the oldest value when the window is full

    # Calculate EMA and standard deviation
    ema_val = ema(data_window)
    std = np.std(data_window)

    # Detect anomaly based on updated EMA and standard deviation
    if anomaly_detection(value, ema_val, std, threshold):
        anomaly_x.append(frame)  
        anomaly_y.append(value) 

    ax.clear()
    ax.plot(x_data, y_data, label='Data Stream', color='blue')  # Plot the data stream
    ax.scatter(anomaly_x, anomaly_y, color='red', label='Anomaly', zorder=3)  # Plot all anomalies
    ax.set_xlim(0, len(x_data) + 10)
    ax.set_ylim(min(y_data) - 1, max(y_data) + 1)  

    ax.legend(loc='upper left') 
    return ax


# Simulate data stream
data_stream = data_stream_simulation(1000)

# Create the animation for real-time plotting
ani = animation.FuncAnimation(fig, update, frames=range(1000), repeat=False)

plt.show()
