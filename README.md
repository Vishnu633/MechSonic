# Mechsonic // Mechanical Keyboard Simulator

A high-fidelity mechanical keyboard sound simulator with a modern, monochrome aesthetic. Experience the tactile feedback of premium switches without the hardware.

<img width="489" height="631" alt="image" src="https://github.com/user-attachments/assets/d42092cd-ecd2-4322-8ca5-373815ba2c8e" />



## Features

-   **High-End Audio Engine**: Low-latency playback using `pygame-ce`.
-   **Monochrome Theme**: Distraction-free, luxurious dark mode interface.
-   **Visualizer**: Real-time input signal visualizer.
-   **Sound Profiles**: Includes 13+ switch types (Cherry MX, Topre, Alps, etc.).
-   **Cross-Platform**: Runs on macOS, Windows, and Linux.

## Installation

### Prerequisites
-   Python 3.10 or higher.

### Steps

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Vishnu633/MechSonic.git
    cd mechsonic
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### macOS / Linux
Run the included shell script:
```bash
./run.sh
```
*Note: On macOS, you may need to grant "Accessibility" permissions to your terminal or the Python application to monitor global keystrokes.*

### Windows
Run directly with Python:
```bash
python main.py
```
