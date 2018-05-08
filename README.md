# Generalized Recommendation Service 

### This Django-based service uses singular value decomposition to perform general recommendations based on user interactions with some set of products or concepts. 

### API

#### /users/:user/products/:product/activities
GET or POST user activity related to a product
#### /users/:user/recs/
GET recommendations of products suggested for a user
#### /users
GET or POST existing or new users
#### /products
GET or POST existing or new products
