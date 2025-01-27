# Movie Recommendation System

This is a content-based movie recommender system which suggests related movies based on the movie selected by the user.
The deployed website can be visited [here](https://movie-recommendation-system-dp.streamlit.app/).

## Relevant Links

The dataset used for performing vectorization and similarity checking is the TMDB 5000 movies dataset which can be found [here](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
The details of the movies (title, genre, runtime, actors, poster, etc) are fetched using an API by the [Open Movie Database (OMDB)](https://www.themoviedb.org/documentation/api).

## Working

This system works using the following steps:

1. Extracting the relevant features from the dataset
2. Converting this data into a single tag string
3. Stemming and vectorizing this string
4. Creating a similarity matrix on these vectors
5. Finding the top movies which are most similar to the given movie

## Libraries Used

This project has been created entirely using Python. The libraries used are given below:

- **Scikit-Learn**: For vectorization and similarity measurement
- **NLTK**: For stemming the movie tags
- **Pandas**: For manipulating the dataset as a Pandas dataframe
- **Requests**: For fetching API data
- **Streamlit**: For creating the frontend
- Pickle, Urllib and AST for various functions
