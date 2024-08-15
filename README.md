<img width="1519" alt="Screenshot 2024-08-15 at 9 12 11 AM" src="https://github.com/user-attachments/assets/4c6a82b2-1a0d-4d38-af73-aae6827783f9">
<img width="1519" alt="Screenshot 2024-08-15 at 9 16 51 AM" src="https://github.com/user-attachments/assets/9276ab22-5f81-40ee-8f51-b053cf84730b">
<img width="1519" alt="Screenshot 2024-08-15 at 9 20 32 AM" src="https://github.com/user-attachments/assets/2af5f883-6648-4787-b8e5-34771be77362">
<img width="1680" alt="Screenshot 2024-08-15 at 9 23 20 AM" src="https://github.com/user-attachments/assets/86d89b7a-ebf0-43b9-b05d-d6e29a97a18c">


# UFC Statistics Web Application

This project is a web application that provides detailed information about UFC fighters and events. The application scrapes data from the UFC website and presents it in a user-friendly interface. Users can search for fighters, view detailed statistics, and explore past and upcoming UFC events.


1. **Web Scraping**: The application scrapes fighter statistics and event details from the UFC website. It uses BeautifulSoup to parse the HTML and extract meaningful data. The scraping functions handle different types of data and parse various HTML structures, making it non-trivial.

2. **Data Processing**: After scraping, the data is processed to format event names, dates, and fighter statistics. The project handles edge cases like missing data and unknown dates, ensuring that the displayed information is accurate and user-friendly.

3. **Dynamic Search and Rendering**: The search functionality is dynamic, allowing users to search for fighters by name or nickname. The application processes the search query and returns results in real-time, showcasing an interactive user experience.

4. **Django Views and Templates**: The application integrates Django views to render pages dynamically. Each page displays detailed information, whether it's a list of events, a specific fighter's details, or search results. The templates are designed to be extendable and maintain a consistent look and feel.

### Files

#### `urls.py`
- Defines the URL patterns for the application, mapping each URL to the corresponding view function.
```
urlpatterns=[
    path("home",views.home,name='home'),
    path("fighters",views.all_fighters,name="all_fighters"),
    path("fighter/<str:first_name>/<str:last_name>",views.fighter_detail,name="fighter_detail"),
    path("fighter/search",views.search_fighter,name="search_fighter"),
    path('events/', views.display_events, name='display_events'),
]
```
#### `views.py`
- Contains the logic for handling requests, scraping data, processing information, and rendering templates.
    - **`all_fighters`**: Scrapes and returns a list of all UFC fighters.
    - **`fighter_detail`**: Retrieves and displays detailed statistics for a specific fighter.
    - **`all_events`**: Scrapes and returns past UFC events.
    - **`scrape_upcoming_events`**: Scrapes and returns upcoming UFC events.
    - **`search_fighter`**: Handles the search functionality for finding fighters based on user input.

#### `templates/stats/home.html`
- The homepage template that displays upcoming fights, includes a search feature for fighters and link to all past events.

#### `templates/stats/search_results.html`
- Displays the search results for fighters based on the user query.

#### `templates/stats/fighter_detail.html`
- Displays detailed statistics for a specific fighter, including personal details and fight records.

#### `templates/stats/all_events.html`
- Lists all past UFC events with their respective details.

#### `static/styles.css`
- Contains the styling for the HTML templates to maintain a consistent and polished look.

### How to Run the Application

1. **Clone the repository**:
   ```
   git clone https://github.com/GavinWang-2024/UFC_stats_site.git
   cd UFC_stats_site
   ```
2. **Install Python packages**:
   ```
   pip install requests
   pip install BeautifulSoup4
   ```
