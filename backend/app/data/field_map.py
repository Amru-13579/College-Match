# Maps key names to College Scorecard API field paths
FIELD_MAP = {
    "id":             "id",
    "name":           "school.name",
    "city":           "school.city",
    "state":          "school.state",
    "url":            "school.school_url",
    "locale":         "school.locale",
    "size":           "latest.student.size",
    "tuition_in":     "latest.cost.tuition.in_state",
    "tuition_out":    "latest.cost.tuition.out_of_state",
    "avg_net_price":  "latest.cost.avg_net_price.overall",
    "admission_rate": "latest.admissions.admission_rate.overall",
    "sat_avg":        "latest.admissions.sat_scores.average.overall",
    "act_mid":        "latest.admissions.act_scores.midpoint.cumulative",
    "lat":            "location.lat",
    "lon":            "location.lon",
}

API_FIELDS = ",".join(FIELD_MAP.values())