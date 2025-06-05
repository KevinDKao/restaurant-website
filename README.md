# 🍽️ Restaurant Reviews App

A beautiful and modern restaurant reviewing application built with Python Dash. Discover restaurants, read reviews, and share your dining experiences!

## ✨ Features

- **Beautiful Modern UI**: Clean, responsive design with Bootstrap styling
- **Restaurant Discovery**: Browse restaurants with rich information and images
- **Advanced Filtering**: Filter by cuisine, location, price range, and rating
- **Detailed Restaurant Pages**: Complete information including photos, contact details, and reviews
- **Review System**: 5-star rating system with detailed written reviews
- **Interactive Navigation**: Multi-page application with smooth navigation
- **Sample Data**: Pre-loaded with 5 sample restaurants and reviews

## 🚀 Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd restaurant-website
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your web browser and navigate to:
```
http://127.0.0.1:8050
```

## 🎯 Usage

### Home Page
- Browse all restaurants with beautiful cards showing photos, ratings, and key information
- Use the search bar to find specific restaurants
- Filter restaurants by:
  - Cuisine type (French, Japanese, Italian, Indian, American)
  - Location (Downtown, Midtown, Little Italy, Uptown, Financial District)
  - Price range ($, $$, $$$, $$$$)
  - Sort by rating or name

### Restaurant Details
- Click "View Details" on any restaurant card to see the full restaurant page
- View complete restaurant information including:
  - High-quality photos
  - Contact information (phone, address)
  - Average rating and review count
  - All customer reviews with ratings and dates

### Adding Reviews
- Click "Add Review" in the navigation or "Write Review" on restaurant pages
- Select a restaurant from the dropdown
- Enter your name and rating (1-5 stars)
- Write your detailed review
- Submit to add your review to the restaurant

## 🏗️ Technical Details

### Built With
- **Python Dash**: Modern web framework for Python
- **Plotly**: Interactive plotting library
- **Bootstrap 5**: Modern CSS framework for responsive design
- **Unsplash Images**: High-quality stock photos for restaurants

### Features Implemented
- Multi-page routing with `dcc.Location`
- Interactive callbacks for filtering and navigation
- Responsive grid layout for restaurant cards
- Star rating system with visual feedback
- Modern gradient design and hover effects
- Form handling for review submissions

### Sample Restaurants Included
1. **The Garden Bistro** - French cuisine, Downtown ($$$)
2. **Sakura Sushi** - Japanese cuisine, Midtown ($$)
3. **Mama Mia Pizzeria** - Italian cuisine, Little Italy ($)
4. **Spice Route** - Indian cuisine, Uptown ($$)
5. **The Steakhouse** - American cuisine, Financial District ($$$$)

## 🎨 UI/UX Features

- **Gradient Hero Section**: Eye-catching header with search functionality
- **Card-Based Layout**: Modern card design with hover animations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Intuitive Navigation**: Clear navigation with breadcrumbs and back buttons
- **Visual Feedback**: Hover effects, loading states, and interactive elements
- **Professional Typography**: Clean, readable fonts and proper spacing

## 🔧 Customization

The app is designed to be easily customizable:

- **Add More Restaurants**: Extend the `restaurants_data` list in `app.py`
- **Modify Styling**: Update the CSS in the `app.index_string` section
- **Add New Features**: Extend the callbacks and layout functions
- **Database Integration**: Replace the in-memory data with a proper database

## 📱 Responsive Design

The application is fully responsive and works great on:
- Desktop computers
- Tablets
- Mobile phones
- Different screen sizes and orientations

Enjoy exploring restaurants and sharing your dining experiences! 🍴
