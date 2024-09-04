SELECT DISTINCT name FROM stars
INNER JOIN people ON stars.person_id = people.id
INNER JOIN movies ON stars.movie_id = movies.id
WHERE year = 2004
ORDER BY birth, name ASC;