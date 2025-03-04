![Thumbnail](https://github.com/user-attachments/assets/cc789673-e251-4259-8920-80d451c0c152)

# Restaurant Reservation Management API

API for managing restaurant reservations with automatic table allocation and robust status tracking. Built for seamless integration with frontend applications and scalability for future features.

---

## 🚀 Features

- **User Authentication**: Secure login system with JWT, supporting role-based access control (Admin and Client).
- **Smart Table Assignment**: Automatically allocates tables based on real-time availability and reservation criteria.
- **Reservation Management**: Comprehensive support for reservation statuses: Pending, Confirmed, Cancelled, and Completed.
- **Scalable Architecture**: Designed with modularity in mind, leveraging Django best practices for maintainability.
- **API Ready for Frontend Integration**: Built with RESTful principles for seamless frontend integration.

---

## 📦 Current Version

### v1.0.0

> **Note:** This is a beta version. Features are still being tested, and breaking changes may occur as the project evolves.

For detailed version history, see the [CHANGELOG.md](CHANGELOG.md).

---

## 🌐 Complementary Frontend
This repository contains exclusively the code for the API of the restaurant reservation management application. Additionally, the development of the frontend, built with **React and Material UI (MUI)**, complements this project by providing a modern, intuitive, and fully functional user interface.

You can explore the frontend repository here [Restaurant Reservation Management Client](https://github.com/danielcaraballo/restaurant-reservations-client).

---

## 🛠️ Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/danielcaraballo/restaurant-reservations-api.git
   cd restaurant-reservation-api
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   - Create a `.env` file in the root directory.
   - Add the necessary environment variables. See `.env.example` for reference:

     ```
      SECRET_KEY=your-secret-key
      DEBUG=True
      ALLOWED_HOSTS=localhost,127.0.0.1
     ```

   - Rename `.env.example` to `.env` and update it with your values.

5. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` to access the API.

---

## 🤝 Contribution

We welcome contributions! Follow these steps to get started:

1. Fork the repository.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/danielcaraballo/restaurant-reservations-api.git
   ```
3. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes and commit them:
   ```bash
   git commit -m "type(scope): description of changes" #Using Conventional Commits
   ```
5. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Open a Pull Request.

---

## 👨‍💻 Maintainer

©2024 Developed by Dev. Project.

Feel free to contact us for any inquiries

📧 Email: devproject.ve@gmail.com

> If you find this project useful, consider starring ⭐ the repository to show your support!
