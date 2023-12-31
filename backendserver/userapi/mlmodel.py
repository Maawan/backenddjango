# -*- coding: utf-8 -*-
"""finale Golmal3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R2Jy3-B6FQMg6D98pzOumaopUZS50gaA
"""

import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import matplotlib.pyplot as plt
import pickle

Dailyweekly='daily'

file_path = 'imdb_top_1000.csv'
movies_df = pd.read_csv(file_path)

pfile_path = 'huihui.csv'
priority_df = pd.read_csv(pfile_path)

new_dataset_file = 'newmodel.csv'  # Replace with the actual file path

movies_df["combined_features"] = (
    movies_df["Genre"]
    + " "
    + movies_df["Director"]
    + " "
    + movies_df["Star1"]
    + " "
    + movies_df["Star2"]
    + " "
    + movies_df["Star3"]
    + " "
    + movies_df["Released_Year"].astype(str)  # Include Released_Year as a string in the combined_features
)

# Create a TF-IDF vectorizer to convert text data to numerical vectors
tfidf_vectorizer = TfidfVectorizer()

# Save the model to a pickled file
model_file_path = 'model.pkl'

with open(model_file_path, 'wb') as file:
    pickle.dump(tfidf_vectorizer, file)

model_file_path = 'model.pkl'  # Replace with the actual file path where the model is saved
with open(model_file_path, 'rb') as file:
    loaded_model = pickle.load(file)

# Transform the 'combined_features' into TF-IDF vectors
tfidf_matrix = loaded_model.fit_transform(movies_df["combined_features"])

# Compute the cosine similarity between movies based on their TF-IDF vectors
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get top N similar movies with similarity scores
def get_similar_movies(movie_names, priority_list, n=4):
    # Check if any movie in the priority_list is in the dataset
    found_movies = [movie for movie in priority_list if movie in movies_df["Series_Title"].values]

    # If priority_list movies found, get their similarity scores using content-based recommender
    similar_movies_with_score = []
    for movie in found_movies:
        movie_indices = [
            movies_df.index[movies_df["Series_Title"] == movie_name].tolist()[0]
            for movie_name in movie_names
        ]
        similar_scores = list(enumerate(cosine_sim[movie_indices[-1]]))
        similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
        similarity_score = next((score[1] for score in similar_scores if movies_df["Series_Title"].iloc[score[0]] == movie), 0.0)
        if similarity_score >= 0.6:
            release_year = movies_df["Released_Year"].iloc[movie_indices[-1]]
            similar_movies_with_score.append((movie, release_year, similarity_score))

    # Sort the priority list movies based on similarity score in descending order
    similar_movies_with_score.sort(key=lambda x: x[2], reverse=True)

    # If priority_list movies found and meet the similarity threshold, return them as predictions with their similarity scores
    if similar_movies_with_score:
        return similar_movies_with_score

    # If none of the priority_list movies found, use content-based recommendation
    movie_indices = [
        movies_df.index[movies_df["Series_Title"] == movie_name].tolist()[0]
        for movie_name in movie_names
    ]
    similar_scores = list(enumerate(cosine_sim[movie_indices[-1]]))
    similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
    similar_scores = [score for score in similar_scores if score[0] not in movie_indices]
    similar_movies = [
        (movies_df["Series_Title"].iloc[score[0]], movies_df["Released_Year"].iloc[score[0]], score[1])
        for score in similar_scores[:n]
    ]
    return similar_movies

input_movies = [
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "Pulp Fiction",
    "The Lord of the Rings: The Return of the King",
]

series_titles=priority_df["Series_Title"]

# Print the Series_Title column
# print(series_titles)

priority_list = series_titles

# print(priority_list)

recommended_movies = get_similar_movies(input_movies, priority_list, n=5)

# for movie in recommended_movies:
#     print(movie)

movie_names = [movie[0] for movie in recommended_movies]

# print(movie_names)

# # Print the recommended movies with release year and similarity scores
# print("Recommended movies:")
# for i, (movie, release_year, score) in enumerate(recommended_movies, start=1):
#     print(f"{i}. {movie} (Released: {release_year}, Similarity Score: {score:.2f})")

# print(movie_names)

import pandas as pd
import random

# Load the old dataset (movies dataset) from your CSV file
old_dataset_file = 'imdb_top_1000.csv'  # Replace with the actual file path
movies_df = pd.read_csv(old_dataset_file)

# Function to get the recommended movies from the movie recommender system
def get_recommended_movies():
    # Replace this with the output from the movie recommender system
    recommended_movies =movie_names
    return recommended_movies

# Function to get a task based on the genre and a randomly selected factor attribute
def get_task(movie_title, new_dataset, preference):
    task = "Neutral Task"
    task_description = ""
    selected_factor = ""
    selected_genre = ""
    reward_points = 0

    movie_genre = movies_df[movies_df["Series_Title"] == movie_title]["Genre"].iloc[0]

    # Check if the movie genre matches any genre in the new dataset's Rel_Genre
    matched_tasks = new_dataset[new_dataset["Rel_Genre"].str.contains(movie_genre, case=False)]

    if not matched_tasks.empty:
        # Randomly select a factor attribute from the matched tasks
        selected_factor = random.choice(matched_tasks["Factor"].values)

        # Get the task associated with the randomly selected factor
        matched_task = matched_tasks[matched_tasks["Factor"] == selected_factor]
        if not matched_task.empty:
            task = matched_task["Task_Name"].iloc[0]
            task_description = matched_task["Task_Description"].iloc[0]
            reward_points = matched_task["Reward (Virtual Coins)"].iloc[0]

            # Get the genre of the selected movie
            selected_genre = movies_df[movies_df["Series_Title"] == movie_title]["Genre"].iloc[0]

    # If genre is not matched, assign a neutral task
    if not selected_genre:
        task_frame = "Daily" if preference == "daily" else "Weekly"
        neutral_tasks = new_dataset[new_dataset["Frame"] == task_frame]
        if not neutral_tasks.empty:
            selected_task = random.choice(neutral_tasks["Task_Name"].values)
            task = f"{selected_task} (Neutral)"
            task_description = neutral_tasks[neutral_tasks["Task_Name"] == selected_task]["Task_Description"].iloc[0]
            selected_factor = neutral_tasks[neutral_tasks["Task_Name"] == selected_task]["Factor"].iloc[0]
            reward_points = neutral_tasks[neutral_tasks["Task_Name"] == selected_task]["Reward (Virtual Coins)"].iloc[0]

    # Determine if the task should be daily or weekly based on user's preference
    task_frequency = "Daily" if preference == "daily" else "Weekly"

    return task, task_description, selected_factor, task_frequency, selected_genre, reward_points

# Load the new dataset (tasks dataset) from your CSV file

new_dataset = pd.read_csv(new_dataset_file)

# Get user's preference for daily or weekly tasks
user_preference = Dailyweekly.lower()

# Get recommended movies from the movie recommender system
recommended_movies = get_recommended_movies()

# Loop through the recommended movies and get the task information for each movie
json_data=[]
for movie in recommended_movies:
    task, task_description, selected_factor, task_frequency, selected_genre, reward_points = get_task(movie, new_dataset, user_preference)

    # Print the movie name, genre, reward points, the corresponding task, task description, selected factor, and task frequency
    data = {
    "Movie for Task": f"{movie} ({selected_genre})",
    "Task": f"{task} ({task_frequency})",
    "Task Description": task_description,
    "Selected Factor": selected_factor,
    "Reward Points": reward_points,
    }
    print(f"Movie for Task: {movie} ({selected_genre})")
    print(f"Task: {task} ({task_frequency})")
    print(f"Task Description: {task_description}")
    print(f"Selected Factor: {selected_factor}")
    print(f"Reward Points: {reward_points}")
    print("=" * 30)
    json_data.append(json.dumps(data))



print(json_data)

