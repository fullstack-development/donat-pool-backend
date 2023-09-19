from better_profanity import profanity

def is_text_acceptable(additional_words, moderating_text):
    profanity.load_censor_words(additional_words)
    return not profanity.contains_profanity(moderating_text)
