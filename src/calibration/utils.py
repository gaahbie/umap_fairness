

def calculate_user_distribution_popularity(items_interacted, movies_data, column='popularity'):
    H = 0
    M = 0
    T = 0

    dist = {
        'H': 0,
        'M': 0,
        'T': 0
    }
    sum_ = 0

    aux_movies = movies_data[movies_data['imdb'].isin([i[0] for i in items_interacted])]

    for (item_id, rating) in items_interacted:
        selected_item = aux_movies[aux_movies['imdb'] == item_id]
        if len(selected_item) > 0:
            popularity_bin = selected_item['popularity_int'].values[0]
            dist[popularity_bin] = dist[popularity_bin] + rating
            sum_ += rating
    
    if sum_ != 0:
        dist = {k:v/sum_ for k,v in dist.items()}

    return dist


def calculate_user_distribution_budget(items_interacted, movies_data, column='popularity'):
    H = 0
    M = 0
    T = 0

    dist = {
        'H': 0,
        'M': 0,
        'T': 0
    }
    sum_ = 0

    aux_movies = movies_data[movies_data['imdb'].isin([i[0] for i in items_interacted])]

    for (item_id, rating) in items_interacted:
        selected_item = aux_movies[aux_movies['imdb'] == item_id]
        if len(selected_item) > 0:
            popularity_bin = selected_item['popularity_budget_inf'].values[0]
            dist[popularity_bin] = dist[popularity_bin] + rating
            sum_ += rating
    if sum_ != 0:
        dist = {k:v/sum_ for k,v in dist.items()}

    return dist