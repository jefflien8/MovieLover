# MovieLover

As a movie lover, I always have a significant problem finding non-mainstream movie screenings, so I create a solution to fix my problem.
_MovieLover_ is a website that contains movie screenings in Taipei's theaters.
Users can easily find their favorite movie screening and add it to their Google calendar.

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