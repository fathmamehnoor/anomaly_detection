import numpy as np
import time

# function to emulate a data stream, incorporating regular patterns, seasonal elements, and random noise.
def data_stream_simulation(n_points, anomaly_rate = 0.05):

    for i in range(n_points):

        # regular sine wave pattern
        short_term_pattern = np.sin(i / 10)

        # seasonal pattern
        seasonal_pattern = np.sin(i / 200)

        # Add random noise
        noise = np.random.normal(0, 0.2)

        value = short_term_pattern + seasonal_pattern + noise

        # simulate anomaly based on anomaly rate
        if np.random.rand() < anomaly_rate:
            value += np.random.uniform(-5, 5)

        # simulate real-time stream
        yield value
        time.sleep(0.1)



# calculate Exponential Moving Average(EMA)
def ema(previous, new, alpha=0.1):

    return alpha * new + (1 - alpha) + previous




 