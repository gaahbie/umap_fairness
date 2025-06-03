
## How to run

The easy way to use the API is probably with docker.

### Run with Docker

### Run without Docker


## How to use the API

### A/B Testing Endpoint

The first endpoint generated the unique user_id and specify which experiments this users bellongs to. This endpoint returns a json with the token (user id) and the experiment id (0-5)

The experiment id returned associate the users with one of the control/treatment used. So 0 means the control, 1 means the treatment 1 and so on...

```
GET /ab_testing/

Returns:
{
  "token": "a0820d66-4d9c-4923-8337-c27e7fa82e83",
  "experiment": 0
}

```

The second endpoint is used to get the information about a specific user id. It will return the date the user started the experiment and the experiment id.

```
GET /ab_testing/{user_id}

Returns:
Response body
Download

{
  "experiment_type": 0,
  "started_timestamp": 1662250307,
  "experiment_id": "a0820d66-4d9c-4923-8337-c27e7fa82e83"
}
```

### Movies Endpoint

The first endpoint is to search a movie by imdb ID. 

```
GET /movies/:imdb_id:

Returns:
{
  "imdb_id": "...",
  "title": "...",
  "description": "...",
  "poster": "...",
  "trailer": "https://www.youtube.com/watch?v=...",
  "rating": 0
}
```

The second endpoint are used to search a movie by a title substring. It also has the pagination function. The pagination functions filter all movies with the substring passed as title and returned the subset started at index ``skip`` to the index ``skip + limit``

```
GET /movies?search=name&skip=0&limit=10:

Returns:
[
    {
        "imdb_id": "...",
        "title": "...",
        "description": "...",
        "poster": "...",
        "trailer": "https://www.youtube.com/watch?v=...",
        "rating": 0
    },
    {
        "imdb_id": "...",
        "title": "...",
        "description": "...",
        "poster": "...",
        "trailer": "https://www.youtube.com/watch?v=...",
        "rating": 0
    },
    ....
]

```


### Profile Endpoint

The first endpoint add item interactions to users profile. You should send an list of dictionary of the items the user interacted and the rating given. Also you must pass the "user_id" which is the identification generate at the *profile endpoint*

```
POST /profile/

{
  "interactions": [
    {
      "item_id": 0,
      "rating": 0
    }
  ],
  "user_id": "string"
}
```

The seconds endpoints lists the items an user interacted. It returns a list of items.

*The item_id reffers to the imdb id*

```
GET /profile/{user_id}

[
  {
    "item_id": 1,
    "rating": 5,
    "added_timestamp": 1662250391
  },
  ...
]
```


### Recommendation endpoint


This endpoint generates the user recommendation. It returns an json with the field "data" which contains 10 movies recommended to that users

*The generations depends on the user experiment id. So it returns the recommendation calibrated or not.*

```
GET /recommendation/{user_id}

{
  "message": "recommendation generated",
  "data": [
    {
      "imdb_id": "...",
      "title": "...",
      "description": "...",
      "poster": "...",
      "trailer": ....",
      "rating": 0
    },
    ...
  ]
}

```