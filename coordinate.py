import math

def center_point(points):
    if len(points) == 2:
        return {
            'x': (points[0]['x'] + points[1]['x']) / 2,
            'y': (points[0]['y'] + points[1]['y']) / 2
        }
    elif len(points) > 2:
        area = x = y = 0
        j = len(points) - 1
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[j]
            f = p1['y'] * p2['x'] - p2['y'] * p1['x']
            x += (p1['x'] + p2['x']) * f
            y += (p1['y'] + p2['y']) * f
            area += f * 3
            j = i
        return {'x': x / area, 'y': y / area}
    else:
        return {'x': points[0]['x'], 'y': points[0]['y']}

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371e3
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

import math

def get_coordinates(lat, lng, rad, stp):
    positions = []
    radius = rad
    step_size = stp
    user_latitude = lat
    user_longitude = lng

    lat_offset = -radius / 111320
    lon_offset_limit = radius / (111320 * math.cos(math.radians(user_latitude)))

    while lat_offset <= radius / 111320:
        lon_offset = -lon_offset_limit
        while lon_offset <= lon_offset_limit:
            lat = user_latitude + lat_offset
            lng = user_longitude + lon_offset

            distance = calculate_distance(user_latitude, user_longitude, lat, lng)
            if distance <= radius:
                positions.append({'x': lat, 'y': lng})
            lon_offset += step_size
        lat_offset += step_size

    return positions

def get_radius_boundary(lat, lng, radius):
    lat_change = radius / 111.32
    lng_change = abs(math.cos(lat * (math.pi / 180)))

    return {
        "lat_min": lat - lat_change,
        "lng_min": lng - lng_change,
        "lat_max": lat + lat_change,
        "lng_max": lng + lng_change
    }

def get_accurate_radius_boundary(lat, lon, radius):
    
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    # 지구의 반지름 (킬로미터)
    earth_radius_km = 6371.0

    # 반경으로 커버되는 각 거리를 계산
    angular_radius = radius / earth_radius_km

    # 위도 경계 계산
    lat_min = lat_rad - angular_radius
    lat_max = lat_rad + angular_radius

    # 경도 경계 계산
    # 위도에 따른 경도 변경 조정
    lon_deg_per_km = (math.pi / 180.0) * earth_radius_km * math.cos(lat_rad)
    lng_min = lon_rad - angular_radius / lon_deg_per_km
    lng_max = lon_rad + angular_radius / lon_deg_per_km

    # 경계를 라디안에서 도로 변환
    lat_min = math.degrees(lat_min)
    lat_max = math.degrees(lat_max)
    lng_min = math.degrees(lng_min)
    lng_max = math.degrees(lng_max)

    return {
        "lat_min": lat_min,
        "lng_min": lng_min,
        "lat_max": lat_max,
        "lng_max": lng_max
    }

coordinates = get_coordinates(35.214461, 129.116741, 1000, 0.0001)
boundary = get_radius_boundary(35.214461, 129.116741, 10)
accurate_bound = get_accurate_radius_boundary(35.214461, 129.116741, 10)
center = center_point(coordinates)


print(test)
print(test2)
print(center)
# print(coordinates)