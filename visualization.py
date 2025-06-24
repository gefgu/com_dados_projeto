import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def plot_signal_waveform(signal, title="Forma de onda do sinal", figsize=(12, 5)):
    """
    Create a beautifully styled plot of a signal waveform with logical pulse appearance.

    Args:
        signal (numpy.ndarray): The signal to plot
        title (str): The title of the plot
        figsize (tuple): Figure size (width, height)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    # Create figure with modern styling
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    ax.set_facecolor("#fafafa")

    # Create time axis for better pulse representation
    time_per_bit = 1.0  # Each bit takes 1 time unit
    total_time = len(signal) * time_per_bit
    time = np.linspace(0, total_time, len(signal))

    # Create step-like signal for pulse appearance
    extended_time = []
    extended_signal = []

    for i, amplitude in enumerate(signal):
        t_start = i * time_per_bit
        t_end = (i + 1) * time_per_bit

        # Add vertical transitions for sharp edges
        if i > 0 and signal[i - 1] != amplitude:
            extended_time.append(t_start)
            extended_signal.append(signal[i - 1])

        # Add the pulse duration
        extended_time.extend([t_start, t_end])
        extended_signal.extend([amplitude, amplitude])

    # Plot the signal with sharp, logical pulse appearance
    ax.plot(
        extended_time,
        extended_signal,
        linewidth=2.5,
        color="#2E86AB",
        alpha=0.9,
        solid_capstyle="butt",
    )

    # Fill positive and negative areas with different colors
    ax.fill_between(
        extended_time,
        extended_signal,
        0,
        where=np.array(extended_signal) > 0,
        color="#A23B72",
        alpha=0.2,
        interpolate=True,
        label="Nível Alto",
    )
    ax.fill_between(
        extended_time,
        extended_signal,
        0,
        where=np.array(extended_signal) < 0,
        color="#F18F01",
        alpha=0.2,
        interpolate=True,
        label="Nível Baixo",
    )

    # Add zero reference line
    ax.axhline(y=0, color="#666666", linestyle="-", alpha=0.6, linewidth=1)

    # Detect signal characteristics for better y-axis limits
    if len(signal) > 0:
        max_val = max(np.max(signal), 1.2)
        min_val = min(np.min(signal), -1.2)
        y_margin = (max_val - min_val) * 0.1
        ax.set_ylim(min_val - y_margin, max_val + y_margin)

    # Set time axis limits
    ax.set_xlim(0, total_time)

    # Enhanced styling
    ax.set_title(title, fontsize=16, fontweight="bold", color="#2c3e50", pad=20)
    ax.set_xlabel("Tempo (unidades de bit)", fontsize=13, color="#34495e")
    ax.set_ylabel("Amplitude do Sinal", fontsize=13, color="#34495e")

    # Modern grid styling
    ax.grid(True, linestyle="--", alpha=0.4, color="#bdc3c7")
    ax.set_axisbelow(True)

    # Add bit markers on x-axis
    bit_positions = np.arange(0, total_time + 1, time_per_bit)
    ax.set_xticks(bit_positions)
    ax.set_xticklabels([f"{int(i)}" for i in bit_positions], fontsize=3)

    # Add amplitude level indicators
    unique_levels = np.unique(signal)
    for level in unique_levels:
        if level != 0:
            ax.axhline(
                y=level, color="#95a5a6", linestyle=":", alpha=0.5, linewidth=0.8
            )
            ax.text(
                total_time * 0.98,
                level,
                f"{level:+.1f}V",
                ha="right",
                va="bottom",
                fontsize=5,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
            )

    # Add legend if we have both positive and negative values
    if np.any(np.array(signal) > 0) and np.any(np.array(signal) < 0):
        ax.legend(loc="upper right", frameon=True, fancybox=True, shadow=True)

    # Remove top and right spines for cleaner look
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#7f8c8d")
    ax.spines["bottom"].set_color("#7f8c8d")

    # Tight layout
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
        ax.text(i + 0.5, bit + 0.1, str(bit), ha="center", fontsize=5)

    # Set tick positions at the bit transitions
    ax.set_xticks(range(len(bits) + 1))
    ax.set_xticklabels(
        [f"{int(i)}" for i in range(len(bits) + 1)], fontsize=3, rotation=90
    )

    # Set labels and title
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Tempo (bits)", fontsize=12)
    ax.set_ylabel("Nível lógico", fontsize=12)

    # Add grid
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Tight layout
    fig.tight_layout()

    return fig
