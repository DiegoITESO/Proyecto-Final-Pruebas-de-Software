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
- Catch2
- Clang-format

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

# Como contribuir

Gracias por tu interes en contribuir a este proyecto! Aqui explicamos como trabajar con el repositorio para que tus contribuciones se integren de forma ordenada y consistente.

## Resumen rapido
- Forkea el proyecto (si no eres colaborador directo).
- Crea una rama temporal para tu trabajo (no trabajes directamente en main).
- Asegurate de que los linters y tests pasen localmente.
- Usa mensajes de commit siguiendo Conventional Commits.
- Abre un Pull Request (PR) desde tu rama hacia la rama de destino (main o develop) y espera la revision y aprobacion.

---

## Flujo recomendado (paso a paso)

1. Fork (si procede) y clona
   - Forkea el repo en GitHub (si eres contribuidor externo).
   - Clona tu fork:
     ```
     git clone [https://github.com/TU_USUARIO/Proyecto-Final-Pruebas-de-Software.git](https://github.com/TU_USUARIO/Proyecto-Final-Pruebas-de-Software.git)
     cd Proyecto-Final-Pruebas-de-Software
     ```

2. Sincroniza con el upstream (opcional pero recomendado)
   - Añade el remoto upstream y sincroniza:
     ```
     git remote add upstream [https://github.com/DiegoITESO/Proyecto-Final-Pruebas-de-Software.git](https://github.com/DiegoITESO/Proyecto-Final-Pruebas-de-Software.git)
     git fetch upstream
     git checkout main
     git merge upstream/main
     ```

3. Crea una rama para tu trabajo
   - Usa un nombre de rama descriptivo y corto:
     - feature/123-descripcion-corta
     - fix/45-corregir-error-login
     - chore/actualizar-dependencias
     ```
     git checkout -b feature/<issue>-descripcion-corta
     ```

4. Realiza cambios y ejecuta checks locales
   - Asegurate de ejecutar los linters y tests que esten configurados en el repositorio antes de commitear.
   - Pre-commit: hooks que se ejecutan al commitear. Para lanzarlo manualmente:
     ```
     pre-commit run --all-files
     ```
     (Si no tienes pre-commit instalado: `pip install pre-commit` o revisa la documentacion del proyecto.)

   - Ejecuta los tests del proyecto segun la configuracion (ejemplos):
     ```
     npm test
     # o
     pytest
     ```

5. Commits: sigue Conventional Commits
   - Formato general: `<type>(scope?): subject`
   - Tipos comunes:
     - feat: nueva funcionalidad
     - fix: arreglo de bug
     - docs: documentacion
     - style: formato / estilo (no afecta codigo)
     - refactor: refactorizacion sin cambios de funcionalidad
     - test: añadir/ajustar tests
     - chore: tareas de mantenimiento
   - Ejemplos:
     ```
     git add .
     git commit -m "feat: agregar pruebas de integracion para login"
     git commit -m "fix(auth): validar token en /api/user"
     ```
   - Si el repositorio tiene un linter para commits (commitlint), los commits que no cumplan la convencion seran rechazados.

6. Si necesitas editar mensajes de commit
   - Para corregir el ultimo commit:
     ```
     git commit --amend -m "fix: mensaje corregido"
     ```
   - Para reescribir varios commits: `git rebase -i HEAD~N` (con cuidado).

7. Push y Pull Request
   - Push a tu fork/remoto:
     ```
     git push origin feature/<issue>-descripcion-corta
     ```
   - Abre un Pull Request desde tu rama hacia la rama de destino del repo original (por ejemplo main o develop).
   - En la descripcion del PR incluye:
     - Resumen del cambio.
     - Issue relacionado (si aplica): `Closes #NN`
     - Como probar los cambios localmente.
     - Evidencia (capturas, logs) si procede.

---

## Checklist recomendado para el PR
Antes de solicitar revision, verifica:
- [ ] Los linters pasan localmente (pre-commit).
- [ ] Todos los tests relevantes pasan.
- [ ] Los mensajes de commit siguen Conventional Commits.
- [ ] La rama esta actualizada con la rama de destino (merge/rebase si es necesario).
- [ ] El PR tiene una descripcion clara y, si aplica, vincula el issue correspondiente.
- [ ] No incluyes secretos ni credenciales.

---

## Revision y merge
- Los mantenedores revisaran el PR y pueden solicitar cambios.
- El PR se fusionara cuando:
  - Tenga la aprobacion(es) requerida(s).
  - Pase las comprobaciones automaticas (CI).
  - Cumpla con las normas de estilo y commits.

---

## Convenciones de nombres de ramas (sugeridas)
- feature/<numero>-descripcion-corta
- fix/<numero>-descripcion-corta
- chore/<descripcion-corta>
- docs/<descripcion-corta>

Usa solo letras minusculas y guiones para separar palabras.

---

## Informacion sobre los linters que usamos
- pre-commit: hooks que verifican formato, linting y otras comprobaciones antes de permitir el commit. Ejecuta los hooks localmente con:

```bash 
pre-commit run --all-files
```


## Training and Prediction Workflow

1. **Training a model:** The program reads a CSV dataset, preprocesses features (normalization, one-hot encoding), trains the logistic regression model, and saves the weights.
2. **Prediction:** Load a trained model and predict churn probabilities for new input data. Results are saved as a CSV file.
3. **Evaluation:** When using `-train --evaluate`, the program calculates and logs metrics including accuracy, precision, recall, and F1 score.

## Requirements

### FR-01: Command Line Interface (CLI)
The system shall provide a command-line interface that allows the user to execute the following options:
- `--help`: Display help information with available commands.
- `--train`: Train a new model using a dataset.
- `--train --evaluate`: Train a model and display evaluation metrics.
- `--predict`: Load a trained model and generate predictions.

---

### FR-02: Training Input Parameters
In training mode (`--train`), the system shall request the following inputs from the user:
- Path to the input CSV file.
- Output path to save the trained model (JSON file).
- Whether the CSV file contains a header.
- Index of the column containing the target label (churn).
- Indices of columns to discard (optional).
- Learning rate.
- Number of training epochs.

---

### FR-03: Data Validation and Reading
The system shall:
- Read CSV files provided by the user.
- Validate that all rows have the same number of columns.
- Raise an error if inconsistencies are found.

---

### FR-04: Data Preprocessing
The system shall preprocess the input data by:
- Converting categorical values "yes"/"no" to numerical values (1.0/0.0).
- Interpreting numerical values as double.
- Applying one-hot encoding to non-numeric categorical features.
- Normalizing all features (mean = 0, standard deviation = 1).
- Removing user-specified columns.

---

### FR-05: Dataset Splitting
The system shall split the dataset into:
- 80% for training.
- 20% for testing.

---

### FR-06: Model Training
The system shall:
- Train a logistic regression model.
- Use stochastic gradient descent (SGD) as the optimization algorithm.
- Adjust model parameters (weights and bias) based on training data.

---

### FR-07: Model Storage
The system shall:
- Save the trained model in a JSON file.
- Include weights (array of doubles) and bias (double).

---

### FR-08: Model Evaluation
In `--train --evaluate` mode, the system shall:
- Compute the following metrics:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
- Display results in the console.
- Save results in the log file.

---

### FR-09: Prediction Input Parameters
In prediction mode (`--predict`), the system shall request:
- Path to the trained model file (JSON).
- Path to the input dataset (CSV).
- Output path for predictions (CSV).
- Whether the dataset contains a header.
- Columns to discard (optional).

---

### FR-10: Prediction Generation
The system shall:
- Load the trained model.
- Preprocess the input dataset in the same way as during training.
- Generate a churn probability for each record.
- Save predictions in a CSV file (one probability per row).

---

### FR-11: Model Persistence and Loading
The system shall:
- Load previously saved models from JSON files.
- Use loaded parameters to perform predictions.

---

### FR-12: Logging
The system shall:
- Generate log files in a `logs/` directory.
- Include a timestamp in each log file.
- Record key events such as:
  - Process start
  - CSV loading
  - Model training
  - Evaluation
  - Prediction generation
  - Errors

### NFR-01: Code Formatting (ClangFormat)
The system shall enforce a consistent coding style using ClangFormat.

- All source code must conform to a predefined `.clang-format` configuration file.
- Any code that does not comply with the formatting rules shall be rejected in the development workflow.
- The formatting rules must be consistent across all contributors.

---

### NFR-02: Linting Integration
The system shall include ClangFormat as part of the development workflow.

- Developers must run ClangFormat before committing code.
- The project repository shall include the `.clang-format` file.

---

### NFR-03: Unit Testing Framework (Catch2)
The system shall include unit tests implemented using the Catch2 framework.

- All core functionalities must be covered by unit tests.
- Test cases must be organized and maintainable.
- The project shall include Catch2 as a dependency.

---

### NFR-04: Test Coverage
The system shall ensure a minimum level of test coverage.

- At least 70% of the codebase must be covered by unit tests.

---

### NFR-05: Test Execution
The system shall allow execution of all unit tests through a single command.

- Tests must be executable via command line
- Test results must clearly indicate passed and failed cases.

---

### NFR-06: Continuous Testing (Optional)
The system should support automated test execution.

- Unit tests should be executed automatically in a CI/CD pipeline.
- Builds should fail if any test fails.

---

### NFR-07: Error Handling Validation
Unit tests shall validate error handling behavior.

- Tests must verify that the system correctly handles:
  - Invalid CSV formats
  - Missing files
  - Incorrect parameters
- Expected exceptions or error messages must be asserted.

---

### NFR-08: Reproducibility
The system shall ensure reproducibility of tests.

- Tests must produce consistent results across different environments.
- Any randomness must use a mock during testing.

---

### NFR-09: Maintainability
The system shall ensure maintainable test and code structure.

- Test files must be separated from production code.
- Naming conventions must be clear and consistent.
- Code must be modular to facilitate testing.


## Mockups

### Help

```bash
$ ./logistic_churn --help
```

```
Customer Churn Predictor - Command Line Interface
--------------------------------------------------
Usage:
  ./logistic_churn [OPTION]

Options:
  --help             Show this help message and exit
  --train            Train a new model
  --train --evaluate Train a model and evaluate its accuracy
  --predict          Predict churn using an existing trained model

Examples:
  ./logistic_churn --train
  ./logistic_churn --train --evaluate
  ./logistic_churn --predict

Log files are saved under the 'logs/' directory with timestamped names.
```

### Train

```bash
./logistic_churn --train
```

**Results:**

```
Enter the dataset file location:
data/customer_data.csv

Enter the destination output file location:
models/weights.json

Does it have a header? (y/n): y

Enter the index of the column that contains the results (weather the client churned or not):
(0 indexed)
5

Enter the indices of the columns you want to drop 
(press enter if you dont want any columns to be dropped):
(These can be IDs or data with weak or nonexistent correlation to the churn. Enter the numbers space-separated)
0 1

Enter the learning rate
0.01

Enter the number of epochs
1000

Progress: 0%
Progress: 1%
Progress: 2%
...
Progress: 99%
Progress: 100%
```

### Evaluate

```bash
$ ./logistic_churn --train --evaluate
```

**Results:**

```
Enter the dataset file location:
data/customer_data.csv

Enter the destination output file location:
models/weights.json

Does it have a header? (y/n): y

Enter the index of the column that contains the results (weather the client churned or not):
(0 indexed)
5

Enter the indices of the columns you want to drop (press enter if you don't want any columns to be dropped):
(These can be IDs or data with weak or nonexistent correlation to the churn. Enter the numbers space-separated)
0 1

Enter the learning rate
0.01

Enter the number of epochs
1000

Progress: 0%
Progress: 1%
...
Progress: 100%

Accuracy: 0.872340
Precision: 0.857143
Recall: 0.818182
F1 score: 0.837209
```

### Prediccion

```bash
$ ./logistic_churn --predict
```

**Results**

```
Enter the weights file location:
models/weights.json

Enter the dataset file location:
data/new_customers.csv

Enter the destination output file location:
output/predictions.csv

Does it have a header? (y/n): y

Enter the indices of the columns you want to drop (press enter if you don't want any columns to be dropped):
(These can be IDs or data with weak or nonexistent correlation to the churn. Enter the numbers space-separated)
0
```

**predictions.csv**

```
0.923456
0.112345
0.456789
0.987654
...
```