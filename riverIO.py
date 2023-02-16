import json
import numpy as np
from riverClasses import CrossSection, PointXY
from riverUtil import pairwise, print_decorate


@print_decorate
def load_parameters():
    with open("parameters.json", "r") as f:
        parameters = json.load(f)

    return parameters


@print_decorate
def load_cross_sections(file_name, order_field_name="s"):
    with open(file_name, "r") as f:
        geojson_data = json.load(f)

    crs = geojson_data["crs"]["properties"]["name"]

    cross_sections = []
    for feature in geojson_data["features"]:
        if feature["geometry"]["type"] == "MultiLineString":
            p_left = np.array(feature["geometry"]["coordinates"][0][0])
            p_right = np.array(feature["geometry"]["coordinates"][0][-1])
        elif feature["geometry"]["type"] == "LineString":
            p_left = np.array(feature["geometry"]["coordinates"][0])
            p_right = np.array(feature["geometry"]["coordinates"][-1])
        else:
            raise Exception("Cross section format not supported")

        cross_sections.append(CrossSection(
            order=feature["properties"][order_field_name],
            station=0.0,
            p_left=p_left,
            p_right=p_right,
        ))

    # Compute cross section stations
    cross_sections = sorted(cross_sections, key=lambda xs: xs.order)
    for section0, section1 in pairwise(cross_sections):
        dist = np.linalg.norm(
            0.5 * (section1.p_left + section1.p_right) -
            0.5 * (section0.p_left + section0.p_right)
        )
        section1.station = section0.station + dist

    return cross_sections, crs


@print_decorate
def load_points(file_name, z_field_name="z"):
    with open(file_name, "r") as f:
        geojson_data = json.load(f)

    crs = geojson_data["crs"]["properties"]["name"]

    points = []
    for feature in geojson_data["features"]:
        if feature["geometry"]["type"] != "Point":
            raise Exception("Point format not supported")

        points.append(PointXY(
            p=np.array(feature["geometry"]["coordinates"][0:2]),
            z=feature["properties"][z_field_name],
        ))

    return points, crs


@print_decorate
def save_river_outline(cross_sections, file_name, crs):
    points = ([list(section.p_right) for section in cross_sections] +
              [list(section.p_left) for section in reversed(cross_sections)])

    data = {
        "type": "FeatureCollection",
        "name": "river_outline",
        "crs": {
            "type": "name",
            "properties": {
                "name": crs
            }
        },
        "features": []
    }

    data["features"].append({
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [list(points)]
        }
    })

    with open(file_name, "w") as f:
        json.dump(data, f)


@print_decorate
def save_res_points(res_points, file_name, crs):
    data = {
        "type": "FeatureCollection",
        "name": "interpolated_points",
        "crs": {
            "type": "name",
            "properties": {
                "name": crs
            }
        },
        "features": []
    }

    for point in res_points:
        data["features"].append({
            "type": "Feature",
            "properties": {
                "z": point.z
            },
            "geometry": {
                "type": "Point",
                "coordinates": list(point.p)
            }
        })

    with open(file_name, "w") as f:
        json.dump(data, f)
