---
title: Discerner API Reference

language_tabs:
  - python

toc_footers:
  - <a href='https://www.discernerapi.com'>Sign Up for a Developer Key</a>

includes:
  - errors

search: true
---

# Introduction

Welcome to the Discerner API! 

We have language bindings in Python and nothing else! You can view code examples in the dark area to the right, and you can switch the programming language of the examples with the tabs in the top right.

# Authentication

> To authorize, use this code:

```python
import requests
import json

response = requests.post("http://discernerapi.com/token", {"username":your_username, "password":your_password})
token = json.loads(response.text)["token"]
auth_string = "token " + token

users = requests.get("http://discernerapi.com/users", headers = {"authorization": token_string})

```
> Make sure to replace `API_KEY` with your API key.

You can register for credentials at [discernerapi.com](http://discernerapi.com/).

Post that username and password to "/token" to receive a token which can be used to validate all future requests. The token can then be sent as an "Authorization" header with "Token " prepended. That looks like the following:

`Authorization: Token YOUR_TOKEN`

<aside class="notice">
You must replace <code>YOUR_TOKEN</code> with your personal API token.
</aside>

# Users

## Get All Users

```python
import requests
import json

response = requests.post("http://discernerapi.com/token", {"username":your_username, "password":your_password})
token = json.loads(response.text)["token"]
auth_string = "token " + token

users = requests.get("http://discernerapi.com/users", headers = {"authorization": token_string})
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1
  },
  {
    "id": 2
  }
]
```

This endpoint retrieves all users.

### HTTP Request

`GET http://discernerapi.com/users`

## Create a New User

```python
import requests
import json

response = requests.post("http://discernerapi.com/token", {"username":your_username, "password":your_password})
token = json.loads(response.text)["token"]
auth_string = "token " + token

new_user = requests.post("http://discernerapi.com/users", headers = {"authorization": token_string})
```

> The above command returns JSON structured like this:

```json
  {
    "id": 1
  }
```

This endpoint creates a user and returns the new user's id.

### HTTP Request

`POST http://discernerapi.com/users`

# Products

## Get All Products

```python
import requests
import json

response = requests.post("http://discernerapi.com/token", {"username":your_username, "password":your_password})
token = json.loads(response.text)["token"]
auth_string = "token " + token

users = requests.get("http://discernerapi.com/products", headers = {"authorization": token_string})
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1
  },
  {
    "id": 2
  }
]
```

This endpoint retrieves all products.

### HTTP Request

`GET http://discernerapi.com/products`

## Create a New Product

```python
import requests
import json

response = requests.post("http://discernerapi.com/token", {"username":your_username, "password":your_password})
token = json.loads(response.text)["token"]
auth_string = "token " + token

new_user = requests.post("http://discernerapi.com/products", headers = {"authorization": token_string})
```

> The above command returns JSON structured like this:

```json
  {
    "id": 1
  }
```

This endpoint creates a product and returns the new product's id.

### HTTP Request

`POST http://discernerapi.com/products`

# Activity

## Get All Activities

```python
import requests
import json

response = requests.post("http://discernerapi.com/token", {"username":your_username, "password":your_password})
token = json.loads(response.text)["token"]
auth_string = "token " + token

users = requests.get("http://discernerapi.com/activities", headers = {"authorization": token_string})
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "user_id":1,
    "product_id":1,
    "score":4.5
  },
  {
    "id": 2,
    "user_id":2,
    "product_id":2,
    "score":2.0
  }
]
```

This endpoint retrieves all actvities.

### HTTP Request

`GET http://discernerapi.com/activities`

## Post a New Activity

```python
import requests
import json

response = requests.post("http://discernerapi.com/token", {"username":your_username, "password":your_password})
token = json.loads(response.text)["token"]
auth_string = "token " + token

requests.post("http://discernerapi.com/users/:user_id/products/:product_id/activities", headers = {"authorization": token_string})
```

> The above command returns JSON structured like this:

```json
  {
    "id": 1,
    "user_id":1,
    "product_id":1,
    "score":4.5
  }
```

This endpoint creates a new activity between a user and product.

### HTTP Request

`POST http://discernerapi.com/users/:user_id/products/:product_id/activities`

# Recommendation

## Get Recommendations for a User

```python
import requests
import json

response = requests.post("http://discernerapi.com/token", {"username":your_username, "password":your_password})
token = json.loads(response.text)["token"]
auth_string = "token " + token

users = requests.get("http://discernerapi.com/users/:user_id/recs", headers = {"authorization": token_string})
```

> The above command returns JSON structured like this:

```json
```

This endpoint retrieves all actvities.

### HTTP Request

`GET http://discernerapi.com/users/:user_id/recs`


