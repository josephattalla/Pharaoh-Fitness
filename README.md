# Pharaoh Fitness

This project is a gym membership management system implemented using Python, Flask, sqlite, HTML/CSS/JavaScript. The system allows users to register for a gym membership, purchase different membership plans, and view the remaining days of their membership.

## Features

- User Registration: New users can create an account by providing a unique username and a secure password. The system ensures password complexity requirements.
- User Authentication: Registered users can log in securely using their credentials. Passwords are hashed for security.
- Membership Plans: Users can choose from various membership plans, including a free 7-day membership, a monthly membership, and a yearly membership.
- Membership Purchase: Users can purchase a membership plan, and the system tracks the membership start and end dates.
- Remaining Days Display: The system calculates and displays the number of days remaining in the user's membership. This information is displayed on the home page after login.
- Error Handling: The system provides appropriate error messages for various scenarios, such as invalid login credentials, duplicate username during registration, and membership plan purchase restrictions.

## Usage

```
pip install -r requirements.txt
flask run
```

## Demonstration
https://github.com/josephattalla/Pharaoh-Fitness/assets/121779512/1109b967-540d-45e3-90d4-3b1312ce25ee

