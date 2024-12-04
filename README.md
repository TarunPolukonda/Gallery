# Dynamic Gallery Web Application

## Project Overview
The **Dynamic Gallery Web Application** is a web-based platform that allows users to manage and view images efficiently. Built using Flask and MySQL, the application supports CRUD operations for image management, ensuring a seamless and responsive user experience.

## Features
- **Responsive Design**: Optimized for all devices, ensuring accessibility across desktops, tablets, and smartphones.
- **CRUD Functionality**: Users can upload, delete, and organize images in specific categories or albums.
- **Dynamic Image Loading**: Efficient retrieval and display of images using optimized SQL queries.
- **Interactive UI**: Features like image previews, zooming, and sorting options for an enhanced user experience.
- **Category Management**: Images can be filtered and sorted based on categories for easier navigation.
- **Cloud Deployment**: The application is scalable and reliable, deployed on a cloud platform (e.g., AWS).

## Technology Stack
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: AWS (or your preferred cloud provider)

## Installation
### Prerequisites
- Python 3.7+
- MySQL Server
- Pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/dynamic-gallery.git
   cd dynamic-gallery
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the database:
   - Create a MySQL database.
   - Import the schema from `schema.sql`:
     ```bash
     mysql -u your-username -p your-database < schema.sql
     ```
   - Update database credentials in `config.py`.
4. Run the application:
   ```bash
   flask run
   ```
5. Access the application at `http://127.0.0.1:5000`.

## Usage
1. **Upload Images**: Navigate to the upload page to add images to the gallery.
2. **View Gallery**: Browse images categorized by albums or tags.
3. **Manage Images**: Edit, delete, or reorganize images as needed.

## Project Structure
```
|-- dynamic-gallery/
    |-- static/        # CSS, JavaScript, and images
    |-- templates/     # HTML templates
    |-- app.py         # Main application
    |-- config.py      # Configuration file
    |-- data.sql     # Database schema
    |-- requirements.txt
```


Thank you for exploring the Dynamic Gallery Web Application!

