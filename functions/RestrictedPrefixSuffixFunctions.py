def get_restricted_prefix_suffix():
    return ["prefix", "suffix"]


def check_title_in_restricted_prefix_suffix(title):
    restricted_prefix_suffix = get_restricted_prefix_suffix()
    invalid_words = []
    
    for word in restricted_prefix_suffix:
        if title.startswith(word) or title.endswith(word):
            invalid_words.append(word)
            
    return {
        "isValid": len(invalid_words) == 0,
        "invalid_words": invalid_words,
    }
