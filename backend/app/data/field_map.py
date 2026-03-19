# Maps key names to College Scorecard API field paths
FIELD_MAP = {
    "id":             "id",
    "name":           "school.name",
    "city":           "school.city",
    "state":          "school.state",
    "url":            "school.school_url",
    "ownership":      "school.ownership",
    "locale":         "school.locale",
    "predominant_degree": "school.degrees_awarded.predominant",
    "size":           "latest.student.size",
    "tuition_in":     "latest.cost.tuition.in_state",
    "tuition_out":    "latest.cost.tuition.out_of_state",
    "avg_net_price":  "latest.cost.avg_net_price.overall",
    "admission_rate": "latest.admissions.admission_rate.overall",
    "lat":            "location.lat",
    "lon":            "location.lon",
}

API_FIELDS = ",".join(FIELD_MAP.values())
