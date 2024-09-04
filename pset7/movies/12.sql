SELECT title FROM stars
INNER JOIN people ON stars.person_id = people.id
INNER JOIN movies ON stars.movie_id = movies.id
WHERE name = 'Helena Bonham Carter'

INTERSECT

SELECT title FROM stars
INNER JOIN people ON stars.person_id = people.id
INNER JOIN movies ON stars.movie_id = movies.id
WHERE name = 'Johnny Depp'