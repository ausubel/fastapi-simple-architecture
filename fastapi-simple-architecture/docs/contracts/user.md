# User Router Contracts

## List Users

### GET /users

#### Response
```json
    [
        {
            "firstName": "Cristiano",
            "lastName": "Ronaldo",
            "email": "cristiano.ronaldo@example.com",
            "dateOfBirth": "1985-02-05T05:00:00.000Z",
        },
        {
            "firstName": "Lionel",
            "lastName": "Messi",
            "email": "lionel.messi@example.com",
            "dateOfBirth": "1987-06-24T05:00:00.000Z",
        },
    ]	
```

## Find User By Id

### GET /users/:id

#### Response
```json
    {
        "id": 1,
        "firstName": "Cristiano",
        "lastName": "Ronaldo",
        "email": "cristiano.ronaldo@example.com",
        "dateOfBirth": "1985-02-05T05:00:00.000Z",
    }
```

Note: ":id" is the path parameter for the user id.

## Update User

### PUT /users/:id

#### Request

```json
    {
        "firstName": "Cristiano",
        "lastName": "Ronaldo",
        "email": "cristiano.ronaldo@example.com",
        "dateOfBirth": "1985-02-05T05:00:00.000Z",
    }
```

#### Response
```json
    {
        "message": "User updated successfully"
    }
```

### Delete User

### DELETE /users/:id

#### Response
```json
    {
        "message": "User deleted successfully"
    }
```