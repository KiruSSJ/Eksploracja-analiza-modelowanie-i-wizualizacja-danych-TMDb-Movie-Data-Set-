import requests
import json
import time

##miejsce na klucz nadany przez administratora api_key = 'xxxx' 

url = 'https://api.themoviedb.org/3/discover/movie'

# Parameters for the API request
params = {
    'api_key': api_key,
    'language': 'en-US',
    'sort_by': 'popularity.desc',
    'include_adult': 'false',
    'include_video': 'false',
    'primary_release_date.gte': '1950-01-01',
    'primary_release_date.lte': '2023-02-28',
    'vote_count.gte':300

}

# Collect data for the first 500 pages of results
movie_data = []
for page in range(1, 100):
    params['page'] = page
    response = requests.get(url, params=params)
    data = response.json()['results']
    movie_data.extend(data)
    time.sleep(0.5)
    
    # Add budget, revenue, keywords, runtime, genres, tagline, director, and cast data to each movie
    for movie in data:
        movie_id = movie['id']
        movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        movie_params = {'api_key': api_key, 'language': 'en-US', 'append_to_response': 'credits,keywords'}
        movie_response = requests.get(movie_url, params=movie_params)
        movie_details = movie_response.json()
        movie['genres'] = movie_details['genres']
        
        # Extract keywords from the movie data
        movie_keywords = [keyword['name'] for keyword in movie_details['keywords']['keywords']]
        movie['keywords'] = movie_keywords

        # Update the corresponding movie in the main movie_data list
        for i, m in enumerate(movie_data):
            if m['id'] == movie_id:
                movie_data[i] = movie

# Save the data to a JSON file
with open('C:/Users/kirmi/OneDrive/Pulpit/movie_data.json', 'w') as f:
    json.dump(movie_data, f)
