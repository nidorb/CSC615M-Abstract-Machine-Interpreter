# 🧠 Abstract Machine Interpreter

## 📌 Project Overview

This project is an interpreter that simulates various abstract computation models by using different memory structures and execution logic. It supports the following machine types:

- **Deterministic Finite Automata (DFA)**
- **Non-deterministic Finite Automata (NFA)**
- **Generalized Sequential Transducers**
- **Pushdown Accepters**
- **Stack and Queue Machines**
- **1D and 2D Turing Machines**

---

## 📥 Input Structure

### `.DATA` Section (Auxiliary Memory Declaration)

Use this section to define the memory structures required by your machine:

- `STACK <name>` – Declares a **LIFO** memory stack.
- `QUEUE <name>` – Declares a **FIFO** memory queue.
- `TAPE <name>` – Declares a **1D Turing machine tape**. The first declared tape is used as the **input tape**.
- `2D_TAPE <name>` – Declares a **2D Turing machine tape**. The first declared 2D tape has **input in the top row**.

---

### `.LOGIC` Section (Logic Definition)

Each state's behavior is defined using the following format:

```text
<SOURCE_STATE>] COMMAND (<SYMBOL_1>,<DESTINATION_STATE_1>), (<SYMBOL_2>,<DESTINATION_STATE_2>), ...
```

#### Available Commands

- `SCAN` – Reads an input symbol.
- `PRINT` – Outputs a symbol.
- `SCAN RIGHT` / `SCAN LEFT` – Reads a symbol and moves the tape head accordingly.
- `READ(<memory>)` – Reads a symbol from the specified `STACK` or `QUEUE`.
- `WRITE(<memory>)` – Writes a symbol to the specified `STACK` or `QUEUE`.

---

### 🧾 Tape Commands (for Turing Machines)

For Turing machine tape operations, use this extended format:

```text
<SOURCE_STATE>] COMMAND (<SYMBOL>/<REPLACEMENT_SYMBOL>,<DESTINATION_STATE>), ...
```

#### Tape Movement Commands

- `RIGHT(<tape>)` – Moves right, replaces symbol, changes state.
- `LEFT(<tape>)` – Moves left, replaces symbol, changes state.
- `UP(<2D_tape>)` – Moves up in a 2D tape, replaces symbol, changes state.
- `DOWN(<2D_tape>)` – Moves down in a 2D tape, replaces symbol, changes state.

---

## 🔚 Special States

- `accept` – Halts and accepts the input.
- `reject` – Halts and rejects the input.

---

## ▶️ Running the Program

Make sure you have **Python** installed. Then run the program with:

```bash
python app.py
```

---
