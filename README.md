# 🍽️ Full-Stack Restaurant Management & Ordering System

A modern, responsive, full-stack web application designed for restaurants to showcase their brand, manage menus, and streamline customer orders. Customers can view operational hours, locate the physical branch, browse the interactive menu, and place orders that seamlessly dispatch detailed invoices straight to the kitchen via an automated email notification system.

### 🔗 [Live Demo Link] | 🔗 [Video Walkthrough / Architecture Overview]

---

## 📌 Overview
This project bridges the gap between digital ordering and physical pickup. Built using a decoupled architecture (**Next.js** on the frontend for lightning-fast user experience and **Django** on the backend for robust data management), it provides a frictionless workflow for both users and restaurant staff. 

Instead of relying on expensive third-party POS integrations, the application uses an elegant backend email dispatch system. When a user submits an order, a structured summary is instantly generated and emailed to the restaurant, allowing staff to prepare the food for customer pickup.

## ⚙️ Core Features
* **Interactive Dynamic Menu:** Users can browse food categories, view prices, and explore descriptions updated directly from the database.
* **Streamlined Ordering System:** An intuitive checkout flow where users can review their cart items and submit pickup orders.
* **Automated Kitchen Dispatch (Email Integration):** Leverages backend SMTP protocols to instantly send structured order summaries to the restaurant's operational email for immediate preparation.
* **Essential Business Info:** High-visibility sections for restaurant location maps, operational working hours, and contact details.
* **Admin Dashboard:** Powered by Django's native admin panel, allowing restaurant managers to easily update menu items, prices, and availability without changing code.

## 🛠️ Tech Stack & Architecture

### Frontend
* **Framework:** Next.js (React)
* **Styling:** CSS Modules / Tailwind CSS (Optional: change this based on what you used)
* **State Management:** React Context API / Hooks (Optional: change this based on what you used)

### Backend
* **Framework:** Django (Python)
* **Database:** SQLite (Development) / PostgreSQL (Production)
* **Notification Layer:** Django Core Mail (SMTP Integration)

---

## 📐 Architecture Flow
```text
[ Next.js Frontend ] ──(Submit Order API)──> [ Django Backend ]
                                                     │
                                             (Triggers SMTP)
                                                     │
                                                     ▼
                                        [ Restaurant Kitchen Email ]
                                        (Staff Prepares Food for Pickup)
