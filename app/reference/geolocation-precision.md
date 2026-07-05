Geolocation Precision

geolocation-precision

1783212139

Latitude/longitude and other geolocation systems can express a position at
exponentially increasing precision as you add digits or levels.  Below are
tables of the approximate ground precision of several coordinate systems.

One degree of latitude is roughly constant everywhere (~111 km), but one degree
of longitude shrinks toward the poles as the meridians converge, scaling with
the cosine of the latitude.  For the latitude/longitude systems below, the
east/west distance is therefore given at several latitudes.  Grid systems like
H3, S2, Geohash, and Plus Codes are designed to be nearly uniform across the
globe, so their precision is instead given as an approximate cell edge length
and area.

## [Degrees with decimals](https://en.wikipedia.org/wiki/Decimal_degrees) (Degrees)

| Degrees | Decimals | E/W at equator | E/W at 20° N/S | E/W at 45° N/S | E/W at 70° N/S |
|---------|----------|----------------|----------------|----------------|----------------|
| 1       | 0        | 111.3 km       | 104.6 km       | 78.72 km       | 38.07 km       |
| 0.1     | 1        | 11.13 km       | 10.46 km       | 7.872 km       | 3.807 km       |
| 0.01    | 2        | 1.113 km       | 1.046 km       | 787.2 m        | 380.7 m        |
| 0.001   | 3        | 111.3 m        | 104.6 m        | 78.72 m        | 38.07 m        |
| 0.0001  | 4        | 11.13 m        | 10.46 m        | 7.872 m        | 3.807 m        |
| 0.00001 | 5        | 1.113 m        | 1.046 m        | 78.7 cm        | 38.1 cm        |

## [Degrees-minutes-seconds](https://en.wikipedia.org/wiki/Geographic_coordinate_system) (DMS)

| Precision      | Unit          | E/W at equator | E/W at 20° N/S | E/W at 45° N/S | E/W at 70° N/S |
|----------------|---------------|----------------|----------------|----------------|----------------|
| 1°00′00″       | degree        | 111.3 km       | 104.6 km       | 78.72 km       | 38.07 km       |
| 0°01′00″       | arcminute     | 1.855 km       | 1.743 km       | 1.312 km       | 634.6 m        |
| 0°00′01″       | arcsecond     | 30.92 m        | 29.06 m        | 21.87 m        | 10.58 m        |
| 0°00′00.1″     | 0.1 arcsecond | 3.092 m        | 2.906 m        | 2.187 m        | 1.058 m        |
| 0°00′00.01″    | 0.01 arcsecond| 30.9 cm        | 29.1 cm        | 21.9 cm        | 10.6 cm        |

## [Geohash](https://en.wikipedia.org/wiki/Geohash) (base32)

Each geohash character adds 5 bits, alternating between longitude and latitude,
so cells are square at odd lengths and 2:1 (wider than tall) at even lengths.

| Length | Cell size (lng × lat) | Ground size at equator      |
|--------|-----------------------|-----------------------------|
| 1      | 45° × 45°             | 5,009 km × 5,009 km         |
| 2      | 11.25° × 5.625°       | 1,252 km × 626.2 km         |
| 3      | 1.406° × 1.406°       | 156.5 km × 156.5 km         |
| 4      | 0.3516° × 0.1758°     | 39.14 km × 19.57 km         |
| 5      | 0.04395° × 0.04395°   | 4.892 km × 4.892 km         |
| 6      | 0.01099° × 0.005493°  | 1.223 km × 611.5 m          |
| 7      | 0.001373° × 0.001373° | 152.9 m × 152.9 m           |
| 8      | 0.0003433° × 0.0001717° | 38.22 m × 19.11 m         |
| 9      | 0.00004292° × 0.00004292° | 4.777 m × 4.777 m       |

## [Plus Codes](https://maps.google.com/pluscodes/) (Open Location Code)

| Code length | Cell size | Ground size at equator |
|-------------|-----------|------------------------|
| 2           | 20°       | 2,226 km               |
| 4           | 1°        | 111.3 km               |
| 6           | 0.05°     | 5.566 km               |
| 8           | 0.0025°   | 278.3 m                |
| 10          | 0.000125° | 13.92 m                |
| 11          | 0.000025° | 2.783 m                |
| 12          | 0.000005° | 55.7 cm                |

## [H3](https://h3geo.org/) hexagonal geospatial indexing

| Resolution | Avg edge length | Avg cell area |
|------------|-----------------|---------------|
| 0          | 1,281 km        | 4,357,449 km² |
| 1          | 483 km          | 609,788 km²   |
| 2          | 183 km          | 86,802 km²    |
| 3          | 68.98 km        | 12,393 km²    |
| 4          | 26.07 km        | 1,770 km²     |
| 5          | 9.854 km        | 253 km²       |
| 6          | 3.725 km        | 36.13 km²     |
| 7          | 1.406 km        | 5.161 km²     |
| 8          | 531.4 m         | 0.7373 km²    |
| 9          | 200.8 m         | 0.1053 km²    |
| 10         | 75.86 m         | 0.01505 km²   |
| 11         | 28.66 m         | 2,150 m²      |
| 12         | 10.83 m         | 307 m²        |
| 13         | 4.092 m         | 43.9 m²       |
| 14         | 1.546 m         | 6.27 m²       |
| 15         | 58.4 cm         | 0.895 m²      |

## [S2](https://s2geometry.io/)

| Level | Avg edge length | Avg cell area |
|-------|-----------------|---------------|
| 0     | 7,842 km        | 85,011,012 km² |
| 4     | 490 km          | 332,074 km²    |
| 8     | 30.63 km        | 1,297 km²      |
| 10    | 7.658 km        | 81.07 km²      |
| 12    | 1.915 km        | 5.067 km²      |
| 16    | 119.7 m         | 0.0198 km²     |
| 20    | 7.479 m         | 77.3 m²        |
| 24    | 46.7 cm         | 0.302 m²       |
| 28    | 2.92 cm         | 11.8 cm²       |
| 30    | 7.3 mm          | 0.737 cm²      |

## [UTM](https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system) (Universal Transverse Mercator)

UTM projects each of 60 longitudinal zones (each 6° wide) onto a flat grid and
expresses a position as an easting/northing in meters within the zone.  Because
the coordinate is already metric, the precision is simply how many digits of the
easting/northing you keep.

| Easting/northing digits | Rounded to | Ground precision |
|-------------------------|------------|------------------|
| 550__                   | 10 km      | 10 km            |
| 5502_                   | 1 km       | 1 km             |
| 55020                   | 100 m      | 100 m            |
| 550200                  | 10 m       | 10 m             |
| 5502001                 | 1 m        | 1 m              |
| 5502001.0               | 0.1 m      | 10 cm            |

## [MGRS](https://en.wikipedia.org/wiki/Military_Grid_Reference_System) (Military Grid Reference System)

MGRS is a grid-based alphanumeric encoding built on UTM (and UPS at the poles):
a grid-zone designator, a 100 km square identifier, then equal numbers of
easting and northing digits.  Each added digit pair narrows the cell tenfold.

| Digits (per axis) | Example         | Ground precision |
|-------------------|-----------------|------------------|
| 0                 | 10SEG           | 100 km           |
| 1                 | 10SEG12         | 10 km            |
| 2                 | 10SEG1234       | 1 km             |
| 3                 | 10SEG123456     | 100 m            |
| 4                 | 10SEG12345678   | 10 m             |
| 5                 | 10SEG1234567890 | 1 m              |

## [Maidenhead](https://en.wikipedia.org/wiki/Maidenhead_Locator_System) locator system

Used by amateur-radio operators, Maidenhead alternates letter and number pairs
(field → square → subsquare → …) to encode longitude and latitude.  Cells are
2:1, wider than tall, because longitude spans 360° against latitude's 180°.

| Characters | Cell size (lng × lat) | Ground size at equator |
|------------|-----------------------|------------------------|
| 2 (field)      | 20° × 10°         | 2,226 km × 1,113 km    |
| 4 (square)     | 2° × 1°           | 223 km × 111 km        |
| 6 (subsquare)  | 5′ × 2.5′         | 9.277 km × 4.638 km    |
| 8 (extended)   | 30″ × 15″         | 927.7 m × 463.8 m      |
| 10             | 1.25″ × 0.625″    | 38.65 m × 19.33 m      |
