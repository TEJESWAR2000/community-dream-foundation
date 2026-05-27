"""
data_cleaning.py

Loads customer feedback data, performs cleaning and preprocessing,
and exports the cleaned dataset to cleaned_feedback.csv.
"""

import pandas as pd
import re

# Load dataset
df = pd.read_csv("customer_feedback.csv")

# Remove rows with missing or empty feedback
df = df.dropna(subset=["feedback_text"])
df = df[df["feedback_text"].str.strip() != ""]

# Remove duplicate rows
df = df.drop_duplicates()

# Convert text to lowercase
df["feedback_text"] = df["feedback_text"].str.lower()

# Remove punctuation and special characters
df["feedback_text"] = df["feedback_text"].apply(
    lambda text: re.sub(r"[^a-z0-9\s]", "", text)
)

# Define common English stop words
stop_words = {
    "the", "is", "and", "a", "an", "to", "of", "was", "but",
    "would", "not", "again", "i", "it", "this", "that", "in",
    "on", "for", "with", "as", "at", "by", "from"
}

# Tokenize text and remove stop words
def preprocess_text(text):
    tokens = text.split()
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return " ".join(filtered_tokens)

df["feedback_text"] = df["feedback_text"].apply(preprocess_text)

# Save cleaned data
df.to_csv("cleaned_feedback.csv", index=False)

print("Data cleaning complete. cleaned_feedback.csv generated successfully.")
