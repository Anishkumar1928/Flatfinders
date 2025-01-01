# FlatFinders Repository

Welcome to the **FlatFinders** repository. This project aims to simplify finding rental accommodations by providing a seamless platform for property listings and searches.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Backend](#backend)
- [Frontend](#frontend)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

---

## Overview

FlatFinders is a comprehensive solution for renters and property owners. Renters can search for available properties by pin codes, while property owners can register, update, and manage their properties. The app also supports profile management, property photos, and authentication.

---

## Features

- **User Authentication:** Sign up, login, and secure token-based access.
- **Profile Management:** View, edit, and update user profiles.
- **Property Listings:** Add, view, update, and delete property details.
- **Search Properties:** Find properties by pin code or user-specific listings.
- **Image Management:** Upload and manage profile and property images using Firebase.
- **Responsive Frontend:** Designed with React Native for mobile-first access.

---

## Backend

- **Framework:** Flask
- **Database:** PostgreSQL
- **Storage:** Firebase for images

### Key Endpoints:

- **User Authentication:**
  - `POST /signup`
  - `POST /login`

- **Profile Management:**
  - `PUT /update_profile`
  - `GET /getprofile`

- **Property Management:**
  - `POST /property`
  - `POST /getproperty`
  - `POST /deleteproperty`

For detailed API documentation, refer to the [Backend Code](backendcode.txt).

---

## Frontend

- **Framework:** React Native
- **Navigation:** React Navigation
- **State Management:** Context API
- **Persistent Storage:** AsyncStorage

### Key Screens:

- **Authentication:** Login and Signup
- **Home:** Displays local property listings
- **Profile:** View and edit user profile
- **Property Registration:** Add new properties
- **Property Details:** View detailed property information

For more details, refer to the [Frontend Code](frontendcode.txt).

---

## Technologies Used

- **Backend:** Flask, PostgreSQL, Firebase
- **Frontend:** React Native, Expo
- **Authentication:** JWT (JSON Web Tokens)
- **Image Storage:** Firebase Storage
- **Dependencies:** Listed in `requirements.txt`

---

## Installation

### Backend:
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```

### Frontend:
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the application:
   ```bash
   npm start
   ```

---

## Usage

1. Run the backend server.
2. Start the frontend application.
3. Access the application on a mobile device or emulator.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
