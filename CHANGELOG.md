# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

---

## v0.5.0 - 2024-12-10

### Added

- User authentication with JWT, including role-based permissions (Admin and Client).
- Smart table assignment logic based on area, date, time, and guest count.
- Reservation status management with states: Pending, Confirmed, Cancelled, and Completed.
- Modular backend architecture with Django, optimized for scalability and maintainability.

### Changed

- Updated environment variables handling with `.env` files for better configurability.
- Enhanced installation instructions in `README.md` for clarity.
