# Price Compare Website

#### Video Demo: https://youtu.be/xxxxxx

#### Description:

Price Compare Website is a shopping price comparison platform developed using Python, Django, HTML, CSS, and JavaScript. The goal is to help users quickly compare product prices across different platforms. Currently, the website supports popular Taiwanese shopping sites momo and PChome, with plans to expand to mainstream e-commerce platforms like Amazon and Shopee in the future.
This project serves as the final project for CS50x. Through this project, I aimed to gain deeper understanding of Django architecture and backend processing workflows, while combining frontend interactive technologies to create a practical product prototype. Since my ideal company uses Django as their primary web framework, I specifically chose Django over Flask or other lightweight frameworks, hoping to include this project in my job application portfolio.

### Features

- 🔍 **Real-time price comparison** across multiple e-commerce sites
- 📱 **Responsive UI** using Bootstrap
- ♾️ **Infinite scroll** using Intersection Observer
- 🔄 **Loading spinner** for smoother user experience
- 🔐 **User authentication system** (register/login/logout)
- 🕸️ **Custom-built web scrapers** using `requests` + `BeautifulSoup`
- 🗃️ **Future support for PostgreSQL and user preference storage**

### Why Django?

I selected **Django** instead of Flask or other minimal frameworks because:

- Django offers a robust and scalable architecture (MTV).
- It comes with built-in user authentication, ORM, routing, and admin panel.
- Many of the companies I'm targeting professionally use Django, so understanding it thoroughly increases my competitiveness.
- Django encourages clean code organization, which helps with long-term maintainability and testing.

### Database & Authentication

- The application currently uses **SQLite3** as its database during development.
- User information is stored using Django’s built-in `auth` system.
- Search records and product source information are handled in the backend but not yet stored persistently.
- Planned migration to **PostgreSQL** will support user preferences and performance improvements.
- User session management is handled by Django’s default session middleware using cookies.

### Frontend Interactivity

To create a dynamic and responsive user interface, the following features have been implemented:

- **Infinite Scroll**: Implemented using JavaScript’s `IntersectionObserver` to load more products as the user scrolls.
- **Loading Spinner**: Displays a spinner while waiting for AJAX responses or scraping data.
- **Bootstrap Integration**: Ensures mobile responsiveness and a clean layout.
- **Search Box**: Users can input product names to query results from all supported platforms.

---

### Challenges Encountered

Several challenges arose during the development process:

1. **Learning Django Structure**:
   I was new to Django, so understanding models, views, templates, URL routing, and app separation took considerable time. I followed the official documentation, tutorials, and MDN web docs to gradually piece everything together.

2. **Web Scraping Difficulties**:
   Since the e-commerce platforms I targeted (momo and PChome) do not provide official APIs, I had to rely on web scraping. I built custom scrapers using `requests` and `BeautifulSoup` to extract product details. I also had to deal with changing HTML structures and ensure stability and maintainability of the scrapers.

3. **Frontend/Backend Integration**:
   Coordinating Django views with JavaScript-based dynamic content loading required clear separation of concerns and careful testing. I used a service layer in Python to handle data fetching from scrapers before rendering them through views or returning JSON.

---

### File Structure
```bash
CS50-FINALPROJECT/
│
├── shopping/                # Django global setting， settings.py、urls.py 
│   ├── settings.py          # Lang, timezone, application settings
│   ├── urls.py              # Main route setting
│
├── shopping_app/            # Price Compare application
│   ├── templates/           # HTML (base.html, index.html)
│   ├── static/              # CSS, JS
│   │   ├── css/style.css
│   │   └── js/index.js
│   ├── scraper/             # scraper module
│   │   └── momo.py
|   |   └── pchome.py
│   ├── services.py          # scraper service
│   ├── views.py             # Django View，handle request and response
│   └── models.py            # Define database schema
│
├── Pipfile                  # pipenv virtual env settings
└── README.md                

```

---

### Most Challenging & Rewarding Features

The two most rewarding parts of this project are:

1. **Web Scraping System**:
   Designing flexible and robust scrapers that work across different HTML structures helped me understand how to deal with unreliable external data sources. This also laid the foundation for adding support for more platforms in the future.

2. **Django Integration**:
   Mastering how to organize Django applications, handle multiple routes, and maintain separation between logic and views was a rewarding experience. I now feel confident building larger Django-based projects in the future.

---

### Future Enhancements

-  Add support for more platforms: Amazon, Shopee, Rakuten, etc.
-  Migrate from SQLite to **PostgreSQL** for better scalability and performance
-  Store **user preferences**, e.g., default shopping websites
-  Add **search history and bookmarks**
-  Introduce **caching and rate limiting** for more efficient data retrieval
-  Improve **UI/UX**, including product charts and keyword suggestions
-  Consider integrating with official APIs if available

---

### Usage

1. Register a new account and log in.
2. Type a product name into the search field.
3. Scroll down to view more results as they are automatically loaded.
4. Log out when done.

> Note: If not logged in, search is still functional but limited in scope.
### Final Notes

This project represents a culmination of everything I’ve learned in CS50x: from backend architecture, web scraping, session handling, to frontend interactivity. I’m proud of the practical value this site provides and am excited to continue developing it beyond the course.
