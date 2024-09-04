SELECT name FROM directors
INNER JOIN people ON directors.person_id = people.id
INNER JOIN movies ON directors.movie_id = movies.id
INNER JOIN ratings ON ratings.movie_id = movies.id
WHERE rating >= 9.0;