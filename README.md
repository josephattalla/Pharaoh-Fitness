# Pharaoh Fitness
#### Description:
This project is a gym membership management system implemented using Python, Flask, sqlite, HTML/CSS/JavaScript. The system allows users to register for a gym membership, purchase different membership plans, and view the remaining days of their membership.

<strong><h5>Features</h5></strong>
<ul>
  <li>User Registration: New users can create an account by providing a unique username and a secure password. The system ensures password complexity requirements.</li>
  <li>User Authentication: Registered users can log in securely using their credentials. Passwords are hashed for security.</li>
  <li>Membership Plans: Users can choose from various membership plans, including a free 7-day membership, a monthly membership, and a yearly membership.</li>
  <li>Membership Purchase: Users can purchase a membership plan, and the system tracks the membership start and end dates.</li>
  <li>Remaining Days Display: The system calculates and displays the number of days remaining in the user's membership. This information is displayed on the home page after login.</li>
  <li>Error Handling: The system provides appropriate error messages for various scenarios, such as invalid login credentials, duplicate username during registration, and membership plan purchase restrictions.</li>
</ul>

<strong><h5>Project Structure</h5></strong>
<ul>
  <li>app.py: Contains the Flask application and routes.</li>
  <li>templates/: Directory containing HTML templates for the web pages.</li>
  <li>gym.db: SQLite database file storing user information, memberships, and purchase history.</li>
</ul>
