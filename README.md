# Rubik's Cube Solver & Speedcubing Learning Tool

An interactive 3D Rubik's Cube solver and educational suite developed as an **A-Level Computer Science Non-Exam Assessment (NEA)**. Designed specifically for intermediate speedcubers seeking to transition from beginner methods to structured **CFOP** (Cross, F2L, OLL, PLL) execution, the application combines custom search algorithms, 3D visualization, algebraic move pruning, and solve session persistence.

---

## Key Features

* **Dual Solving Engines:**
  * **CFOP Solver (Human-Centric):** Uses an $A^*$ search algorithm with a Manhattan distance-inspired heuristic for the White Cross, followed by algorithmic steps for First Two Layers (F2L), Orienting the Last Layer (OLL), and Permutating the Last Layer (PLL).
  * **Kociemba Solver (Optimal):** Integrates Two-Phase Algorithm solving for near-optimal move efficiency ($\le 25$ moves).
* **Interactive 3D Visualizer:** Built using the Ursina Engine (OpenGL) featuring 360-degree orbital camera rotation, animated move transitions, keyboard controls, and step-by-step solution playback for look-ahead training.
* **Algebraic Move Optimization:** Applies cyclic group theory ($fr = r \pmod 4$) and inverse move pruning to simplify generated solution strings and eliminate redundant face rotations.
* **Database & PDF Analytics:** Powered by SQLite3 to store solve histories, algorithm lookup tables, and user preferences. Includes a custom **Merge Sort** sorting engine and PDF report generation for offline revision.

---

## Tech Stack & Dependencies

| Component | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core application logic and backend solver |
| **3D Rendering** | Ursina Engine / OpenGL 3.0+ | Real-time 3D cube rendering and user interface |
| **Matrix Operations** | NumPy | Multidimensional face sticker array manipulation |
| **Optimal Solving** | Kociemba (C++ Wrapper) | Sub-25 move two-phase solving algorithm |
| **Database** | SQLite3 | Relational storage for solves and algorithm definitions |

---

## System Architecture

```text
/Program
│
├── main.py                   # Application entry point
├── config.py                 # System constants and global parameters
│
├── core_main/                # Backend logic & algorithms
│   ├── cube_logic.py         # Matrix representation & 3D rotation logic
│   └── solver.py             # A* White Cross, CFOP pipeline, and Kociemba solver
│
├── database/                 # Persistence layer
│   ├── database_setup.py     # SQLite schema definitions (3NF normalized)
│   ├── algorithm_library.py  # SQL queries for loading OLL/PLL cases
│   ├── data_manager.py       # Solve history storage, sorting, and export
│   └── algorithm_data.py     # Hardcoded algorithm mappings and lookup strings
│
└── ui/                       # Graphical User Interface
    ├── solver_page.py        # Main UI layout and button event handlers
    └── threed_cube.py        # Ursina entity creation and move animations

```

## Installation & Setup

### Requirements

* **Operating System:** Windows 10+ (recommended for Ursina/OpenGL support)
* **Python:** Version 3.10 or higher
* **Build Tools:** Microsoft C++ Build Tools (required for compiling the `kociemba` C++ library)

### Step-by-Step Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rubiks-cube-solver.git
cd rubiks-cube-solver
```

#### 2. Create a Virtual Environment

Creating a virtual environment is optional but recommended.

```bash
python -m venv venv
```

On Windows, activate the virtual environment using:

```bash
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install ursina numpy kociemba reportlab
```

#### 4. Run the Application

```bash
python main.py
```

## Usage Guide

* **Scramble:** Click the **Scramble** button or use the available keyboard shortcuts to generate a randomized 25-move state.
* **Select Method:** Choose between **CFOP** (educational step-by-step) or **Kociemba** (move-optimal).
* **Solve & Playback:** Click **Solve** to execute the back-end algorithm. Use the step forward/backward buttons to inspect individual rotation steps for look-ahead practice.
* **Export History:** Navigate to the **History** tab to sort past solves by move count and generate an offline PDF report.

