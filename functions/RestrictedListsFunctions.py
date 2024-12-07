def get_restricted_lists(type):
    words = [
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
    prefix_suffix = ["prefix", "suffix"]
    return words if type == "words" else prefix_suffix

def check_title_in_restricted_lists(title, type):
    restricted_words = get_restricted_lists(type)
    invalid_words = []
    title_words = title.split()

    for word in restricted_words:
        if word in title:
            invalid_words.append(word)
        for title_word in title_words:
            if word == title_word and word not in invalid_words:
                invalid_words.append(word)

    return {"isValid": len(invalid_words) == 0, "invalid_words": invalid_words}
