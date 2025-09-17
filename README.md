# social-media-api-capstone
ALX Capstone Project: Social Media API using Django and DRF
Given that it's 09:42 AM WAT on Wednesday, September 17, 2025, and your Social Media API project is at the deployment stage, your `README.md` should be comprehensive, clear, and up-to-date to reflect your progress. Below is an updated template tailored to your project, including the deployment status and other completed components. You can copy this into your `README.md` file in the `social-media-api-capstone` repository.

---

# Social Media API Capstone Project

## Overview
This is my ALX Capstone Project, a backend API for a social media platform built using Django and Django REST Framework (DRF). The API enables users to create profiles, post content, follow others, view a personalized feed, and engage with posts through likes and comments. It addresses the need for a scalable, secure backend to support social media functionality.

## Features
- **User Management**: Create, read, update, and delete user profiles with optional fields like bio, location, and profile picture.
- **Post Management**: CRUD operations for posts with optional media URLs.
- **Follow System**: Users can follow/unfollow others, with prevention of self-following.
- **Feed**: View posts from followed users and yourself in reverse chronological order.
- **Likes and Comments**: Users can like and comment on posts (stretch goals).
- **Profile Customization**: Add location, website, and cover photo to profiles (stretch goal).
- **Authentication**: Token-based authentication for secure access.
- **Pagination**: Paginated responses for large datasets.

## Deployment
The API is deployed on Heroku. The base URL is:
- **https://social-media-api-capstone.herokuapp.com/api/**  
  (Note: Replace with your actual Heroku app URL if different.)

### How to Access
- Test endpoints in an incognito window or with tools like Postman.
- Example: Get posts with a token: `GET https://social-media-api-capstone.herokuapp.com/api/posts/ -H "Authorization: Token <your_token>"`.

## Setup Instructions
To run locally:
1. Clone the repo: `git clone https://github.com/yourusername/social-media-api-capstone.git`.
2. Navigate to the project: `cd social-media-api-capstone/social_media_api`.
3. Create a virtual environment: `python -m venv venv`.
4. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows).
5. Install dependencies: `pip install -r requirements.txt`.
6. Apply migrations: `python manage.py migrate`.
7. Create a superuser: `python manage.py createsuperuser`.
8. Run the server: `python manage.py runserver`.

## Environment Variables
- `SECRET_KEY`: Set in Heroku or locally (e.g., in a `.env` file).
- `DATABASE_URL`: Auto-configured by Heroku PostgreSQL.

## Testing
Run tests with: `python manage.py test social.tests`.
Tests cover models, API endpoints, authentication, and functionality.

## Demo
Check out the project demo: [Loom Video Link]  
(Insert link after recording your 5-minute presentation.)

## Project Progress
- **Completed**: Models, API (serializers, views, URLs), admin interface, tests, deployment preparation.
- **Current Stage**: Deployed on Heroku, testing endpoints.
- **Next Steps**: Finalize stretch goals (e.g., notifications), optimize performance.

## Challenges
- Handled model validation (e.g., no self-following) with custom methods.
- Resolved URL mismatches in tests by aligning with DRF router.
- Managed authentication setup with token configuration.

## Contributors
- [Your Name] (you)

## License
[Add a license if applicable, e.g., MIT License]

---



