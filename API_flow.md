# API Order 
In this document we have defined the api order for the trade mark sarthi project.Its listed the api in the order of execution and grouped by the functionality that will title will be rejected or accepted or we are finding the similarity with the existing titles.

## Validate Title : 
where we validate the title based on the following criteria and if failed then we return the error message that why it is failed and also we return the list of disallowed words, prefix and suffix. user can not move forward until the title is valid and pass all the api listed below:

1. /api/v1/validate_title/disallowed_words
2. /api/v1/validate_title/disallowed_prefix_suffix
3. /api/v1/validate_title/combination_of_existing_titles

