SELECT AVG(rating) FROM movies
Join ratings ON movies.id = ratings.movie_id
WHERE year = 2012;