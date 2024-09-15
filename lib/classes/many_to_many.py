from __init__ import CURSOR, CONN

class Band:
    
    all = {}
    
    def __init__(self, name, hometown='a place that has to remain confidential', id=None):
        self.id = id
        self.name = name
        self.hometown = hometown
    
    def __repr__(self):
        return f"Band {self.id}: {self.name}, {self.hometown}"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value
    
    # @property
    # def hometown(self):
    #     return self._hometown
    
    # @hometown.setter
    # def hometown(self, value):
    #     if not isinstance(value, str):
    #         raise ValueError("Hometown must be a string")
    #     self._hometown = value
    
    @classmethod
    def create_table(cls):
        sql = '''
        CREATE TABLE IF NOT EXISTS bands (
            id INTEGER PRIMARY KEY,
            name TEXT,
            hometown TEXT
        )
        '''
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = '''
        DROP TABLE IF EXISTS bands;
        '''
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def instance_from_db(cls, row):
        return cls(id=row[0], name=row[1], hometown=row[2])

    def save(self):
        if self.id is None:
            sql = '''
            INSERT INTO bands (name, hometown)
            VALUES (?, ?)
            '''
            CURSOR.execute(sql, (self.name, self.hometown))
            CONN.commit()
            self.id = CURSOR.lastrowid
            Band.all[self.id] = self
        else:
            sql = '''
            UPDATE bands
            SET name = ?, hometown = ?
            WHERE id = ?
            '''
            CURSOR.execute(sql, (self.name, self.hometown, self.id))
            CONN.commit()
        Band.all[self.id] = self
        
        
    def concerts(self):
        sql = '''
        SELECT * 
        FROM concerts
        WHERE band_id = ?;
        '''
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Concert.instance_from_db(row) for row in rows]

    def venues(self):
        concerts = self.concerts()
        venues = set()  # Use a set to avoid duplicates
        for concert in concerts:
            venue = concert.venue()  # Fetch the venue for each concert
            venues.add(venue)
        return list(venues)  # Convert the set back to a list
    
    
    def play_in_venue(self, venue, date):
        venue_id = CURSOR.execute('SELECT id FROM venues WHERE title = ?', (venue,)).fetchone()
        if venue_id:
            venue_id = venue_id[0]
        else:
            CURSOR.execute('INSERT INTO venues (title) VALUES (?)', (venue,))
            CONN.commit()
            venue_id = CURSOR.lastrowid
        
        sql = '''
        INSERT INTO concerts (date, name, band_id, venue_id)
        VALUES (?, ?, ?, ?)
        '''
        CURSOR.execute(sql, (date, self.name, self.id, venue_id))
        CONN.commit()
        
        pass

    def all_introductions(self):
        concerts = self.concerts()
        introductions = []
        for concert in concerts:
            introduction = concert.introduction()
            introductions.append(introduction)
        return introductions
    
    @classmethod
    def most_performances(cls):
        sql = '''
        SELECT bands.id, bands.name, COUNT(concerts.id) as performance_count
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        GROUP BY bands.id
        ORDER BY performance_count DESC
        LIMIT 1
        '''
        result = CURSOR.execute(sql).fetchone()
        if result:
            band_id = result[0]
            return cls.all.get(band_id)
        return None


class Concert:
    
    all = {}
    
    def __init__(self, date, name, band, venue, id=None):
        self.name = name
        self.date = date
        self.band_name = band
        self.venue_title = venue
        self.id = id
        
        self.band_id = self._get_or_create_band_id(band)
        self.venue_id = self._get_or_create_venue_id(venue)
    
    def __repr__(self):
        return (f"Concert {self.id}: [ Date: {self.date!r}, Name : {self.name!r}, "
                f"band_name: {self.band_name!r}, venue_title : {self.venue_title!r}, "
                f"band_id: {self.band_id}, venue_id: {self.venue_id} ]")
    
    def _get_or_create_band_id(self, band_name):
        result = CURSOR.execute('SELECT id FROM bands WHERE name = ?', (band_name,)).fetchone()
        if result:
            return result[0]  # Return existing band ID

        CURSOR.execute('INSERT INTO bands (name) VALUES (?)', (band_name,))
        CONN.commit()
        return CURSOR.lastrowid  # Return newly created band ID

    def _get_or_create_venue_id(self, venue_title):
        result = CURSOR.execute('SELECT id FROM venues WHERE title = ?', (venue_title,)).fetchone()
        if result:
            return result[0]  # Return existing venue ID

        CURSOR.execute('INSERT INTO venues (title) VALUES (?)', (venue_title,))
        CONN.commit()
        return CURSOR.lastrowid  # Return newly created venue ID
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        if not isinstance(value, str):
            raise ValueError("Date must be a string")
        self._date = value


        
    @classmethod
    def create_table(cls):
        sql = '''
        CREATE TABLE IF NOT EXISTS concerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            name TEXT,
            band_id INTEGER,
            venue_id INTEGER,
            FOREIGN KEY (band_id) REFERENCES bands(id),
            FOREIGN KEY (venue_id) REFERENCES venues(id)
        )
        '''
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql = '''
        DROP TABLE IF EXISTS concerts;
        '''
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        if self.id is None:
            sql = '''
            INSERT INTO concerts (date, name, band_id, venue_id)
            VALUES (?, ?, ?, ?)
            '''
            CURSOR.execute(sql, (self.date, self.name, self.band_id, self.venue_id))
            CONN.commit()
            self.id = CURSOR.lastrowid
            Concert.all[self.id] = self
        else:
            sql = '''
            UPDATE concerts
            SET date = ?, name = ?, band_id = ?, venue_id = ?
            WHERE id = ?
            '''
            CURSOR.execute(sql, (self.date, self.name, self.band_id, self.venue_id, self.id))
            CONN.commit()

    @classmethod
    def instance_from_db(cls, row):
        if row:
            return cls(date=row[1], name=row[2], band=row[3], venue=row[4], id=row[0])
        return None
    
    def band(self):
        sql = '''
        SELECT * 
        FROM bands
        WHERE id = ?;
        '''
        row = CURSOR.execute(sql, (self.band_id,)).fetchone()
        return Band.instance_from_db(row)
    
    def venue(self):
        sql = '''
        SELECT * 
        FROM venues
        WHERE id = ?;
        '''
        row = CURSOR.execute(sql, (self.venue_id,)).fetchone()
        return Venue.instance_from_db(row)

    def hometown_show(self):
        sql = '''
        SELECT bands.hometown, venues.city
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        JOIN venues ON concerts.venue_id = venues.id
        WHERE concerts.id = ?;
        '''
        result = CURSOR.execute(sql, (self.id,)).fetchone()
    
        if result:
            band_hometown, venue_city = result

            return band_hometown == venue_city
    
        print("No result found for concert ID:", self.id)
        return False


    def introduction(self):
        band = self.band()
        venue = self.venue()
        return f"Hello {venue.city}!!!!! We are {band.name} and we're from {band.hometown}"

class Venue:
    
    all = {}
    
    def __init__(self, title, city, id=None):
        self.title = title
        self.city = city
        self.id = id
        
    def __repr__(self):
        return f"Venue {self.id}: {self.title}, {self.city}"
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        self._title = value

    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, value):
        if not isinstance(value, str):
            raise ValueError("City must be a string")
        self._city = value
    
    @classmethod
    def create_table(cls):
        sql = '''
        CREATE TABLE IF NOT EXISTS venues (
            id INTEGER PRIMARY KEY,
            title TEXT,
            city TEXT DEFAULT "Look from Google Maps"
        )
        '''
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = '''
        DROP TABLE IF EXISTS venues;
        '''
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def instance_from_db(cls, row):
        return cls(id=row[0], title=row[1], city=row[2])
    
    def save(self):
        if self.id is None:
            sql = '''
            INSERT INTO venues (title, city)
            VALUES (?, ?)
            '''
            CURSOR.execute(sql, (self.title, self.city))
            CONN.commit()
            self.id = CURSOR.lastrowid
            Venue.all[self.id] = self
        else:
            sql = '''
            UPDATE venues
            SET title = ?, city = ?
            WHERE id = ?
            '''
            CURSOR.execute(sql, (self.title, self.city, self.id))
            CONN.commit()
        Venue.all[self.id] = self
        
    def concerts(self):
        sql = '''
        SELECT * 
        FROM concerts
        WHERE venue_id = ?;
        '''
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Concert.instance_from_db(row) for row in rows]


    def bands(self):
        sql = '''
        SELECT DISTINCT bands.*
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.venue_id = ?;
        '''
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Band.instance_from_db(row) for row in rows]

    def most_frequent_band(self):
        sql = '''
        SELECT bands.id, bands.name, COUNT(concerts.id) as performance_count
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        WHERE concerts.venue_id = ?
        GROUP BY bands.id
        ORDER BY performance_count DESC
        LIMIT 1
        '''
        result = CURSOR.execute(sql, (self.id,)).fetchone()
        # print("Most Frequent Band Result:", result)
        if result:
            band_id = result[0]
            return Band.instance_from_db(result)  
        return None

    def concert_on(self, date):
        sql = '''
        SELECT * 
        FROM concerts
        WHERE venue_id = ? AND date = ?
        LIMIT 1;
        '''
        result = CURSOR.execute(sql, (self.id, date)).fetchone()
        return Concert.instance_from_db(result) if result else None