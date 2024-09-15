from classes.many_to_many import Band
from classes.many_to_many import Concert
from classes.many_to_many import Venue

class TestVenue:
    """Venue in many_to_many.py"""
    
    def test_has_name(self):
        """Venue is instantiated with a name"""
        venue = Venue(name="Theedge", city="SAC")

        assert venue.name == "Theedge"

    def test_name_is_mutable_string(self):
        """names are mutable strings"""
        venue_1 = Venue(name="Theedge", city="SAC")
        assert isinstance(venue_1.name, str)

        venue_1.name = "Rollingloud"
        assert isinstance(venue_1.name, str)
        assert venue_1.name == "Rollingloud"

        venue_1.name = 7
        assert venue_1.name == "Rollingloud"

    def test_name_has_length(self):
        """names are longer than 0 characters"""
        venue_1 = Venue(name="Theedge", city="SAC")
        assert len(venue_1.name) > 0

        venue_1.name = ""
        assert venue_1.name == "Theedge"

    def test_has_city(self):
        """Venue is instantiated with a city"""
        venue = Venue(name="Theedge", city="SAC")

        assert venue.city == "SAC"

    def test_city_is_mutable_string(self):
        """cities are mutable strings"""
        venue_1 = Venue(name="Theedge", city="SAC")
        assert isinstance(venue_1.city, str)

        venue_1.city = "LA"
        assert isinstance(venue_1.city, str)
        assert venue_1.city == "LA"

        venue_1.city = 7
        assert venue_1.city == "LA"
        venue_1.city = "LA"

    def test_city_has_length(self):
        """cities are longer than 0 characters"""
        venue_1 = Venue(name="Theedge", city="SAC")
        assert len(venue_1.city) > 0

        venue_1.city = "LA"
        assert venue_1.city == "SAC"


    def test_concerts(self):
        """venue has many concerts"""
        band = Band(name="Onedirection", hometown="LA")
        venue = Venue(name="Theatre Max", city="LA")
        concert_1 = Concert(date="May 31", band=band, venue=venue)
        concert_2 = Concert(date="May 31", band=band, venue=venue)

        assert len(venue.concerts()) == 2
        assert concert_1 in venue.concerts()
        assert concert_2 in venue.concerts()

    def test_concerts_of_type_concert(self):
        """concerts must be of type Concert"""
        band = Band(name="", hometown="LA")
        venue = Venue(name="Theatre Max", city="LA")
        Concert(date="Dec 2", band=band, venue=venue)
        Concert(date="Nov 28", band=band, venue=venue)

        assert all(isinstance(concert, Concert) for concert in venue.concerts())

    def test_bands(self):
        """venue has many bands"""
        band_1 = Band(name="Onedirection", hometown="NYC")
        band_2 = Band(name="Sautisol", hometown="LA")
        venue_1 = Venue(name="Theatre", city="NYC")
        Concert(date="Dec 2", band=band_1, venue=venue_1)
        Concert(date="Nov 28", band=band_2, venue=venue_1)

        assert len(venue_1.bands()) == 2
        assert band_1 in venue_1.bands()
        assert band_2 in venue_1.bands()

    def test_bands_of_type_band(self):
        """bands must be of type Band"""
        band_1 = Band(name="Onedirection", hometown="NYC")
        band_2 = Band(name="Sautisol", hometown="LA")
        venue_1 = Venue(name="Theatre", city="NYC")
        Concert(date="Dec 2", band=band_1, venue=venue_1)
        Concert(date="Nov 28", band=band_2, venue=venue_1)

        assert all(isinstance(band, Band) for band in venue_1.bands())

    def test_bands_are_unique(self):
        """bands are unique"""
        band_1 = Band(name="Onedirection", hometown="NYC")
        band_2 = Band(name="Sautisol", hometown="LA")
        venue_1 = Venue(name="Theatre", city="NYC")
        Concert(date="Dec 2", band=band_1, venue=venue_1)
        Concert(date="Dec 2", band=band_2, venue=venue_1)
        Concert(date="Nov 28", band=band_2, venue=venue_1)

        assert len(set(venue_1.bands())) == len(venue_1.bands())
        assert len(venue_1.bands()) == 2
        assert band_1 in venue_1.bands()
        assert band_2 in venue_1.bands()

    # def test_concert_on(self):
    #     """returns the first concert on that date or None if no concerts exist"""
    #     band = Band(name="boygenius", hometown="NYC")
    #     venue = Venue(name="Theatre", city="NYC")
    #     venue2 = Venue(name="Ace of Spades", city="SAC")
    #     band.play_in_venue(venue=venue, date="Nov 22")
    #     band.play_in_venue(venue=venue2, date="Nov 27")

    #     assert venue.concert_on("Nov 22") == band.concerts()[0]
    #     assert venue2.concert_on("Nov 27") == band.concerts()[1]
    #     assert venue.concert_on("Nov 25") is None
