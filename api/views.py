from django.shortcuts import render
#from .. import recommend.pkl
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import movieInputModel
from .serializers import movieInputSerializer
import numpy as np
import sklearn
import pickle
#from sklearn.externals import joblib
import joblib
import pandas as pd
from fuzzywuzzy import fuzz
from sklearn.neighbors import NearestNeighbors

# Create your views here.

class movieInputViewset(viewsets.ModelViewSet):
    queryset = movieInputModel.objects.all()
    serializer_class = movieInputSerializer



#api decorator handles the POST request
@api_view(['POST'])
def recommendModel(request):
    try:
        model = model_knn = NearestNeighbors(
            metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)

        #i have pickled
        sparced_data = joblib.load('./sparced data matrix.pkl')
        model_knn = model_knn.fit(sparced_data)
        movie_to_index = joblib.load('./movie_to_index.pkl')
        collectData = request.data
        
        #the request from the web came in as a string like {collectData : ""} so i got the keys
        key_value = collectData.keys()

        #change to numpy array
        unit = np.array(key_value)

        #fuction that checks if there is a match in the ML database
        def fuzzy_matching(mapper, fav_movie, verbose=True):
            """
            return the closest match via fuzzy ratio. If no match found, return None

            Parameters
            ----------    
            mapper: dict, map movie title name to index of the movie in data

            fav_movie: str, name of user input movie

            verbose: bool, print log if True

            Return
            ------
            index of the closest match
            """
            match_tuple = []
            # get match
            for title, idx in mapper.items():
                ratio = fuzz.ratio(title.lower(), fav_movie.lower())
                if ratio > 47:
                    match_tuple.append((title, idx, ratio))
            # sort
            match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
            if not match_tuple:
                return [False, False]
            if verbose:
                return [match_tuple[0][1], match_tuple[0][0]]

        #this function will take in the Ml algorithm  parameter and return a JsonResponce
        def make_recommendation(data, mapper, fav_movie, n_recommendations, model_knn=model):
            """
            return top n similar movie recommendations based on user's input movie
            Parameters
            ----------
            model_knn: sklearn model, knn model

            data: movie-user matrix

            mapper: dict, map movie title name to index of the movie in data

            fav_movie: str, name of user input movie

            n_recommendations: int, top n recommendations

            Return
            ------
            list of top n similar movie recommendations
            """
            # fit
            model_knn.fit(data)
            # get input movie index
            #print('You have input movie:', fav_movie)
            match_result = fuzzy_matching(mapper, fav_movie, verbose=True)
            match_result_index = match_result[0]
            # inference
            
            distances, indices = model_knn.kneighbors(
                data[match_result_index], n_neighbors=n_recommendations+1)
            # get list of raw idx of recommendations
            raw_recommends = \
                sorted(list(zip(indices.squeeze().tolist(),
                                distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
            # get reverse mapper
            reverse_mapper = {v: k for k, v in mapper.items()}
            # print recommendations
            #print('Recommendations for {}:'.format(fav_movie))

            #all responce as dictionary to be changed into a json data type later
            response = {
                        'msg_if_found': match_result_index,
                        'loading_msg_1': 'Database match -> {}'.format(match_result[1]),
                        'loading_msg_2': 'Recommendation system start to make inference'
                        }
            for i, (idx, dist) in enumerate(raw_recommends):
                #reverse_mapper[idx] returns the value of each key

                response[i+1] = reverse_mapper[idx]

            #checking if there is a match in the database

            if type(match_result_index) is int:
                return response
            else:
                return {'404': ''}
        
        make_recommendation = make_recommendation(
            model_knn=model,
            data=sparced_data,
            fav_movie=''.join(str(unit)),
            mapper=movie_to_index,
            n_recommendations=10)

        return JsonResponse(make_recommendation)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

