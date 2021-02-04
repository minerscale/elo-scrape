import berserk
import random
import pickle
from datetime import datetime

'''
Process raw dict output into a tuple (because they are hashable)
return type: (id, bullet, blitz, rapid, classical, fide)
'''
def process_profile (profile):
    # Check if a FIDE rating is reported
    try:
        profile['profile']['fideRating']
    except KeyError:
        # If not just return an empty array other than username
        return (profile['id'], None, None, None, None, None)

    return (
        profile['id'],
        profile['perfs']['bullet']['rating'],
        profile['perfs']['blitz']['rating'],
        profile['perfs']['rapid']['rating'],
        profile['perfs']['classical']['rating'],
        profile['profile']['fideRating']
    )

client = berserk.Client()

# Set this to the size of the raw dataset (before filtering out FIDE)
cutoff_users = 100

# User to start on
current_user = "minerscale"

# Using sets becuase they do not have duplicates
profiles = set()
users_crawled = set()

# Perform the search
while len(profiles) < cutoff_users:
    # Print cool status
    print('> ' + str(len(profiles)) + '/' + str(cutoff_users) + ' | scraping: ' + current_user + '                          ', end='\r', flush=True)

    # Add the user we're searching to the blacklist of who to search
    users_crawled.add(current_user)

    # Add the new profiles to the set of profiles
    profiles.update(set([process_profile(i) for i in client.users.get_users_followed(current_user)]))

    # Get a new not-before searched profile
    while current_user in users_crawled:
        current_user = random.choice(tuple(profiles))[0]

# Create the list to export to a file
fide_profiles = []
for i in list(profiles):
    # Exclude non-fide profiles
    if i[5] != None: fide_profiles.append(i)

# Create the pickle file timestamped with the current datetime
with open('fide_profiles_'+datetime.now().strftime("%Y-%m-%d-%H%M%S")+'.pickle', 'wb') as file:
    pickle.dump(fide_profiles, file)
