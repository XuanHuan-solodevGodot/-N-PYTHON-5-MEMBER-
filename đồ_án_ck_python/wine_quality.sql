
CREATE DATABASE IF NOT EXISTS wine_quality_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE wine_quality_db;

DROP TABLE IF EXISTS prediction_history;
DROP TABLE IF EXISTS model_results;
DROP TABLE IF EXISTS wine_data;

CREATE TABLE wine_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_label INT NOT NULL,
    alcohol DECIMAL(5,2),
    malic_acid DECIMAL(5,2),
    ash DECIMAL(5,2),
    alcalinity_of_ash DECIMAL(5,2),
    magnesium INT,
    total_phenols DECIMAL(5,2),
    flavanoids DECIMAL(5,2),
    nonflavanoid_phenols DECIMAL(5,2),
    proanthocyanins DECIMAL(5,2),
    color_intensity DECIMAL(6,2),
    hue DECIMAL(5,2),
    od280_od315 DECIMAL(5,2),
    proline INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE model_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    accuracy DECIMAL(5,2),
    precision_score DECIMAL(5,2),
    recall_score DECIMAL(5,2),
    f1_score DECIMAL(5,2),
    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prediction_history (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    alcohol DECIMAL(5,2),
    malic_acid DECIMAL(5,2),
    ash DECIMAL(5,2),
    alcalinity_of_ash DECIMAL(5,2),
    magnesium INT,
    total_phenols DECIMAL(5,2),
    flavanoids DECIMAL(5,2),
    nonflavanoid_phenols DECIMAL(5,2),
    proanthocyanins DECIMAL(5,2),
    color_intensity DECIMAL(6,2),
    hue DECIMAL(5,2),
    od280_od315 DECIMAL(5,2),
    proline INT,
    predicted_class INT,
    confidence_score DECIMAL(5,2),
    prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO model_results
(model_name, accuracy, precision_score, recall_score, f1_score)
VALUES
('KNN',95.00,95.00,95.00,95.00),
('Decision Tree',93.00,93.00,93.00,93.00),
('Random Forest',98.00,98.00,98.00,98.00);
