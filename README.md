# CollegeMatch

A personalized college recommendation system that helps high school students find their best-fit universities based on individual preferences and constraints.

---

## Overview

CollegeMatch is a college search and recommendation platform designed to help students identify colleges that match their preferences and constraints. Instead of presenting overwhelming lists of options, the system narrows choices to a manageable set of relevant colleges and explains why each one is a good fit.

---

## Problem Statement

High school students face an overwhelming early decision when applying to college: which universities are even worth applying to?

With thousands of options, students usually start with scattered sources like rankings, Reddit threads, and individual college websites. These sources rarely help them filter schools based on a specific mix of personal constraints and preferences. As a result, students often build lists that are too broad, miss good-fit schools, or waste time researching colleges that are unrealistic financially or geographically.

---

## Features

**Core Functionality**
- Smart filtering based on non-negotiable constraints (max tuition, distance, required majors)
- Personalized ranking based on weighted preferences
- Climate matching for preferred weather conditions
- Distance calculations from home location
- Clear explanations for why each school was recommended
- Safety/Target/Reach labels based on academic profile (optional)

**Supported Preferences**
- Budget (max tuition or net price)
- Distance from home
- Weather preferences (warm, cool, rain tolerance)
- Campus setting (urban, suburban, rural)
- Campus size (small, medium, large)
- Major or field of study
- Academic fit via GPA/SAT/ACT (optional)

---

## System Architecture

### Components

| Component | Description |
|-----------|-------------|
| User Preference Manager | Collects and stores student constraints and preferences |
| College Data Collector | Gathers and normalizes college information from public datasets |
| Location & Distance Processor | Determines nearby colleges based on student location |
| Climate Context Module | Evaluates weather conditions for each college location |
| Filtering & Ranking Engine | Removes non-qualifying colleges, ranks remaining options |
| Recommendation Module | Generates explanations for why each college was suggested |
| User Interface | Presents recommendations and allows preference updates |

---

## Data Sources

| Data Type | Source | Update Frequency |
|-----------|--------|------------------|
| College Information | College Scorecard API | Stored locally |
| Weather/Climate | NWS API / NOAA CDO | Cached summaries |
| Distance/Travel | Mapbox or Google Maps API | On-demand |
| User Preferences | User input | Real-time |

**College Data Points:**
- Tuition and financial aid
- SAT/ACT acceptance ranges
- Degree offerings
- Geographic coordinates
- Campus size and setting

**Climate Data Points:**
- Historical temperature ranges
- Precipitation patterns
- Seasonal summaries

---

## How It Works

1. **Onboarding** - Student enters home location, budget constraints, weather preferences, campus preferences, and optionally their academic profile.

2. **Filtering** - System removes colleges that don't meet non-negotiable requirements.

3. **Ranking** - Remaining colleges are scored based on preference weights.

4. **Recommendations** - System presents a ranked list with explanations and optional safety/target/reach labels.

5. **Refinement** - Student adjusts preferences and results update automatically.

### Ranking Logic

A college ranks higher when it better matches the student's priorities after all constraints are met. Schools within budget and distance limits rank above those that barely qualify. Within the eligible set, the system favors colleges whose climate, campus setting, size, and selectivity match the student's preferences.

---

## Project Scope

### In Scope
- Functional prototype with ranked college recommendations
- Onboarding flow for preference collection
- Searchable recommendation interface
- Basic explanation feature for recommendations
- Integration with US college dataset
- Weather and distance data sources

### Out of Scope
- Real-time tuition change tracking
- Guaranteed acceptance percentages
- Application submission tools
- Counselor messaging features

---

## Team

**Team Name:** CollegePrep

| Member | Role | Responsibilities |
|--------|------|------------------|
| Amratha Rao | Data & Backend | Data sourcing, backend logic, filtering rules |
| Vathsan Sankaranarayanan | Systems & Integration | Recommendation logic, user preference translation |
| Dia Ganesh Kumar | UI/UX | Interface design, preference input, result presentation |

UCI NetIDs: amrathr, srivats3, dganeshk

---

## Roadmap

| Phase | Tasks |
|-------|-------|
| Phase 1 | Integrate College Scorecard API, set up database, implement basic filtering |
| Phase 2 | Build preference manager, develop ranking algorithm, add distance calculations |
| Phase 3 | Weather data integration, match explanation generation, safety/target/reach labeling |
| Phase 4 | Onboarding flow, results display, preference adjustment controls |
| Phase 5 | User testing, algorithm tuning, documentation |

---

## Anticipated Challenges

| Challenge | Mitigation |
|-----------|------------|
| Data format inconsistencies across sources | Robust normalization layer |
| Subjective weather preferences | Clear category definitions |
| Over-filtering leading to too few results | Progressive filter relaxation |
| Overwhelming number of recommendations | Limit initial results with option to expand |

---

## Acknowledgments

- UC Irvine
- College Scorecard for open data access
- NOAA/NWS for climate data
