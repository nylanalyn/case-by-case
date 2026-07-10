from .authored import CASE_DEFINITIONS


CASE_DEFINITION_BY_SLUG = {
    definition["slug"]: definition
    for definition in CASE_DEFINITIONS
}


def case_definition_for_slug(slug):
    return CASE_DEFINITION_BY_SLUG.get(slug, {})
