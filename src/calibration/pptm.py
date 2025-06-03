import copy
from scipy.stats import wasserstein_distance

import numpy as np

def run_calibration(recomendations, user_profile_bins, movies_popularities, itemscores, movies_data, movies_budgets, column='popularity', c=0.001, k=10):
    aux_3 = copy.deepcopy(recomendations)

    if column == 'popularity':
        S = seedset_pop(
            recomendations,
            movies_popularities,
            user_profile_bins,
            k=10
        )
    else:
        S = seedset_pop(
            recomendations,
            movies_budgets,
            user_profile_bins,
            k=10
        )    


    H = []
    M = []
    T = []

    max_len = (k-len(S))

    if column == 'popularity':
        for i in aux_3:
            if int(i[0]) not in S:
                if movies_popularities[i[0]] == 'H' and len(H) < max_len:
                    H.append(i)
                elif movies_popularities[i[0]] == 'M' and len(M) < max_len:
                    M.append(i)
                elif movies_popularities[i[0]] == 'T' and len(T) < max_len:
                    T.append(i)

            if len(H) == max_len and len(M) == max_len and len(T) == max_len:
                break
    else:
        for i in aux_3:
            if int(i[0]) not in S:
                if movies_budgets[i[0]] == 'H' and len(H) < max_len:
                    H.append(i)
                elif movies_budgets[i[0]] == 'M' and len(M) < max_len:
                    M.append(i)
                elif movies_budgets[i[0]] == 'T' and len(T) < max_len:
                    T.append(i)

            if len(H) == max_len and len(M) == max_len and len(T) == max_len:
                break


    B = H + M + T
    R = greedy_selection(
        S,
        itemscores,
        B,
        user_profile_bins,
        movies_data,
        k=10,
        c=c,
        column=column
    )

    return R


def seedset_pop(list_items, movies_popularities, user_ppt, k):
    S = []
    S_ppt =  {
        'H': 0,
        'M': 0,
        'T': 0
    }
    K = list_items[:k]
    
    for ij, rating in K:
        b = movies_popularities[ij]
        
        if user_ppt.get(b, 0) > S_ppt[b] + 1/k:
            S.append(ij)
            S_ppt[b] = S_ppt[b] + 1/k
    return S

def calculo(P, Q, P_items_score, c):
    popularity_bins = {
        'H': 0,
        'M': 0,
        'T': 0
    }
    
    P_ = [P.get(bin_, 0) for bin_ in popularity_bins.keys()]
    Q_ = [Q.get(bin_, 0) for bin_ in popularity_bins.keys()]


    EMD = wasserstein_distance(P_, Q_)
    return P_items_score - c*EMD


def calculate_PPT(temp_list, movies_data, column):
    dist = {
        'H': 0,
        'M': 0,
        'T': 0
    }
    sum_ = 0

    aux_movies = movies_data[movies_data['movieId'].isin([i for i in temp_list])]

    for rating, item_id in enumerate(temp_list):
        selected_item = aux_movies[aux_movies['movieId'] == item_id]
        if column == 'popularity':
            popularity_bin = selected_item['popularity_int'].values[0]
        else:
            popularity_bin = selected_item['popularity_budget_inf'].values[0]
        dist[popularity_bin] = dist[popularity_bin] + rating
        sum_ += rating
    
    dist = {k:v/sum_ for k,v in dist.items()}

    return dist


def greedy_selection(S, itemscores, B, user_profile_bins, movies_data, column, k=10, c=0.001):
    R = copy.deepcopy(S)
    R_minus_S = []
    len_S = len(S)

    user_profile_score = 0
    for i in R:
        if isinstance(i, tuple):
            user_profile_score += itemscores[i[0]]
        else:
            user_profile_score += itemscores[i]

    
    for i in range(k-len_S):
        maxmmr = -np.inf
        maxitem = None
        results_maximization = []
        for item, rating in B:
            if item in R:
                continue
            
            temp_list = R + [item]
            temp_score = user_profile_score + itemscores[item]

            objective = calculo(
                user_profile_bins,
                calculate_PPT(temp_list, movies_data, column=column),
                temp_score, c=c
            )
            results_maximization.append((objective, item))

        
        maxitem = sorted(results_maximization, key=lambda x: x[0], reverse=True)[0][1]

        if maxitem is not None: 
            R.append(maxitem)
            user_profile_score += itemscores[item]
            R_minus_S.append(maxitem)
            B = [i for i in B if i[0] != maxitem]

    R_changed = True
    while R_changed is True:
        maxmmr = -np.inf
        maxitem = None
        temp_score = user_profile_score

        results_maximization = []
        
        for (item, rating) in B:
            for item2 in R_minus_S:
                
                temp_list1 = R + [item]
                if item2 in temp_list1:
                    temp_list1.remove(item2)
                    temp_score = user_profile_score + itemscores[item] - itemscores[item2]
                else:
                    temp_score = user_profile_score + itemscores[item]
                
                objective = calculo(
                    user_profile_bins,
                    calculate_PPT(temp_list1, movies_data, column=column),
                    temp_score, c=c
                )

                results_maximization.append((objective, (item, item2)))

        if len(results_maximization) > 0:
            maxitem = sorted(results_maximization, key=lambda x: x[0], reverse=True)[0][1]
            temp_list1 = R + [maxitem[0]]
            if maxitem[1] in temp_list1: temp_list1.remove(maxitem[1])

            comparison1 = calculo(
                user_profile_bins,
                calculate_PPT(temp_list1, movies_data, column=column),
                temp_score, c=c
            )
            
            comparison2 = calculo(
                user_profile_bins,
                calculate_PPT(R, movies_data, column=column),
                temp_score, c=c
            )

            if comparison1 > comparison2:
                
                
                R.append(maxitem[0])

                if maxitem[1] in R: 
                    R.remove(maxitem[1])
                    user_profile_score -= itemscores[maxitem[1]]

                user_profile_score += itemscores[maxitem[0]] 
                if maxitem[0] in B: 
                    B = [i for i in B if i[0] != maxitem[0]]
                
                B.append((maxitem[1], itemscores[maxitem[1]]))
                
                R_changed = True
            else:
                R_changed = False
        else:
            temp_list1 = R
            R_changed = False
            
    return R