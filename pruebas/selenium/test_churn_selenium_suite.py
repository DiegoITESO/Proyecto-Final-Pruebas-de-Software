# Suite Selenium: valida fixtures HTML alineadas al README y ArgParser del proyecto C++.
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _wait(driver):
    return WebDriverWait(driver, 10)


# --- Help (espejo de showHelp) ---


def test_help_root_visible(driver, open_fixture):
    """Objetivo: comprobar que la pagina de ayuda carga y el contenedor principal es visible (documentacion equivalente a --help)."""
    open_fixture("help.html")
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="cli-help-root"]').is_displayed()


def test_help_title_text(driver, open_fixture):
    """Objetivo: comprobar que el titulo coincide con la salida de showHelp en ArgParser."""
    open_fixture("help.html")
    el = driver.find_element(By.ID, "help-title")
    assert "Customer Churn Predictor" in el.text


def test_help_lists_train_option(driver, open_fixture):
    """Objetivo: comprobar que la opcion --train esta documentada en la lista de opciones."""
    open_fixture("help.html")
    assert "--train" in driver.find_element(By.CSS_SELECTOR, '[data-testid="opt-train"]').text


def test_help_lists_predict_option(driver, open_fixture):
    """Objetivo: comprobar que la opcion --predict esta documentada."""
    open_fixture("help.html")
    assert "--predict" in driver.find_element(By.CSS_SELECTOR, '[data-testid="opt-predict"]').text


def test_help_lists_evaluate_combo(driver, open_fixture):
    """Objetivo: comprobar que el modo --train --evaluate aparece como en el CLI real."""
    open_fixture("help.html")
    txt = driver.find_element(By.CSS_SELECTOR, '[data-testid="opt-train-eval"]').text
    assert "--evaluate" in txt and "--train" in txt


def test_help_log_directory_note(driver, open_fixture):
    """Objetivo: comprobar el aviso de logs con ruta logs/ alineado a Logger y al texto de ayuda del programa."""
    open_fixture("help.html")
    note = driver.find_element(By.CSS_SELECTOR, '[data-testid="logs-note"]').text
    assert "logs/" in note


def test_help_usage_line_has_executable(driver, open_fixture):
    """Objetivo: comprobar que la linea de uso incluye el nombre del ejecutable logistic_churn."""
    open_fixture("help.html")
    assert "logistic_churn" in driver.find_element(By.ID, "usage-line").text


def test_help_example_train_command(driver, open_fixture):
    """Objetivo: comprobar que el bloque de ejemplos incluye el comando de entrenamiento documentado."""
    open_fixture("help.html")
    assert "./logistic_churn --train" in driver.find_element(
        By.CSS_SELECTOR, '[data-testid="ex-train"]'
    ).text


def test_help_example_evaluate_command(driver, open_fixture):
    """Objetivo: comprobar que el ejemplo con --evaluate esta presente."""
    open_fixture("help.html")
    assert "--evaluate" in driver.find_element(By.CSS_SELECTOR, '[data-testid="ex-eval"]').text


def test_help_example_predict_command(driver, open_fixture):
    """Objetivo: comprobar que el ejemplo de prediccion coincide con el flujo --predict."""
    open_fixture("help.html")
    assert "./logistic_churn --predict" in driver.find_element(
        By.CSS_SELECTOR, '[data-testid="ex-predict"]'
    ).text


# --- Dashboard y navegacion entre fixtures ---


def test_dashboard_title(driver, open_fixture):
    """Objetivo: comprobar que el dashboard identifica el producto Customer Churn Predictor."""
    open_fixture("dashboard.html")
    assert "Customer Churn" in driver.find_element(By.CSS_SELECTOR, '[data-testid="dashboard-title"]').text


def test_dashboard_nav_has_help_link(driver, open_fixture):
    """Objetivo: comprobar que el enlace de navegacion apunta a help.html (ruta relativa correcta)."""
    open_fixture("dashboard.html")
    link = driver.find_element(By.CSS_SELECTOR, '[data-testid="nav-help"]')
    assert link.get_attribute("href").endswith("help.html")


def test_dashboard_blurb_logistic(driver, open_fixture):
    """Objetivo: comprobar que el resumen menciona regresion logistica como en el nucleo del proyecto."""
    open_fixture("dashboard.html")
    assert "logistic regression" in driver.find_element(By.CSS_SELECTOR, '[data-testid="blurb-logistic"]').text


def test_dashboard_blurb_csv(driver, open_fixture):
    """Objetivo: comprobar que el resumen enlaza la idea de CSVReader con entrada/salida de datos."""
    open_fixture("dashboard.html")
    assert "CSVReader" in driver.find_element(By.CSS_SELECTOR, '[data-testid="blurb-csv"]').text


def test_dashboard_blurb_sgd(driver, open_fixture):
    """Objetivo: comprobar que el resumen documenta SGD como optimizador del modelo."""
    open_fixture("dashboard.html")
    assert "stochastic gradient descent" in driver.find_element(By.CSS_SELECTOR, '[data-testid="blurb-sgd"]').text


def test_dashboard_click_help_navigates(driver, open_fixture):
    """Objetivo: comprobar navegacion funcional: click en CLI help lleva al DOM de help.html."""
    open_fixture("dashboard.html")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="nav-help"]').click()
    _wait(driver).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="cli-help-root"]')))
    assert "Command Line Interface" in driver.find_element(By.ID, "help-title").text


# --- Train wizard ---


def test_train_page_title(driver, open_fixture):
    """Objetivo: comprobar que la pagina de entrenamiento declara el flujo equivalente a --train."""
    open_fixture("train.html")
    assert "Training wizard" in driver.find_element(By.CSS_SELECTOR, '[data-testid="train-page-title"]').text


def test_train_form_is_displayed(driver, open_fixture):
    """Objetivo: comprobar que el formulario de parametros de entrenamiento (collectTrainData) es visible."""
    open_fixture("train.html")
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="train-form"]').is_displayed()


def test_train_dataset_input_required_attr(driver, open_fixture):
    """Objetivo: comprobar que la ruta del dataset CSV se marca como obligatoria (aria-required)."""
    open_fixture("train.html")
    inp = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-dataset"]')
    assert inp.get_attribute("aria-required") == "true"


def test_train_output_input_required_attr(driver, open_fixture):
    """Objetivo: comprobar que la ruta de salida del modelo JSON se marca como obligatoria."""
    open_fixture("train.html")
    inp = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-output"]')
    assert inp.get_attribute("aria-required") == "true"


def test_train_header_y_selectable(driver, open_fixture):
    """Objetivo: comprobar interaccion: opcion de cabecera CSV 'y' es seleccionable como en el prompt y/n."""
    open_fixture("train.html")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="header-y"]').click()
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="header-y"]').is_selected()


def test_train_header_n_selectable(driver, open_fixture):
    """Objetivo: comprobar interaccion: opcion 'n' para CSV sin cabecera."""
    open_fixture("train.html")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="header-n"]').click()
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="header-n"]').is_selected()


def test_train_churn_index_field(driver, open_fixture):
    """Objetivo: comprobar que existe campo para indice de columna objetivo (0-based) como pide el CLI."""
    open_fixture("train.html")
    val = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-churn"]').get_attribute("value")
    assert val == "5"


def test_train_drop_hint_visible(driver, open_fixture):
    """Objetivo: comprobar texto de ayuda para columnas a descartar alineado al prompt del programa."""
    open_fixture("train.html")
    assert "weakly correlated" in driver.find_element(By.CSS_SELECTOR, '[data-testid="drop-hint"]').text


def test_train_learning_rate_default(driver, open_fixture):
    """Objetivo: comprobar que el campo learning rate tiene valor por defecto razonable (alpha)."""
    open_fixture("train.html")
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="input-alpha"]').get_attribute("value") == "0.01"


def test_train_epochs_default(driver, open_fixture):
    """Objetivo: comprobar que el campo epochs tiene valor por defecto para pruebas rapidas en fixture."""
    open_fixture("train.html")
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="input-epochs"]').get_attribute("value") == "100"


def test_train_submit_shows_result_when_valid(driver, open_fixture):
    """Objetivo: comprobar flujo feliz del formulario: con rutas no vacias muestra panel de resumen."""
    open_fixture("train.html")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="input-dataset"]').send_keys("data/x.csv")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="input-output"]').send_keys("models/w.json")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="btn-submit-train"]').click()
    _wait(driver).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="train-result"]')))
    assert "Summary" in driver.find_element(By.CSS_SELECTOR, '[data-testid="train-result-text"]').text


def test_train_empty_dataset_shows_error(driver, open_fixture):
    """Objetivo: comprobar validacion: sin ruta de dataset el formulario muestra error (parametro obligatorio FR-02)."""
    open_fixture("train.html")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="input-dataset"]').clear()
    driver.find_element(By.CSS_SELECTOR, '[data-testid="input-output"]').send_keys("out.json")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="btn-submit-train"]').click()
    _wait(driver).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="train-error"]')))
    assert "required" in driver.find_element(By.CSS_SELECTOR, '[data-testid="train-error"]').text.lower()


def test_train_dataset_placeholder(driver, open_fixture):
    """Objetivo: comprobar que el placeholder guia hacia un CSV de ejemplo como en el README."""
    open_fixture("train.html")
    ph = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-dataset"]').get_attribute("placeholder")
    assert "customer_data.csv" in ph


def test_train_output_placeholder(driver, open_fixture):
    """Objetivo: comprobar placeholder de salida hacia JSON de pesos como en FR-07."""
    open_fixture("train.html")
    ph = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-output"]').get_attribute("placeholder")
    assert "weights.json" in ph


def test_train_fr02_trace_note(driver, open_fixture):
    """Objetivo: comprobar trazabilidad a FR-02 (parametros de entrada en modo train)."""
    open_fixture("train.html")
    assert "FR-02" in driver.find_element(By.CSS_SELECTOR, '[data-testid="fr02-note"]').text


def test_train_norm_doc_visible(driver, open_fixture):
    """Objetivo: comprobar que la UI documenta normalizacion mean/std alineada a FR-04 y preprocess."""
    open_fixture("train.html")
    assert "mean 0" in driver.find_element(By.CSS_SELECTOR, '[data-testid="norm-doc"]').text


def test_train_encode_doc_visible(driver, open_fixture):
    """Objetivo: comprobar mencion de one-hot encoding coherente con preprocess del codigo."""
    open_fixture("train.html")
    assert "one-hot" in driver.find_element(By.CSS_SELECTOR, '[data-testid="encode-doc"]').text


def test_train_drops_textarea_exists(driver, open_fixture):
    """Objetivo: comprobar que columnas a eliminar usan area multilinea como lista separada por espacios."""
    open_fixture("train.html")
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="input-drops"]').tag_name.lower() == "textarea"


# --- Predict wizard ---


def test_predict_title(driver, open_fixture):
    """Objetivo: comprobar que la pagina declara el flujo equivalente a --predict."""
    open_fixture("predict.html")
    assert "Prediction wizard" in driver.find_element(By.CSS_SELECTOR, '[data-testid="predict-title"]').text


def test_predict_weights_required(driver, open_fixture):
    """Objetivo: comprobar que la ruta del JSON de pesos es obligatoria (primer prompt en collectPredictData)."""
    open_fixture("predict.html")
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="input-weights"]').get_attribute("required")


def test_predict_dataset_required(driver, open_fixture):
    """Objetivo: comprobar que el CSV de entrada a predecir es obligatorio."""
    open_fixture("predict.html")
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="input-predict-dataset"]').get_attribute("required")


def test_predict_output_required(driver, open_fixture):
    """Objetivo: comprobar que la ruta de salida de predicciones es obligatoria."""
    open_fixture("predict.html")
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="input-predict-output"]').get_attribute("required")


def test_predict_header_toggle(driver, open_fixture):
    """Objetivo: comprobar interaccion del flag de cabecera y/n en modo predict."""
    open_fixture("predict.html")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="pheader-n"]').click()
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="pheader-n"]').is_selected()


def test_predict_fr09_note(driver, open_fixture):
    """Objetivo: comprobar trazabilidad a FR-09 (orden y campos de predict)."""
    open_fixture("predict.html")
    assert "FR-09" in driver.find_element(By.CSS_SELECTOR, '[data-testid="fr09-note"]').text


def test_predict_json_hint(driver, open_fixture):
    """Objetivo: comprobar que se documenta formato JSON de modelo (pesos + bias)."""
    open_fixture("predict.html")
    assert "JSON" in driver.find_element(By.CSS_SELECTOR, '[data-testid="json-hint"]').text


def test_predict_csv_hint(driver, open_fixture):
    """Objetivo: comprobar referencia a FR-10 (salida CSV una probabilidad por fila)."""
    open_fixture("predict.html")
    assert "FR-10" in driver.find_element(By.CSS_SELECTOR, '[data-testid="csv-hint"]').text


def test_predict_submit_shows_result(driver, open_fixture):
    """Objetivo: comprobar flujo feliz: rellenar pesos, datos y salida muestra panel de vista previa."""
    open_fixture("predict.html")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="input-weights"]').send_keys("m.json")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="input-predict-dataset"]').send_keys("d.csv")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="input-predict-output"]').send_keys("p.csv")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="btn-predict-run"]').click()
    _wait(driver).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="predict-result"]')))


def test_predict_weights_placeholder(driver, open_fixture):
    """Objetivo: comprobar placeholder de archivo de pesos alineado a model.save JSON."""
    open_fixture("predict.html")
    assert "weights.json" in driver.find_element(By.CSS_SELECTOR, '[data-testid="input-weights"]').get_attribute(
        "placeholder"
    )


def test_predict_drops_area_exists(driver, open_fixture):
    """Objetivo: comprobar que existe campo opcional para indices de columnas a descartar en predict."""
    open_fixture("predict.html")
    assert driver.find_element(By.CSS_SELECTOR, '[data-testid="input-predict-drops"]').is_displayed()


# --- Metricas evaluate ---


def test_metrics_accuracy_label(driver, open_fixture):
    """Objetivo: comprobar etiqueta Accuracy como en la salida de handleEvaluate."""
    open_fixture("metrics.html")
    assert "Accuracy" in driver.find_element(By.CSS_SELECTOR, '[data-testid="lbl-accuracy"]').text


def test_metrics_precision_label(driver, open_fixture):
    """Objetivo: comprobar etiqueta Precision en bloque de metricas."""
    open_fixture("metrics.html")
    assert "Precision" in driver.find_element(By.CSS_SELECTOR, '[data-testid="lbl-precision"]').text


def test_metrics_recall_label(driver, open_fixture):
    """Objetivo: comprobar etiqueta Recall en bloque de metricas."""
    open_fixture("metrics.html")
    assert "Recall" in driver.find_element(By.CSS_SELECTOR, '[data-testid="lbl-recall"]').text


def test_metrics_f1_label(driver, open_fixture):
    """Objetivo: comprobar etiqueta F1 score como en cout del programa."""
    open_fixture("metrics.html")
    assert "F1" in driver.find_element(By.CSS_SELECTOR, '[data-testid="lbl-f1"]').text


def test_metrics_sample_block_matches_handle_evaluate(driver, open_fixture):
    """Objetivo: comprobar que el bloque de ejemplo replica el formato Accuracy:/Precision:/... del CLI."""
    open_fixture("metrics.html")
    block = driver.find_element(By.CSS_SELECTOR, '[data-testid="sample-cli-out"]').text
    assert "Accuracy:" in block and "F1 score:" in block


def test_metrics_fr08_note(driver, open_fixture):
    """Objetivo: comprobar trazabilidad a FR-08 (metricas en train --evaluate)."""
    open_fixture("metrics.html")
    assert "FR-08" in driver.find_element(By.CSS_SELECTOR, '[data-testid="fr08"]').text


# --- Preprocesado y datos ---


def test_pre_yes_no_mapping_text(driver, open_fixture):
    """Objetivo: comprobar documentacion de mapeo yes/no a 1.0/0.0 (FR-04)."""
    open_fixture("preprocessing.html")
    assert "1.0" in driver.find_element(By.CSS_SELECTOR, '[data-testid="yes-no-map"]').text


def test_pre_normalization_text(driver, open_fixture):
    """Objetivo: comprobar texto sobre normalizacion z-score (FR-04)."""
    open_fixture("preprocessing.html")
    assert "z-score" in driver.find_element(By.CSS_SELECTOR, '[data-testid="norm-text"]').text


def test_pre_onehot_text(driver, open_fixture):
    """Objetivo: comprobar mencion de one-hot para categoricas (FR-04)."""
    open_fixture("preprocessing.html")
    assert "one-hot" in driver.find_element(By.CSS_SELECTOR, '[data-testid="onehot-text"]').text


def test_pre_fr03_csv_validation(driver, open_fixture):
    """Objetivo: comprobar documentacion de validacion CSV por filas inconsistentes (FR-03)."""
    open_fixture("preprocessing.html")
    assert "unequal" in driver.find_element(By.CSS_SELECTOR, '[data-testid="fr03-csv"]').text


def test_pre_split_8020(driver, open_fixture):
    """Objetivo: comprobar documentacion del split 80/20 (FR-05 y RandomSplitter)."""
    open_fixture("preprocessing.html")
    txt = driver.find_element(By.CSS_SELECTOR, '[data-testid="split8020"]').text
    assert "80%" in txt and "20%" in txt


# --- Arquitectura y persistencia ---


def test_arch_vector_module(driver, open_fixture):
    """Objetivo: comprobar que la pagina de arquitectura incluye modulo Vector del codigo fuente."""
    open_fixture("architecture.html")
    assert "Vector" in driver.find_element(By.CSS_SELECTOR, '[data-testid="mod-vector"]').text


def test_arch_matrix_module(driver, open_fixture):
    """Objetivo: comprobar mencion de Matrix en mapa de modulos."""
    open_fixture("architecture.html")
    assert "Matrix" in driver.find_element(By.CSS_SELECTOR, '[data-testid="mod-matrix"]').text


def test_arch_splitter_module(driver, open_fixture):
    """Objetivo: comprobar mencion de Splitter para particion train/test."""
    open_fixture("architecture.html")
    assert "Splitter" in driver.find_element(By.CSS_SELECTOR, '[data-testid="mod-splitter"]').text


def test_arch_unknown_option_doc(driver, open_fixture):
    """Objetivo: comprobar documentacion del error Unknown option de ArgParser::run."""
    open_fixture("architecture.html")
    assert "Unknown option" in driver.find_element(By.CSS_SELECTOR, '[data-testid="cli-unknown"]').text


def test_persist_fr07_json(driver, open_fixture):
    """Objetivo: comprobar FR-07 (persistencia JSON con pesos y bias)."""
    open_fixture("persistence.html")
    assert "FR-07" in driver.find_element(By.CSS_SELECTOR, '[data-testid="fr07"]').text


def test_persist_fr11_load(driver, open_fixture):
    """Objetivo: comprobar FR-11 (cargar modelo guardado para inferencia)."""
    open_fixture("persistence.html")
    assert "FR-11" in driver.find_element(By.CSS_SELECTOR, '[data-testid="fr11"]').text


def test_persist_fr06_sgd(driver, open_fixture):
    """Objetivo: comprobar FR-06 (entrenamiento con actualizacion SGD)."""
    open_fixture("persistence.html")
    assert "FR-06" in driver.find_element(By.CSS_SELECTOR, '[data-testid="fr06"]').text


def test_persist_nfr_catch2(driver, open_fixture):
    """Objetivo: comprobar referencia a pruebas unitarias Catch2 (NFR-03) como complemento a Selenium."""
    open_fixture("persistence.html")
    assert "Catch2" in driver.find_element(By.CSS_SELECTOR, '[data-testid="nfr-tests"]').text


def test_arch_logger_logs_dir(driver, open_fixture):
    """Objetivo: comprobar que Logger se documenta con carpeta logs/."""
    open_fixture("architecture.html")
    assert "logs/" in driver.find_element(By.CSS_SELECTOR, '[data-testid="mod-logger"]').text


def test_arch_csvreader_module(driver, open_fixture):
    """Objetivo: comprobar modulo CSVReader en mapa de arquitectura."""
    open_fixture("architecture.html")
    assert "CSVReader" in driver.find_element(By.CSS_SELECTOR, '[data-testid="mod-csv"]').text


def test_dashboard_nav_arch_link(driver, open_fixture):
    """Objetivo: comprobar href del enlace a architecture.html desde el dashboard."""
    open_fixture("dashboard.html")
    assert "architecture.html" in driver.find_element(
        By.CSS_SELECTOR, '[data-testid="nav-arch"]'
    ).get_attribute("href")
