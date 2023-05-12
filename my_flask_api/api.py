from my_flask_api.app import api, app
from my_flask_api.views.user_views import UserView, UsersView, UserGoogleLogin
from my_flask_api.views.amazon_products_views import ProductsView, ProductScraperView

# User views
api.add_resource(UserView, "/users:register")
api.add_resource(UsersView, "/users")
api.add_resource(UserGoogleLogin, "/users/google_login")

api.add_resource(ProductsView, "/products")
api.add_resource(ProductScraperView, "/products:scrape")


if __name__ == "__main__":
    app.run(debug=True, port=5005, host="0.0.0.0")
