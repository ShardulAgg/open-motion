# Open Motion - Use AI to plan your work automatically, locally, for free

## Quick start: Get Google Authentication API credentials.json and paste it to backend folder 

1. Go to the Google Cloud Console (https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Google Calendar API for your project.
4. Go to the Credentials page.
5. Click "Create Credentials" and select "OAuth client ID".
6. Choose "Web Application" as the application type.
7. Add http://localhost:80/oauth2callback as redirect URL
8. Download the client configuration file (credentials.json).
9. Copy the downloaded credentials.json file to the `backend` folder of your project.


Ensure that the credentials.json file is properly placed in the backend folder before proceeding with the next steps.

## Quick Start: Run the backend and connect to Google Calendar

1. Navigate to the project root and open a terminal.
2. Enter the following commands:
```
   cd backend
   docker compose up --build
```
3. In a browser, open `http://localhost/docs`
4. Call `start_auth` and copy the link into a new tab, removing the double quotes.
5. Follow the Google Authentication instructions.

## Quick Start: Run the frontend

1. Navigate to the project root and open a terminal.
2. Enter the following commands:
```
   cd frontend
   npm install  # If not already performed
   npm start
```
3. Open `http://localhost:3000` in your browser.