This is SleeveNote.

It's a web app whose purpose is to enable the user to discover
new releases [updated every Friday], search for albums, tracks
and artists, as well as personalize their profiles where they
can list their favorite records and set their profile header
to an image of their favorite artist.

SleeveNote was written in python using flask. And SQL
was used to store user's data in a database akin to its
function in the finance problem set.

Spotify's API is the backbone of the app and although working
extensively with APIs wasn't covered in this course it was
crucial for the app's ability to function. so the code dealing
with that was taken from a youtube tutorial dealing with the
topic, but i DID type it myself and i understand every line of
code.

Jinja2 was extensively used in the html code in order to
display the JSON data sent by the API.

It should be noted that i didn't write the html/css code
from scratch, instead i used a free template (credited in
the comments on top of every html file) and edited it to
fit the project, which explains why the homepage has a
video background which greatly exceeds my coding capabilities.
Though itshould be noted that i did make that vide myself.

It should also be noted that certain features weren't captured
in the screencast such as that when you rest the pointer on a
record's artwork a title showing the record's title and
artist's name pops up. Also, that in the new releases page
there's a drop down menu that enbales the user to display
the new releases relevant to a particular country.

The Register, login and logout functions were directly taken
from the finance distribution code and the code written for
that problem set.

This is SleeveNote. This was CS50.