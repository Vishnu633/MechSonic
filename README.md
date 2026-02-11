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

**Clone the repository**:

```bash
git clone https://github.com/Vishnu633/MechSonic.git
cd MechSonic
```

## Usage

### macOS / Linux (Recommended)

Run the included shell script:

```bash
./run.sh
```

The script will:

-   Activate the `.venv` virtual environment (if available)
-   Run `main.py`

If `.venv` does not exist, create it first:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run:

```bash
./run.sh
```

*Note: On macOS, you may need to grant "Accessibility" permissions to your terminal or the Python application to monitor global keystrokes.*

### Manual Setup (Without run.sh)

**Create a virtual environment (optional but recommended):**

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Run the application:**

**macOS / Linux**

```bash
python3 main.py
```

**Windows**

```bash
python main.py
```
