import os
import re

from elasticsearch_dsl import analyzer, token_filter, tokenizer

SYNONYMS_PATH = os.getenv(
    "SYNONYMS_PATH",
    "/usr/share/elasticsearch/config/synonyms"
)


def strip_html(markup):
    """Make sure markup stripping doesn't mash content elements together."""
    clean = re.compile("<.*?>")
    return re.sub(clean, " ", markup).strip()


label_autocomplete = analyzer(
    'label_autocomplete',
    tokenizer=tokenizer(
        'trigram',
        'edge_ngram',
        min_gram=2,
        max_gram=25,
        token_chars=["letter", "digit"]
    ),
    filter=['lowercase', token_filter('ascii_fold', 'asciifolding')]
)

synonynm_filter = token_filter(
    'synonym_filter_en',
    'synonym',
    synonyms_path=(
        f'{SYNONYMS_PATH}/synonyms_en.txt'
    ),
)

synonym_analyzer = analyzer(
    'synonym_analyzer_en',
    type='custom',
    tokenizer='standard',
    filter=[
        synonynm_filter,
        'lowercase'
    ])
