
---

# Library Management System API

This is a Library Management System API built as a personal project to manage a library's resources, including books, users, and borrowing transactions. It is implemented using **FastAPI** for rapid development, with **SQLModel** as the ORM for database interactions, and **Amazon S3** for file storage.

## Features

- **User Management**

  - **Registration & Authentication**: Allows users to sign up and log in, with JWT-based authentication.
  - **User Roles**: Role-based access for admins and members, with admin privileges for book and user management.
  - **Profile Management**: Users can manage their profile information.

- **Book Management**

  - **Add/Update/Delete Books**: Admins can add new books, update existing book details, and delete books from the library.
  - **Search and Filter**: Users can search for books by title, author, or genre.
  - **File Storage with S3**: Book cover images and other media are stored securely in Amazon S3.

- **Borrowing and Returning Books**

  - **Borrow Books**: Members can borrow books if copies are available.
  - **Return Books**: Members can return borrowed books, updating the availability in the library.
  - **Transaction Management**: Track borrowing and return activities, including due dates and return dates.

- **Overdue Management and Notifications**

  - **Overdue Notifications**: Notify members of overdue books.

- **Transaction History**
  - **Admin and Member Views**: Members can view their borrowing history, while admins can view all transactions.

## Tech Stack

- **Backend Framework**: FastAPI – for building the RESTful API with asynchronous request handling and a user-friendly auto-generated API documentation.
- **Database ORM**: SQLModel – used to interact with the database using Python objects and ensure efficient querying and model definition.
- **Database**: PostgreSQL – relational database for storing user, book, and transaction data.
- **Authentication**: JWT – for secure, token-based user authentication.
- **File Storage**: Amazon S3 – for storing book-related media files, like cover images.
- **Environment Management**: Docker – to ensure consistent development and deployment environments.

## Key Libraries

- **FastAPI**: Core web framework for building the API.
- **SQLModel**: ORM for managing data models and interacting with the database.
- **Boto3**: AWS SDK for handling file storage in Amazon S3.
- **PyJWT**: JSON Web Token library for handling authentication.

## Getting Started

### Prerequisites

- **Python 3.8+**
- **PostgreSQL** (configurable in the environment variables)
- **AWS S3 Bucket** with appropriate permissions
- **Docker** (optional, for containerized setup)

### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**

   Create a `.env` file to define environment variables for database connection, AWS credentials, and JWT secret.

   ```env
   DATABASE_URL=postgresql://username:password@localhost/library_db
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   S3_BUCKET_NAME=your_s3_bucket
   JWT_SECRET_KEY=your_jwt_secret
   ```

4. **Database Setup**

   Initialize the database by creating the necessary tables as defined by the SQLModel models. You can use FastAPI’s startup events or an external script to handle migrations.

5. **Run the Application**

   Start the FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

6. **API Documentation**

   Access the automatically generated API documentation at `http://localhost:8000/docs`.

### Deployment

You can deploy this project using Docker. Ensure you set up AWS credentials and environment variables on the target server.

---
