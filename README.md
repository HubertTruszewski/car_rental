# AUTEX - Car rental project using Python

My first project written for PIPR subject at Warsaw University of Technology.

Program is running only in text mode in system console.

### Used technologies:
- sqlite3
- terminaltables

### Files:
- classes.py - definition of used class in program
- errors.py - custom errors
- modelio.py - communication with database
- main.py - main file of the project
- test_classes.py - unit tests written with pytest framework


### Functionality:
+ #### Cars:
  - Adding new car
  - Modifying car details
  - Searching for car using parameters or list all vehicles
  - Removing car from database
+ #### Reservations:
  - Adding new reservation
  - Modyfing reservation details
  - Cancelling reservation
+ #### Rentals:
  - Collecting reservation
  - Create rental without reservation
  - Showing list of unpaid rentals
  - Returning car