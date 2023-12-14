# MovieLover

As a movie enthusiast, I find it's challenging to locate venues and showtimes for non-mainstream films. That's why my project, MovieLover, came to fruition! Audiences can easily discover showtimes for the movies they want to watch and add them to their Google Calendar! 
I hope everyone enjoys it and has a great time at the movies!

## Technique
### Frontend
+ HTML
+ CSS
+ Javascript

### Backend
+ Deploying website with docker
+ Using Python/Flask environment
+ Following RESTful API 
+ Using BeautifulSoup4 & Selenium to scrape movies info
+ Saving data in AWS RDS MySQL database
+ Apply SSL Certificate and HTTPS with AWS ELB

## System Architecture
![image](/Image/System%20Architecture.jpg)

## Function Introduction
### Homepage
Show a list of movies in theaters, users can click in to get more information.
![image](/Image/Movie%20index.jpg)

### Movie Page
Show information about the movie and a button that users can add to their favorite list.
![image](/Image/Movie%20Info%20top.jpg)

Show all the screenings users can select by date, time, and theaters.
Then, the link above information can let users add screening to their Google calendar.
![image](/Image/Movie%20Info%20bot.jpg)

### Favorite Page
Show User's Favorite Movie. 
![image](/Image/Favorite.jpg)

### Search Bar
Every page has a nav bar where users can search for the title of movies.
![image](/Image/Search%20Bar.jpg)