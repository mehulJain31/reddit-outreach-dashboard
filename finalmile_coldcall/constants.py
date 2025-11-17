"""Constants for location parsing and Reddit scraping."""

import us

# Regex patterns for extracting city/state from titles
LOCATION_PATTERNS = [
    r"([A-Za-z\s]+?),\s*([A-Z]{2})\b",         # City, ST
    r"([A-Za-z\s]+?)\s+([A-Z]{2})\b",          # City ST (word boundary)
    r"([A-Za-z\s]+?),\s*([A-Za-z\s]+?)\s*[$]", # City, State (before $)
    r"([A-Za-z\s]+?)\s+([A-Z][a-z]+\s?[A-Za-z]*)\s*[$]", # City State (before $)
    r"([A-Za-z\s]+?)\s+([A-Z]{2})\s*[0-9]",    # City ST before number
]

# Generate state mappings from us library
STATE_MAP = {state.name: state.abbr for state in us.states.STATES}
STATE_FULL_MAP = {state.abbr: state.name for state in us.states.STATES}

# Map airport codes to city/state
AIRPORT_MAP = {
    "RNO": "Reno, NV",
    "DFW": "Dallas-Fort Worth, TX",
    "ATL": "Atlanta, GA",
    "LAX": "Los Angeles, CA",
    "ORD": "Chicago, IL",
    "DEN": "Denver, CO",
    "PHX": "Phoenix, AZ",
    "SAN": "San Diego, CA",
    "SEA": "Seattle, WA",
    "MIA": "Miami, FL",
    "BOS": "Boston, MA",
    "LAS": "Las Vegas, NV",
    "SFO": "San Francisco, CA",
    "SLC": "Salt Lake City, UT",
    "MSP": "Minneapolis, MN",
    "DTW": "Detroit, MI",
    "CLT": "Charlotte, NC",
    "PHL": "Philadelphia, PA",
    "LGA": "New York, NY",
    "BWI": "Baltimore, MD",
    "DCA": "Washington, DC",
    "IAH": "Houston, TX",
    "HOU": "Houston, TX",
    "DAL": "Dallas, TX",
    "JFK": "New York, NY",
    "EWR": "Newark, NJ",
    "OAK": "Oakland, CA",
    "SJC": "San Jose, CA",
    "SMF": "Sacramento, CA",
    "PDX": "Portland, OR",
    "TUS": "Tucson, AZ",
    "ABQ": "Albuquerque, NM",
    "OKC": "Oklahoma City, OK",
    "TUL": "Tulsa, OK",
    "OMA": "Omaha, NE",
    "MCI": "Kansas City, MO",
    "STL": "St. Louis, MO",
    "CVG": "Cincinnati, OH",
    "CMH": "Columbus, OH",
    "CLE": "Cleveland, OH",
    "IND": "Indianapolis, IN",
    "MKE": "Milwaukee, WI",
    "BNA": "Nashville, TN",
    "MEM": "Memphis, TN",
    "RDU": "Raleigh, NC",
    "CHS": "Charleston, SC",
    "JAX": "Jacksonville, FL",
    "TPA": "Tampa, FL",
    "MCO": "Orlando, FL",
    "FLL": "Fort Lauderdale, FL",
    "PBI": "West Palm Beach, FL",
    "HNL": "Honolulu, HI",
    "ANC": "Anchorage, AK",
}

# List of known city names for fallback extraction (major US cities)
KNOWN_CITIES = [
    # Largest cities by population
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis",
    "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville",
    "Detroit", "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville",
    "Milwaukee", "Baltimore", "Albuquerque", "Tucson", "Fresno", "Sacramento",
    "Kansas City", "Mesa", "Atlanta", "Omaha", "Colorado Springs", "Raleigh",
    "Miami", "Oakland", "Minneapolis", "Tampa", "Tulsa", "Arlington", "Wichita",
    "New Orleans", "Bakersfield", "Cleveland", "Aurora", "Anaheim", "Honolulu",
    "Santa Ana", "Riverside", "Corpus Christi", "Lexington", "Henderson",
    "Stockton", "St. Paul", "Cincinnati", "Irvine", "Greensboro", "Pittsburgh",
    "Lincoln", "St. Louis", "Orlando", "Durham", "Plano", "Anchorage", "Newark",
    "Chula Vista", "Fort Wayne", "Chandler", "Laredo", "Scottsdale", "Glendale",
    "Gilbert", "Reno", "Buffalo", "Jersey City", "Garland", "Irving", "Hialeah",
    "Fremont", "Greensboro", "Rochester", "Spokane", "Madison", "Baton Rouge",
    
    # State capitals
    "Montgomery", "Juneau", "Little Rock", "Sacramento", "Denver", "Hartford",
    "Dover", "Tallahassee", "Atlanta", "Honolulu", "Boise", "Springfield",
    "Indianapolis", "Des Moines", "Topeka", "Frankfort", "Baton Rouge", "Augusta",
    "Annapolis", "Boston", "Lansing", "Saint Paul", "Jackson", "Jefferson City",
    "Helena", "Lincoln", "Carson City", "Concord", "Trenton", "Santa Fe", "Albany",
    "Raleigh", "Bismarck", "Columbus", "Oklahoma City", "Salem", "Harrisburg",
    "Providence", "Columbia", "Pierre", "Nashville", "Austin", "Salt Lake City",
    "Montpelier", "Richmond", "Charleston", "Madison", "Cheyenne",
    
    # Other notable cities by region
    "Birmingham", "Richmond", "Louisville", "Grand Rapids", "Tucson", "Fresno",
    "Mesa", "Colorado Springs", "Omaha", "Raleigh", "Miami", "Kansas City",
    "Long Beach", "Virginia Beach", "Oakland", "Minneapolis", "Tampa", "Tulsa",
    "Arlington", "Wichita", "New Orleans", "Bakersfield", "Cleveland", "Aurora",
    "Anaheim", "Honolulu", "Santa Ana", "Riverside", "Corpus Christi", "Lexington",
    "Henderson", "Stockton", "St. Paul", "Cincinnati", "Irvine", "Greensboro",
    "Pittsburgh", "Lincoln", "St. Louis", "Orlando", "Durham", "Plano", "Anchorage",
    "Newark", "Chula Vista", "Fort Wayne", "Chandler", "Laredo", "Scottsdale",
    "Glendale", "Gilbert", "Reno", "Buffalo", "Jersey City", "Garland", "Irving",
    "Hialeah", "Fremont", "Spokane", "Baton Rouge", "Bridgeport", "New Haven",
    "Stamford", "Waterbury", "Norwalk", "Danbury", "New Britain", "Bristol",
    "Meriden", "West Hartford", "East Hartford", "Middletown", "Enfield", "Glastonbury",
    "Norwich", "Torrington", "Trumbull", "Wallingford", "Stratford", "Milford",
    "Ansonia", "Middletown", "Derby", "Groton", "Shelton", "East Haven", "Naugatuck",
    "West Haven", "Manchester", "South Windsor", "Glastonbury", "Farmington", "Enfield",
    "Vernon", "Shelton", "East Hartford", "Middletown", "Newington", "Naugatuck",
    "Stamford", "Norwalk", "Danbury", "Bristol", "Meriden", "West Hartford",
    "East Hartford", "Middletown", "Enfield", "Glastonbury", "Norwich", "Torrington",
    "Trumbull", "Wallingford", "Stratford", "Milford", "Ansonia", "Middletown",
    "Derby", "Groton", "Shelton", "East Haven", "Naugatuck", "West Haven",
    "Manchester", "South Windsor", "Glastonbury", "Farmington", "Enfield", "Vernon",
]

# Default request headers for Reddit API
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
