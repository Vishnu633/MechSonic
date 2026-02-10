# Mechsonic // Mechanical Keyboard Simulator

A high-fidelity mechanical keyboard sound simulator with a modern, monochrome aesthetic. Experience the tactile feedback of premium switches without the hardware.

![Mechsonic UI](https://via.placeholder.com/800x600?text=Mechsonic+UI+Preview) 
*(Replace with actual screenshot)*

## Features

-   **High-End Audio Engine**: Low-latency playback using `pygame-ce`.
-   **Monochrome Theme**: Distraction-free, luxurious dark mode interface.
-   **Visualizer**: Real-time input signal visualizer.
-   **Sound Profiles**: Includes 13+ switch types (Cherry MX, Topre, Alps, etc.).
-   **Customizable**: Import your own sound packs easily.
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

## Adding Custom Sounds
1.  Click the **"+ IMPORT SOUND PACK"** button in the app.
2.  Select a folder containing your sound files.
3.  The folder should contain `press/` and `release/` subdirectories, or files named like `press_*.wav`.

## License
MIT License. See `LICENSE` for details.
