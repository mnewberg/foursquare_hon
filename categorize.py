import re

def categorize(venue):
     if re.findall('.*Arcade|.*Gallery|.*Casino|.*Alley|.*Club|*.Cafe|.*Entertainment|.*Museum|.*Venue|.*Hall|.*Bar|.*Racetrack|.*Park|.*Zoo|.*Aquarium|.*Restaurant|.*Joint|.*Shop|.*Bakery|.*Brewery|.*Diner|.*Court|.*Place|.*Steakhouse|.*Winery|.*Garden|.*Beer.*|.*Lounge|.*Pub|.*Speakeasy|.*Run|.*Marina|.*Harbor|.*Trail|.*Lake|.*Spring|.*Plaza|.*Pool|.*Rink|.*Lodge|.*Chalet|.*Vineyard|.*Store|.*Market|.*Parlor|.*Breakfast|.*Hostel|.*Motel|.*Hotel|.*Deck',venue,flags=re.IGNORECASE):
          return venue
