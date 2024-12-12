from fastapi import APIRouter, Query
import pandas as pd
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from metaphone import doublemetaphone
from pymilvus import AnnSearchRequest
from pymilvus import WeightedRanker
from fuzzywuzzy import fuzz
from phonetics import metaphone

import json
from config.database import get_collection
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
# nltk.download('stopwords')
# nltk.download('punkt_tab')

similiar_router = APIRouter(prefix="/searchresults", tags=["trademark"])
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_metaphone(name):
    # return doublemetaphone(name)[0]
    return metaphone(name)


def wagner_fischer(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    if len_s1 > len_s2:
        s1, s2 = s2, s1
        len_s1, len_s2 = len_s2, len_s1

    current_row = range(len_s1 + 1)
    for i in range(1, len_s2 + 1):
        previous_row, current_row = current_row, [i] + [0] * len_s1
        for j in range(1, len_s1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
            if s1[j-1] != s2[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[len_s1]

def spell_check(word, dictionary):
    suggestions = []

    for correct_word in dictionary:
        distance = wagner_fischer(word, correct_word)
        suggestions.append(distance)

    # suggestions.sort(key=lambda x: x[1])
    return suggestions


async def perform_hybrid_search(collection,reqs,output_fields,name=0.8,meta=0.2):
    processed_results = []
    rerank = WeightedRanker(name, meta)
    results = collection.hybrid_search(
    reqs,
    rerank,
    limit=200,
    output_fields=output_fields
    )
    for result in results[0]:
        processed_results.append({
            "distance": result.distance,
            "Metaphone_Name_After_Sort": result.entity.get("Metaphone_Name_After_Sort"),
            "Title_Name": result.entity.get("Title_Name"),
            "Title_Name_After_Sort":result.entity.get("Title_Name_After_Sort")
        })
    return processed_results

async def hybrid_vector_search_for_count(name,title,meta):
    try:
        collection=get_collection("Alphabetic_sort_3")
        nameVector=[model.encode(name).tolist()]
        metaphoneVector=[model.encode(get_metaphone(name)).tolist()]
        search_param_1 = {
        "data": nameVector, 
        "anns_field": "vector_of_name", 
        "param": {
            "metric_type": "COSINE", 
            "params": {"nprobe": 384}
        },
        "limit": 200,
        }
        search_param_2 = {
        "data": metaphoneVector, 
        "anns_field": "vector_of_metaphone", 
        "param": {
            "metric_type": "COSINE",
            "params": {"nprobe": 384}
        },
        "limit": 200,
        }
        # search_param_3 = {
        # "data": metaphoneVector, 
        # "anns_field": "vector_of_metaphone", 
        # "param": {
        #     "metric_type": "COSINE",
        #     "params": {"nprobe": 384}
        # },
        # "limit": 200,
        # }
        reqs = [AnnSearchRequest(**search_param_1), AnnSearchRequest(**search_param_2)]
        output_fields=["Metaphone_Name_After_Sort","Title_Name",'Title_Name_After_Sort']
        final_result_df=await perform_hybrid_search(collection,reqs,output_fields,title,meta,)
        df=pd.DataFrame(final_result_df)[:200]
        # df=df.sort_values(by=['distance'],ascending=False)[:60]
        # print(df)
        return df
        # return df.loc[df['Count']>100]
    except Exception as e:
        return {"error": str(e.with_traceback())}, 500

def calculate_dynamic_impacts(fuzzy_scores, title):
    """
    Calculate dynamic impact weights based on the distribution of scores
    """
    if not fuzzy_scores:
        return 0.0

    total_count = len(fuzzy_scores)

    # Categorize scores into 5 levels
    highest_scores = [score for score in fuzzy_scores if 96 <= score <= 100]
    higher_scores = [score for score in fuzzy_scores if 91 <= score <= 95]
    high_scores = [score for score in fuzzy_scores if 80 <= score <= 90]
    medium_scores = [score for score in fuzzy_scores if 60 <= score <= 79]
    low_scores = [score for score in fuzzy_scores if 40 <= score <= 59]

    n_highest = len(highest_scores)
    n_higher = len(higher_scores)
    n_high = len(high_scores)
    n_medium = len(medium_scores)
    n_low = len(low_scores)

    # Calculate average scores for each category if they exist
    highest_avg = sum(highest_scores) / n_highest if n_highest > 0 else 0
    higher_avg = sum(higher_scores) / n_higher if n_higher > 0 else 0
    high_avg = sum(high_scores) / n_high if n_high > 0 else 0
    medium_avg = sum(medium_scores) / n_medium if n_medium > 0 else 0
    low_avg = sum(low_scores) / n_low if n_low > 0 else 0

    # Calculate dynamic impacts based on category averages
    # Higher average score = higher impact
    highest_impact = (highest_avg / 100) * 10 if n_highest > 0 else 0
    higher_impact = (higher_avg / 100) * 5 if n_higher > 0 else 0
    high_impact = (high_avg / 100) * 3 if n_high > 0 else 0
    medium_impact = (medium_avg / 100) * 0.5 if n_medium > 0 else 0  # Scale down medium scores
    low_impact = (low_avg / 100) * 0.2 if n_low > 0 else 0  # Scale down low scores

    # Calculate weighted probability reduction
    initial_prob = 1.0
    remaining_prob = initial_prob

    # Apply impacts proportionally to the number of scores in each category
    if total_count > 0:
        if n_highest > 0:
            remaining_prob -= (n_highest / total_count) * highest_impact
        if n_higher > 0:
            remaining_prob -= (n_higher / total_count) * higher_impact
        if n_high > 0:
            remaining_prob -= (n_high / total_count) * high_impact
        if n_medium > 0:
            remaining_prob -= (n_medium / total_count) * medium_impact
        if n_low > 0:
            remaining_prob -= (n_low / total_count) * low_impact

    # Ensure probability stays within valid range
    remaining_prob = max(0, min(1, remaining_prob))

    return remaining_prob

    # return {
    #     "title": title,
    #     "remaining_probability": f"{round(remaining_prob * 100, 2)}% for acceptance",
    #     "statistics": {
    #         "total_count": total_count,
    #         "highest_scores": {
    #             "count": n_highest,
    #             "average": round(highest_avg, 2) if n_highest > 0 else 0,
    #             "impact": round(highest_impact, 3),
    #         },
    #         "higher_scores": {
    #             "count": n_higher,
    #             "average": round(higher_avg, 2) if n_higher > 0 else 0,
    #             "impact": round(higher_impact, 3),
    #         },
    #         "high_scores": {
    #             "count": n_high,
    #             "average": round(high_avg, 2) if n_high > 0 else 0,
    #             "impact": round(high_impact, 3),
    #         },
    #         "medium_scores": {
    #             "count": n_medium,
    #             "average": round(medium_avg, 2) if n_medium > 0 else 0,
    #             "impact": round(medium_impact, 3),
    #         },
    #         "low_scores": {
    #             "count": n_low,
    #             "average": round(low_avg, 2) if n_low > 0 else 0,
    #             "impact": round(low_impact, 3),
    #         },
    #     },
    # }

@similiar_router.get("/sametitle")
async def same_title(title: str = Query(..., description="The name to search for")):
    try:
        # LOKTANTRATIMES | LOKTANTRA TIMES | TIMES LOKTANTRA | TIMES OF LOKTANTRA | MAHARASHTRATIMES CITY
        # MAHARASHTRATIMESCITY -> Not working
        name=title
        words = word_tokenize(name)
        filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]
        sorted_sentence = sorted(filtered_words, key=str.lower)
        title_after_sort = ' '.join(sorted_sentence).upper()
        # for i in range(2,11):
        print(title_after_sort)
        print(get_metaphone(title_after_sort.upper()))
        result= await hybrid_vector_search_for_count(title_after_sort,1.0,0.3)
        meta_dist=spell_check(get_metaphone(title_after_sort.upper()),result['Metaphone_Name_After_Sort'])
        result['fuzzy'] = result['Title_Name_After_Sort'].apply(lambda x: fuzz.ratio(title_after_sort.upper(), x))
        result['Meta_Levensthein'] = meta_dist
        lmax = result["Meta_Levensthein"].max()
        # result['Meta_Levensthein'] = lmax - result['Meta_Levensthein']
        result = result.loc[
            (result['distance'] >= ((1.0 + float(0.3)) - 0.150)) &
            (result['fuzzy'] > 90)
        ]
        resultFDL = result.sort_values(
            by=['fuzzy','distance','Meta_Levensthein'], 
            ascending=[False,False,False])
        resultFLD = result.sort_values(
            by=['fuzzy','Meta_Levensthein','distance'], 
            ascending=[False,False,False])
        average_fuzzy=0
        if resultFDL.empty or resultFDL['fuzzy'].dropna().empty:
            average_fuzzy = 0  
        else:
            average_fuzzy = resultFDL['fuzzy'].mean()
        return {
                "status":"success",
                "message": f"Titles as same as {name}",
                "FDL":json.loads(resultFDL.to_json()),
                # "FLD":json.loads(resultFLD.to_json()),
                "isValid":True,
                "rejectance probability" : average_fuzzy,
                "acceptance probability" : 100-average_fuzzy,
            }

    except Exception as e:
        return {"error": str(e),"isValid":False}
    
@similiar_router.get("/similartitles")
async def similar_title(title: str = Query(..., description="The name to search for")):
    try:
        name=title
        words = word_tokenize(name)
        filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]
        sorted_sentence = sorted(filtered_words, key=str.lower)
        title_after_sort = ' '.join(sorted_sentence).upper()
        
        print(title_after_sort)
        print(get_metaphone(title_after_sort.upper()))
        result= await hybrid_vector_search_for_count(title_after_sort,1.0,0.0)
        meta_dist=spell_check(get_metaphone(title_after_sort.upper()),result['Metaphone_Name_After_Sort'])
        result['fuzzy'] = result['Title_Name_After_Sort'].apply(lambda x: fuzz.ratio(title_after_sort.upper(), x))
        result['Meta_Levensthein'] = meta_dist
        lmax = result["Meta_Levensthein"].max()
        result['Meta_Levensthein'] = lmax - result['Meta_Levensthein']
        result = result.loc[
            (result['distance'] >= (0.6)) &
            (result['fuzzy'] >= 40)
        ]
        resultDFL = result.sort_values(
            by=['distance','fuzzy','Meta_Levensthein'], 
            ascending=[False,False,False])
        resultFDL = result.sort_values(
            by=['fuzzy','distance','Meta_Levensthein'], 
            ascending=[False,False,False])
        column_order = ['fuzzy', 'distance', 'Meta_Levensthein', 'Metaphone_Name_After_Sort', 'Title_Name', 'Title_Name_After_Sort']
        resultFDL = resultFDL[column_order]
        resultFDL = resultFDL.reset_index(drop=True)
        print(resultFDL)
        print("--")
        print(resultFDL["fuzzy"],type(resultFDL["fuzzy"]))

        fuzzy_values = resultFDL["fuzzy"].tolist()
        print(type(fuzzy_values))
        probability=calculate_dynamic_impacts(fuzzy_values,name)
        return {
                "status":"success",
                "message": f"Titles as same as {name}",
                # "DFL":json.loads(resultDFL.to_json()),
                "FDL":json.loads(resultFDL.to_json()),
                "probability":probability,
                "isValid":True,
                "rejectance probability" : probability,
                "acceptance probability" : 100-probability,
            }
    except Exception as e:
        return {"status":"failed","error": str(e),"isValid":False}    
    
@similiar_router.get("/similarsound")
async def similar_sound(title: str = Query(..., description="The name to search for")):
    try:
        name=title
        words = word_tokenize(name)
        filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]
        sorted_sentence = sorted(filtered_words, key=str.lower)
        title_after_sort = ' '.join(sorted_sentence).upper()
        
        print(title_after_sort)
        print(get_metaphone(title_after_sort.upper()))
        result= await hybrid_vector_search_for_count(title_after_sort,0.3,1.0)
        meta_dist=spell_check(get_metaphone(title_after_sort.upper()),result['Metaphone_Name_After_Sort'])
        result['fuzzy'] = result['Title_Name_After_Sort'].apply(lambda x: fuzz.ratio(title_after_sort.upper(), x))
        result['Meta_Levensthein'] = meta_dist
        lmax = result["Meta_Levensthein"].max()
        result['Meta_Levensthein'] = lmax - result['Meta_Levensthein']
        result = result.loc[
            (result['distance'] >= (0.65)) &
            (result['fuzzy'] >= 50)
        ]
        print(result)
        resultDFL = result.sort_values(
            by=['distance','fuzzy','Meta_Levensthein'], 
            ascending=[False,False,False])
        resultFLD = result.sort_values(
            by=['fuzzy','distance','Meta_Levensthein'], 
            ascending=[False,False,False])
        print(resultDFL)
        # average_distance=0
        # if resultDFL.empty or resultDFL['distance'].dropna().empty:
        #     average_distance = 0  
        # else:
        #     average_distance = resultDFL['distance'].mean()
        distance_values= resultDFL["distance"].tolist()
        probability=calculate_dynamic_impacts(distance_values,name)
        # resultFDL = resultFDL.reset_index(drop=True)
        return {
                "status":"success",
                "message": f"Titles as same as {name}",
                "isValid":True,
                "DFL":json.loads(resultDFL.to_json()),
                # "FLD":json.loads(resultFLD.to_json()),
                "rejectance probability" : probability,
                "acceptance probability" : 100-probability,
            }
    except Exception as e:
            return {"status":"failed","error": str(e),"isValid":False}
