# E-commerce


User Authentication: api/auth/register ---> Register Users
                     api/auth/login ---> login with registered Users

Categories: api/categories/  ---> List of Categories
            api/categories/id/ --> Details of particular category

Products: api/products/  ---> List of Products
            api/products/id/ --> Details of particular Product
            POST/PUT/DELETE allowed for admin or product created user.

Cart:    api/cart/ — View current user's cart.
         Each user has one cart.

Cart Items: api/cart-items/ — List items in the user's cart.
            Post— Add an item to cart.
            Put — Update quantity of a cart item.
            Delete  — Remove an item from the cart.


Place Order: api/orders/ to add orders/
             Converts current user's cart into an order.
             Automatically creates OrderItems for each cart item.
             Clears the cart after placing the order.

Order History: api/orders/ — Lists all orders made by the authenticated user.
              Each order includes product details, quantity, and order timestamp.






