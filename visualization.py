import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def plot_signal_waveform(signal, title="Forma de onda do sinal", figsize=(10, 4)):
    """
    Create a beautifully styled plot of a signal waveform.

    Args:
        signal (numpy.ndarray): The signal to plot
        title (str): The title of the plot
        figsize (tuple): Figure size (width, height)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    # Create figure with light gray background and white grid
    fig, ax = plt.subplots(figsize=figsize, facecolor="#f9f9f9")
    ax.set_facecolor("#f9f9f9")

    # Plot the signal with a thicker blue line
    ax.plot(signal, linewidth=1.5, color="#1f77b4", alpha=0.8)

    # Detect signal characteristics to determine y-axis limits
    if len(signal) > 0:
        max_val = max(np.max(signal), 1)
        min_val = min(np.min(signal), -1)
        y_margin = (max_val - min_val) * 0.1
        ax.set_ylim(min_val - y_margin, max_val + y_margin)

    # Add zero line for reference
    ax.axhline(y=0, color="#cccccc", linestyle="-", alpha=0.3)

    # Set labels and title with a nice font
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Amostras", fontsize=12)
    ax.set_ylabel("Amplitude", fontsize=12)

    # Add grid for better readability
    ax.grid(True, linestyle="--", alpha=0.7)

    # Add ticks without cluttering
    if len(signal) > 20:
        # Show fewer x-ticks for clarity
        ax.set_xticks(np.linspace(0, len(signal) - 1, 10, dtype=int))

    # Tight layout to make everything fit nicely
    fig.tight_layout()

    return fig


def plot_binary_signal(
    binary_string, title="Representação do Sinal Binário", figsize=(10, 3)
):
    """
    Create a plot representing a binary signal as discrete levels.

    Args:
        binary_string (str): The binary string to visualize
        title (str): The title of the plot
        figsize (tuple): Figure size (width, height)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    bits = [int(bit) for bit in binary_string.replace(" ", "")]

    # Create figure
    fig, ax = plt.subplots(figsize=figsize, facecolor="#f9f9f9")
    ax.set_facecolor("#f9f9f9")

    # Create a step plot for binary data
    x = np.arange(len(bits) + 1)
    y = np.array(bits + [bits[-1]])  # Repeat last bit for step plot
    ax.step(x, y, "g-", linewidth=1.5, where="post", alpha=0.8)

    # Fill areas
    ax.fill_between(x, y, step="post", alpha=0.3, color="green")

    # Set proper y-limits with margin
    ax.set_ylim(-0.2, 1.2)

    # Add bit values as text annotations
    for i, bit in enumerate(bits):
        ax.text(i + 0.5, bit + 0.1, str(bit), ha="center", fontsize=9)

    # Set tick positions at the bit transitions
    ax.set_xticks(range(len(bits) + 1))

    # Set labels and title
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Tempo (bits)", fontsize=12)
    ax.set_ylabel("Nível lógico", fontsize=12)

    # Add grid
    ax.grid(True, linestyle="--", alpha=0.7)

    # Tight layout
    fig.tight_layout()

    return fig
