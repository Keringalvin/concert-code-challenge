
import ipdb
    
from __init__ import CONN, CURSOR
from classes.many_to_many import Band
from classes.many_to_many import Concert
from classes.many_to_many import Venue

if __name__ == '__main__':
    print("HELLO! :) let's debug :vibing_potato:")
    
    Band.drop_table()
    Band.create_table()
    
    Concert.drop_table()
    Concert.create_table()
    
    Venue.drop_table()
    Venue.create_table()
    
    band1 = Band(name="one voice", hometown="London")
    band1.save()

    band2 = Band(name="Vintage lee", hometown="los angeles")
    band2.save()

    band3 = Band(name="Raiders", hometown="Aberdare")
    band3.save()

    venue1 = Venue(title="Wembley Stadium", city="London")
    venue1.save()

    venue2 = Venue(title="Ayo and Teo", city="Los Angeles")
    venue2.save()

    venue3 = Venue(title="The salvatores", city="Mystic falls")
    venue3.save()
    
    concert1 = Concert(date="2024-09-01", name="Rock Extravaganza", band=band1.name, venue=venue1.title)
    concert1.save()

    concert2 = Concert(date="2024-09-15", name="Nirvana's Last Stand", band=band2.name, venue=venue2.title)
    concert2.save()

    concert3 = Concert(date="2024-10-05", name="Radiohead Live", band=band3.name, venue=venue3.title)
    concert3.save()
    
    concert4 = Concert(date="2024-10-05", name="Radiohead Live", band="Nicki", venue="MInaj")
    concert4.save()
    
    print(concert1.band())  
    print(concert1.venue())  
    
    venue = Venue.all[1]
    venue.concerts()
    venue.bands()
    
    band = Band.all[1]
    band.concerts()
    band.venues()
    
    
    ipdb.set_trace()
