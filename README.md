# Customer Churn Predictor

Customer Churn Predictor is a C++ project that implements a simple logistic regression model to predict whether a customer is likely to cancel a service or subscription, based on a set of input features.

## Key Implementations

- Manual implementation of core vector and matrix operations
- Logistic Regression algorithm with sigmoid activation
- Cross-Entropy Loss for classification accuracy
- Stochastic Gradient Descent optimization implemented from scratch
- Basic CSV parsing for input and output handling
- Command-line interface for training, predicting, and evaluating the model
- Logging with timestamped log files

## How to Build and Run

### Prerequisites

- A C++20-compliant compiler (e.g., g++)
- make utility

### Build the Project

```bash
make
```

This compiles the main application and produces an executable named `logistic_churn`.

### Run the Program

```bash
./logistic_churn [OPTION]

```

### Command-Line Options

- `-help`

  Displays help information.

- `-train`

  Train a new model. The program will prompt for dataset location, output path, learning rate, epochs, and columns to drop.

- `-train --evaluate`

  Train a model and display evaluation metrics (accuracy, precision, recall, F1 score).

- `-predict`

  Predict churn using an existing trained model. The program will prompt for the model weights file, input dataset, and output destination.


**Examples:**

```bash
./logistic_churn --train
./logistic_churn --train --evaluate
./logistic_churn --predict

```

Log files are automatically saved under the `logs/` directory with timestamped names.

### Clean Build Files

```bash
make clean
```

This removes the executables (`logistic_churn`, `run_tests`) from the project directory.

## Project Structure

```
.
├── main.cpp          # Entry point
├── include/          # Header files
│   └── ...
├── src/              # Core logic (vector ops, model, etc.)
│   └── ...
├── data/             # Input and output data
├── logs/             # Execution logs
├── Makefile          # Build and test automation
└── README.md         # Project documentation
```

## Training and Prediction Workflow

1. **Training a model:** The program reads a CSV dataset, preprocesses features (normalization, one-hot encoding), trains the logistic regression model, and saves the weights.
2. **Prediction:** Load a trained model and predict churn probabilities for new input data. Results are saved as a CSV file.
3. **Evaluation:** When using `-train --evaluate`, the program calculates and logs metrics including accuracy, precision, recall, and F1 score.