# Pharaoh Fitness
#### Video Demo:  <URL HERE>
#### Description:This project is a Gym Membership Management System implemented using Python, Flask, SQL, HTML, and CSS. The system allows users to register for a gym membership, purchase different membership plans, and view the remaining days of their membership.

Features
User Registration: New users can create an account by providing a unique username and a secure password. The system ensures password complexity requirements.

User Authentication: Registered users can log in securely using their credentials. Passwords are hashed for security.

Membership Plans: Users can choose from various membership plans, including a free 7-day membership, a monthly membership, and a yearly membership.

Membership Purchase: Users can purchase a membership plan, and the system tracks the membership start and end dates.

Remaining Days Display: The system calculates and displays the number of days remaining in the user's membership. This information is displayed on the home page after login.

Error Handling: The system provides appropriate error messages for various scenarios, such as invalid login credentials, duplicate username during registration, and membership plan purchase restrictions.

Project Structure
app.py: Contains the Flask application and routes.
templates/: Directory containing HTML templates for the web pages.
gym.db: SQLite database file storing user information, memberships, and purchase history.
Usage
Access the home page by visiting the root URL (/). If you are not logged in, you will be prompted to log in or register.

If you are a new user, click on the "Register" link to create an account. Provide a unique username and a secure password following the specified complexity requirements.

If you are an existing user, click on the "Log In" link to enter your username and password.

After logging in, you will see the number of days remaining in your membership, along with various membership plans you can purchase.

Click on the "Free 7-Day Membership", "Monthly Agreement", or "Yearly Agreement" button to purchase the corresponding membership plan. If you already have an active 7-day membership, you cannot purchase another free pass.

After purchasing a membership, the system will display the number of days remaining in your membership.

Click on the "Log Out" link at the top right corner to log out of your account.
