import pandas as pd

from database import get_connection
from config import FEATURE_COLUMNS


def empty_wine_df():
    return pd.DataFrame(columns=["id", "class_label"] + FEATURE_COLUMNS + ["created_at"])


def load_wine_data():
    """Loads the wine_data table. Returns (dataframe, error_message_or_None)."""
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM wine_data", conn)
        conn.close()
        return df, None
    except Exception as e:
        return empty_wine_df(), str(e)


def load_prediction_history():
    """Loads prediction_history, newest first. Returns (dataframe, error_message_or_None)."""
    try:
        conn = get_connection()
        query = "SELECT * FROM prediction_history ORDER BY prediction_id DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return pd.DataFrame(), str(e)


def save_prediction(values, prediction, probability):
    """Inserts one prediction row into prediction_history."""
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO prediction_history(
        alcohol, malic_acid, ash, alcalinity_of_ash, magnesium,
        total_phenols, flavanoids, nonflavanoid_phenols,
        proanthocyanins, color_intensity, hue, od280_od315, proline,
        predicted_class, confidence_score
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (*values, int(prediction), float(probability)))
    conn.commit()

    cursor.close()
    conn.close()
    