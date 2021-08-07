PROJECT TITLE ;

BOOK YOUR SALON APPOINTMENT

VIDEO DEMO ;
                    
                      https://youtu.be/LFWNZ0NQ1Jc

DESCRIPTION :

	
I have created a Web application using HTML,CSS,JAVASCRIPT,PYTHON and SQL. The website is created for online salon booking. Salon owners from specified cities can register with their salon details in our website. People can book their online appointment with their favourite salon with selected services, date , time.

In this project i have created Pages for salon registration,login, booking, success and appointment which is executed by using application.py page. 

In the Registration page salon owners can register with their details, which contains salon name, username,password ,city and address. All the details are stored in a database table called salon. The password is hashed using generate password hash.

In the index page I have created a link ref to booking page. In the booking page people/user can select their favourite salon which are registered on our website with DROPDOWN. It also holds radio  button to select their gender, It also contains CHECKBOX INSIDE SELECT OPTION which i have created using JAVASCRIPT CODE  to select the required service and also created a DATE format using HTML and TIme can be selected using radio buttons and a input box with NAME and MOBILE NUMBER. Once the user have provided complete details the page will redirect to success page which show a message YOU ARE REGISTERED. The details entered in the booking page is stored in a database table called USER.

In the LOGIN route the salon owners can login using username and password. The show password checkbox is fixed using JAVASCRIPT CODE. once the  username and password is validated it will redirect to appointment page.The username is assigned to session[name].

APPOINTMENT Page will display the table which contains the username,gender,services,date, time of the user who had booked with their salon through our website. In the appointment route the salon name is selected using SQL Query with the session[name] and the table is displayed with user details.




