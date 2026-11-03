
import math


def validate_coordinates(latitude, longitude):
    if not -90 <= latitude <= 90:
        raise ValueError("Latitude must be between -90 and 90.")

    if not -180 <= longitude <= 180:
        raise ValueError("Longitude must be between -180 and 180.")


def calculate_distance(lat1, lon1, lat2, lon2):
    validate_coordinates(lat1, lon1)
    validate_coordinates(lat2, lon2)

    # Convert degrees into radians
    lat1, lon1, lat2, lon2 = map(
        math.radians, (lat1, lon1, lat2, lon2)
    )

    # Calculate differences between coordinates
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Apply the Haversine formula
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    # Protect against tiny floating-point rounding errors
    a = max(0.0, min(1.0, a))

    central_angle = 2 * math.asin(math.sqrt(a))

    earth_radius_km = 6371.0
    distance_km = earth_radius_km * central_angle

    return distance_km


def main():
    try:
        print("=== GPS Distance Calculator ===")

        lat1 = float(input("Location 1 latitude: "))
        lon1 = float(input("Location 1 longitude: "))

        lat2 = float(input("Location 2 latitude: "))
        lon2 = float(input("Location 2 longitude: "))

        distance_km = calculate_distance(lat1, lon1, lat2, lon2)
        distance_miles = distance_km * 0.621371

        print(f"\nDistance: {distance_km:.2f} km")
        print(f"Distance: {distance_miles:.2f} miles")

    except ValueError as error:
        print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
