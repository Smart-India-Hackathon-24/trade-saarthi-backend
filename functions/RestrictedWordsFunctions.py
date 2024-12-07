def get_restricted_words():
    return [
        "police",
        "corruption",
        "terrorism",
        "crime",
        "terrorist",
        "bureau",
        "investigation",
        "vigilance",
        "commission",
        "defense",
        "cid",
        "cbi",
        "establishment",
    ]


def check_title_in_restricted_words(title):
    restricted_words = get_restricted_words()
    invalid_words = []
    title_words = title.split()
    
    for word in restricted_words:
        if word in title:
            invalid_words.append(word)
        for title_word in title_words:
            if word == title_word and word not in invalid_words:
                invalid_words.append(word)
                
    return {
        "isValid": len(invalid_words) == 0,
        "invalid_words": invalid_words
    }
