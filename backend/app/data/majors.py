import re


MAJOR_CATEGORY_LABELS = {
    "agriculture": "Agriculture",
    "resources": "Natural Resources",
    "architecture": "Architecture",
    "ethnic_cultural_gender": "Ethnic, Cultural, and Gender Studies",
    "communication": "Communications",
    "communications_technology": "Communications Technology",
    "computer": "Computer Science",
    "personal_culinary": "Culinary and Personal Services",
    "education": "Education",
    "engineering": "Engineering",
    "engineering_technology": "Engineering Technology",
    "language": "Languages",
    "family_consumer_science": "Family and Consumer Sciences",
    "legal": "Legal Studies",
    "english": "English",
    "humanities": "Humanities",
    "library": "Library Science",
    "biological": "Biology",
    "mathematics": "Mathematics",
    "military": "Military Science",
    "multidiscipline": "Interdisciplinary Studies",
    "parks_recreation_fitness": "Parks, Recreation, and Fitness",
    "philosophy_religious": "Philosophy and Religious Studies",
    "theology_religious_vocation": "Theology",
    "physical_science": "Physical Sciences",
    "science_technology": "Science and Technology",
    "psychology": "Psychology",
    "security_law_enforcement": "Criminal Justice",
    "public_administration_social_service": "Public Administration and Social Service",
    "social_science": "Social Sciences",
    "construction": "Construction Trades",
    "mechanic_repair_technology": "Mechanic and Repair Technologies",
    "precision_production": "Precision Production",
    "transportation": "Transportation",
    "visual_performing": "Visual and Performing Arts",
    "health": "Health Professions",
    "business_marketing": "Business",
    "history": "History",
}

MAJOR_ALIASES = {
    "Agriculture": ["ag science", "agricultural science", "farm science"],
    "Natural Resources": ["environmental science", "environmental studies", "ecology"],
    "Communications": ["communication", "media studies", "journalism", "public relations"],
    "Communications Technology": ["broadcasting", "media production"],
    "Computer Science": ["computer engineering", "comp sci", "cs", "software", "computing", "it", "information technology"],
    "Culinary and Personal Services": ["culinary arts", "hospitality services", "cosmetology"],
    "Education": ["teaching", "teacher education", "elementary education"],
    "Engineering": ["mechanical engineering", "electrical engineering", "civil engineering", "chemical engineering"],
    "Engineering Technology": ["engineering tech"],
    "Languages": ["foreign languages", "linguistics", "spanish", "french"],
    "Legal Studies": ["pre-law", "law", "paralegal"],
    "Biology": ["biological sciences", "biomedical sciences", "life sciences"],
    "Mathematics": ["applied math", "statistics"],
    "Interdisciplinary Studies": ["liberal studies", "general studies"],
    "Parks, Recreation, and Fitness": ["exercise science", "kinesiology", "sports management"],
    "Physical Sciences": ["chemistry", "physics", "geology", "earth science"],
    "Psychology": ["psych"],
    "Criminal Justice": ["criminology", "law enforcement", "forensics"],
    "Public Administration and Social Service": ["social work", "public policy", "human services"],
    "Social Sciences": ["sociology", "political science", "economics", "anthropology"],
    "Visual and Performing Arts": ["art", "fine arts", "graphic design", "music", "theater", "dance"],
    "Health Professions": ["nursing", "pre-med", "public health", "healthcare", "health sciences"],
    "Business": ["business administration", "marketing", "finance", "accounting", "management"],
}


def major_field_names():
    fields = []
    for slug in MAJOR_CATEGORY_LABELS:
        fields.append(f"latest.academics.program.degree_or_certificate.{slug}")
        fields.append(f"latest.academics.program_percentage.{slug}")
    return fields


def extract_majors(raw):
    ranked = []
    for slug, label in MAJOR_CATEGORY_LABELS.items():
        offered = raw.get(f"latest.academics.program.degree_or_certificate.{slug}")
        share = raw.get(f"latest.academics.program_percentage.{slug}")
        if offered or (share is not None and share > 0):
            ranked.append((label, share or 0))

    ranked.sort(key=lambda item: (-item[1], item[0]))
    return [label for label, _ in ranked]


def all_major_labels():
    return sorted(MAJOR_CATEGORY_LABELS.values())


def normalize_major_text(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def school_offers_major(school, query):
    query_norm = normalize_major_text(query)
    if not query_norm:
        return True

    for major in school.get("majors", []):
        terms = [major, *MAJOR_ALIASES.get(major, [])]
        for term in terms:
            term_norm = normalize_major_text(term)
            if query_norm in term_norm or term_norm in query_norm:
                return True

    return False
