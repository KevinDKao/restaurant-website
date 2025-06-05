import dash
from dash import dcc, html, Input, Output, State, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
from datetime import date
import uuid

# Sample restaurant data
restaurants_data = [
    {
        'id': '1',
        'name': 'The Garden Bistro',
        'cuisine': 'French',
        'location': 'Downtown',
        'price_range': '$$$',
        'image': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop',
        'description': 'Elegant French cuisine in a cozy garden setting with seasonal menus.',
        'phone': '(555) 123-4567',
        'address': '123 Main St, Downtown'
    },
    {
        'id': '2',
        'name': 'Sakura Sushi',
        'cuisine': 'Japanese',
        'location': 'Midtown',
        'price_range': '$$',
        'image': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop',
        'description': 'Authentic Japanese sushi bar with fresh ingredients and traditional preparation.',
        'phone': '(555) 234-5678',
        'address': '456 Oak Ave, Midtown'
    },
    {
        'id': '3',
        'name': 'Mama Mia Pizzeria',
        'cuisine': 'Italian',
        'location': 'Little Italy',
        'price_range': '$',
        'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop',
        'description': 'Family-owned pizzeria serving authentic wood-fired pizzas since 1952.',
        'phone': '(555) 345-6789',
        'address': '789 Pine St, Little Italy'
    },
    {
        'id': '4',
        'name': 'Spice Route',
        'cuisine': 'Indian',
        'location': 'Uptown',
        'price_range': '$$',
        'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop',
        'description': 'Modern Indian cuisine with traditional spices and contemporary presentation.',
        'phone': '(555) 456-7890',
        'address': '321 Elm St, Uptown'
    },
    {
        'id': '5',
        'name': 'The Steakhouse',
        'cuisine': 'American',
        'location': 'Financial District',
        'price_range': '$$$$',
        'image': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400&h=300&fit=crop',
        'description': 'Premium steaks and fine dining experience in an upscale atmosphere.',
        'phone': '(555) 567-8901',
        'address': '654 Broadway, Financial District'
    }
]

# Sample reviews data
reviews_data = [
    {
        'id': str(uuid.uuid4()),
        'restaurant_id': '1',
        'reviewer_name': 'Sarah Johnson',
        'rating': 5,
        'review_text': 'Absolutely amazing! The coq au vin was perfection and the service was impeccable.',
        'date': '2024-01-15'
    },
    {
        'id': str(uuid.uuid4()),
        'restaurant_id': '1',
        'reviewer_name': 'Mike Chen',
        'rating': 4,
        'review_text': 'Great atmosphere and delicious food. The wine selection is excellent.',
        'date': '2024-01-10'
    },
    {
        'id': str(uuid.uuid4()),
        'restaurant_id': '2',
        'reviewer_name': 'Emma Wilson',
        'rating': 5,
        'review_text': 'Best sushi in town! Fresh fish and perfect rice. The chef is a true artist.',
        'date': '2024-01-12'
    },
    {
        'id': str(uuid.uuid4()),
        'restaurant_id': '3',
        'reviewer_name': 'David Brown',
        'rating': 4,
        'review_text': 'Authentic Italian pizza with a perfect crust. Great value for money!',
        'date': '2024-01-08'
    }
]

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Restaurant Reviews"

# Define styles
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

def create_header():
    return html.Div([
        html.Nav([
            html.Div([
                html.A([
                    html.H1("🍽️ Restaurant Reviews", className="navbar-brand")
                ], href="/", className="navbar-brand"),
                html.Div([
                    html.A("Home", href="/", className="nav-link"),
                    html.A("Add Review", href="/add-review", className="nav-link")
                ], className="navbar-nav")
            ], className="container")
        ], className="navbar navbar-expand-lg navbar-dark bg-primary")
    ])

def create_star_rating(rating):
    stars = []
    for i in range(5):
        if i < rating:
            stars.append(html.Span("★", className="star filled"))
        else:
            stars.append(html.Span("☆", className="star"))
    return html.Div(stars, className="star-rating")

def create_restaurant_card(restaurant):
    avg_rating = calculate_average_rating(restaurant['id'])
    review_count = len([r for r in reviews_data if r['restaurant_id'] == restaurant['id']])
    
    return html.Div([
        html.Div([
            html.Img(src=restaurant['image'], className="card-img-top"),
            html.Div([
                html.H5(restaurant['name'], className="card-title"),
                html.P([
                    html.Span(f"{restaurant['cuisine']} • ", className="cuisine"),
                    html.Span(f"{restaurant['location']} • ", className="location"),
                    html.Span(restaurant['price_range'], className="price")
                ], className="card-subtitle"),
                html.P(restaurant['description'], className="card-text"),
                html.Div([
                    create_star_rating(avg_rating),
                    html.Span(f" ({review_count} reviews)", className="review-count")
                ], className="rating-section"),
                html.Div([
                    html.A("View Details", href=f"/restaurant/{restaurant['id']}", 
                          className="btn btn-primary btn-sm"),
                    html.A("Write Review", href=f"/add-review?restaurant_id={restaurant['id']}", 
                          className="btn btn-outline-primary btn-sm")
                ], className="card-actions")
            ], className="card-body")
        ], className="card restaurant-card")
    ], className="col-md-6 col-lg-4 mb-4")

def calculate_average_rating(restaurant_id):
    restaurant_reviews = [r for r in reviews_data if r['restaurant_id'] == restaurant_id]
    if not restaurant_reviews:
        return 0
    return round(sum(r['rating'] for r in restaurant_reviews) / len(restaurant_reviews), 1)

def create_home_page():
    return html.Div([
        create_header(),
        html.Div([
            # Hero section
            html.Div([
                html.Div([
                    html.H1("Discover Amazing Restaurants", className="display-4"),
                    html.P("Find and review the best dining experiences in your city", 
                          className="lead"),
                    html.Div([
                        dcc.Input(
                            id="search-input",
                            type="text",
                            placeholder="Search restaurants...",
                            className="form-control search-input"
                        ),
                        html.Button("Search", className="btn btn-primary search-btn")
                    ], className="search-section")
                ], className="hero-content")
            ], className="hero-section"),
            
            # Filters
            html.Div([
                html.Div([
                    html.H4("Filter by:"),
                    html.Div([
                        html.Div([
                            html.Label("Cuisine:"),
                            dcc.Dropdown(
                                id="cuisine-filter",
                                options=[
                                    {'label': 'All Cuisines', 'value': 'all'},
                                    {'label': 'French', 'value': 'French'},
                                    {'label': 'Japanese', 'value': 'Japanese'},
                                    {'label': 'Italian', 'value': 'Italian'},
                                    {'label': 'Indian', 'value': 'Indian'},
                                    {'label': 'American', 'value': 'American'}
                                ],
                                value='all',
                                className="form-select"
                            )
                        ], className="col-md-3"),
                        html.Div([
                            html.Label("Location:"),
                            dcc.Dropdown(
                                id="location-filter",
                                options=[
                                    {'label': 'All Locations', 'value': 'all'},
                                    {'label': 'Downtown', 'value': 'Downtown'},
                                    {'label': 'Midtown', 'value': 'Midtown'},
                                    {'label': 'Little Italy', 'value': 'Little Italy'},
                                    {'label': 'Uptown', 'value': 'Uptown'},
                                    {'label': 'Financial District', 'value': 'Financial District'}
                                ],
                                value='all',
                                className="form-select"
                            )
                        ], className="col-md-3"),
                        html.Div([
                            html.Label("Price Range:"),
                            dcc.Dropdown(
                                id="price-filter",
                                options=[
                                    {'label': 'All Prices', 'value': 'all'},
                                    {'label': '$', 'value': '$'},
                                    {'label': '$$', 'value': '$$'},
                                    {'label': '$$$', 'value': '$$$'},
                                    {'label': '$$$$', 'value': '$$$$'}
                                ],
                                value='all',
                                className="form-select"
                            )
                        ], className="col-md-3"),
                        html.Div([
                            html.Label("Sort by:"),
                            dcc.Dropdown(
                                id="sort-filter",
                                options=[
                                    {'label': 'Rating (High to Low)', 'value': 'rating_desc'},
                                    {'label': 'Rating (Low to High)', 'value': 'rating_asc'},
                                    {'label': 'Name (A-Z)', 'value': 'name_asc'},
                                    {'label': 'Name (Z-A)', 'value': 'name_desc'}
                                ],
                                value='rating_desc',
                                className="form-select"
                            )
                        ], className="col-md-3")
                    ], className="row")
                ], className="container")
            ], className="filters-section"),
            
            # Restaurant grid
            html.Div([
                html.Div([
                    html.Div(id="restaurants-grid", className="row")
                ], className="container")
            ], className="restaurants-section")
        ])
    ])

def create_restaurant_detail_page(restaurant_id):
    restaurant = next((r for r in restaurants_data if r['id'] == restaurant_id), None)
    if not restaurant:
        return html.Div([
            create_header(),
            html.Div([
                html.H1("Restaurant not found", className="text-center")
            ], className="container")
        ])
    
    restaurant_reviews = [r for r in reviews_data if r['restaurant_id'] == restaurant_id]
    avg_rating = calculate_average_rating(restaurant_id)
    
    return html.Div([
        create_header(),
        html.Div([
            html.Div([
                html.Div([
                    html.Img(src=restaurant['image'], className="restaurant-hero-img")
                ], className="col-md-6"),
                html.Div([
                    html.H1(restaurant['name']),
                    html.Div([
                        create_star_rating(avg_rating),
                        html.Span(f" {avg_rating}/5 ({len(restaurant_reviews)} reviews)", 
                                className="rating-text")
                    ], className="rating-section"),
                    html.P([
                        html.Strong("Cuisine: "), restaurant['cuisine']
                    ]),
                    html.P([
                        html.Strong("Location: "), restaurant['location']
                    ]),
                    html.P([
                        html.Strong("Price Range: "), restaurant['price_range']
                    ]),
                    html.P([
                        html.Strong("Phone: "), restaurant['phone']
                    ]),
                    html.P([
                        html.Strong("Address: "), restaurant['address']
                    ]),
                    html.P(restaurant['description']),
                    html.A("Write a Review", 
                          href=f"/add-review?restaurant_id={restaurant_id}",
                          className="btn btn-primary")
                ], className="col-md-6")
            ], className="row restaurant-details"),
            
            html.Hr(),
            
            html.H3("Reviews"),
            html.Div([
                create_review_card(review) for review in restaurant_reviews
            ] if restaurant_reviews else [
                html.P("No reviews yet. Be the first to review this restaurant!")
            ], className="reviews-section")
        ], className="container")
    ])

def create_review_card(review):
    return html.Div([
        html.Div([
            html.Div([
                html.H6(review['reviewer_name']),
                html.Small(review['date'], className="text-muted")
            ], className="review-header"),
            create_star_rating(review['rating']),
            html.P(review['review_text'], className="review-text")
        ], className="card-body")
    ], className="card review-card mb-3")

def create_add_review_page():
    return html.Div([
        create_header(),
        html.Div([
            html.Div([
                html.H2("Write a Review"),
                html.Form([
                    html.Div([
                        html.Label("Select Restaurant:"),
                        dcc.Dropdown(
                            id="review-restaurant-select",
                            options=[
                                {'label': restaurant['name'], 'value': restaurant['id']}
                                for restaurant in restaurants_data
                            ],
                            placeholder="Choose a restaurant...",
                            className="form-select"
                        )
                    ], className="mb-3"),
                    
                    html.Div([
                        html.Label("Your Name:"),
                        dcc.Input(
                            id="reviewer-name",
                            type="text",
                            placeholder="Enter your name",
                            className="form-control"
                        )
                    ], className="mb-3"),
                    
                    html.Div([
                        html.Label("Rating:"),
                        dcc.Dropdown(
                            id="rating-select",
                            options=[
                                {'label': '★★★★★ (5 stars)', 'value': 5},
                                {'label': '★★★★☆ (4 stars)', 'value': 4},
                                {'label': '★★★☆☆ (3 stars)', 'value': 3},
                                {'label': '★★☆☆☆ (2 stars)', 'value': 2},
                                {'label': '★☆☆☆☆ (1 star)', 'value': 1}
                            ],
                            placeholder="Select rating...",
                            className="form-select"
                        )
                    ], className="mb-3"),
                    
                    html.Div([
                        html.Label("Review:"),
                        dcc.Textarea(
                            id="review-text",
                            placeholder="Write your review here...",
                            className="form-control",
                            style={'height': '150px'}
                        )
                    ], className="mb-3"),
                    
                    html.Button("Submit Review", id="submit-review", 
                              className="btn btn-primary")
                ])
            ], className="col-md-8 mx-auto")
        ], className="container")
    ])

# Callbacks
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/add-review':
        return create_add_review_page()
    elif pathname and pathname.startswith('/restaurant/'):
        restaurant_id = pathname.split('/')[-1]
        return create_restaurant_detail_page(restaurant_id)
    else:
        return create_home_page()

@app.callback(
    Output('restaurants-grid', 'children'),
    [Input('cuisine-filter', 'value'),
     Input('location-filter', 'value'),
     Input('price-filter', 'value'),
     Input('sort-filter', 'value')]
)
def update_restaurants_grid(cuisine, location, price, sort_by):
    filtered_restaurants = restaurants_data.copy()
    
    # Apply filters
    if cuisine != 'all':
        filtered_restaurants = [r for r in filtered_restaurants if r['cuisine'] == cuisine]
    if location != 'all':
        filtered_restaurants = [r for r in filtered_restaurants if r['location'] == location]
    if price != 'all':
        filtered_restaurants = [r for r in filtered_restaurants if r['price_range'] == price]
    
    # Apply sorting
    if sort_by == 'rating_desc':
        filtered_restaurants.sort(key=lambda x: calculate_average_rating(x['id']), reverse=True)
    elif sort_by == 'rating_asc':
        filtered_restaurants.sort(key=lambda x: calculate_average_rating(x['id']))
    elif sort_by == 'name_asc':
        filtered_restaurants.sort(key=lambda x: x['name'])
    elif sort_by == 'name_desc':
        filtered_restaurants.sort(key=lambda x: x['name'], reverse=True)
    
    return [create_restaurant_card(restaurant) for restaurant in filtered_restaurants]

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8f9fa;
            }
            
            .hero-section {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 80px 0;
                text-align: center;
            }
            
            .hero-content h1 {
                font-size: 3.5rem;
                margin-bottom: 1rem;
                font-weight: 700;
            }
            
            .search-section {
                max-width: 600px;
                margin: 2rem auto;
                display: flex;
                gap: 10px;
            }
            
            .search-input {
                flex: 1;
                padding: 12px 20px;
                border: none;
                border-radius: 25px;
                font-size: 16px;
            }
            
            .search-btn {
                padding: 12px 30px;
                border-radius: 25px;
                border: none;
                background-color: #ff6b6b;
                color: white;
                font-weight: 600;
            }
            
            .filters-section {
                background-color: white;
                padding: 30px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .restaurants-section {
                padding: 50px 0;
            }
            
            .restaurant-card {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border: none;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .restaurant-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.2);
            }
            
            .card-img-top {
                height: 200px;
                object-fit: cover;
            }
            
            .star-rating {
                display: inline-block;
                margin: 10px 0;
            }
            
            .star {
                font-size: 18px;
                color: #ddd;
            }
            
            .star.filled {
                color: #ffd700;
            }
            
            .card-actions {
                display: flex;
                gap: 10px;
            }
            
            .btn {
                border-radius: 20px;
                padding: 8px 20px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .btn-primary {
                background-color: #667eea;
                border-color: #667eea;
            }
            
            .btn-primary:hover {
                background-color: #5a6fd8;
                border-color: #5a6fd8;
            }
            
            .btn-outline-primary {
                color: #667eea;
                border-color: #667eea;
            }
            
            .btn-outline-primary:hover {
                background-color: #667eea;
                border-color: #667eea;
            }
            
            .restaurant-details {
                padding: 50px 0;
            }
            
            .restaurant-hero-img {
                width: 100%;
                height: 400px;
                object-fit: cover;
                border-radius: 15px;
            }
            
            .rating-section {
                margin: 20px 0;
            }
            
            .rating-text {
                font-size: 18px;
                color: #666;
                margin-left: 10px;
            }
            
            .review-card {
                border-radius: 10px;
                border: none;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .review-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }
            
            .review-text {
                margin-top: 10px;
                line-height: 1.6;
            }
            
            .navbar-brand {
                font-size: 1.5rem;
                font-weight: 700;
            }
            
            .nav-link {
                font-weight: 500;
                margin: 0 15px;
                color: rgba(255,255,255,0.8) !important;
            }
            
            .nav-link:hover {
                color: white !important;
            }
            
            .form-control, .form-select {
                border-radius: 8px;
                border: 1px solid #ddd;
                padding: 10px 15px;
            }
            
            .form-control:focus, .form-select:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)