# -*- coding: utf-8 -*-
import numpy as np
from riverClasses import PointXY, PointRowCol, InterpolationGrid
from riverIO import (load_parameters, load_cross_sections,
                     load_points, save_river_outline, save_res_points)
from riverUtil import pairwise, print_decorate


@print_decorate
def create_interpolation_grid(cross_sections, dx):
    total_length = np.sum(
        [
            section1.station - section0.station
            for section0, section1 in pairwise(cross_sections)
        ]
    )

    average_width = np.mean(
        [
            np.linalg.norm(section.p_left - section.p_right)
            for section in cross_sections
        ]
    )

    num_rows = int(np.ceil(total_length / dx))
    num_cols = int(np.ceil(average_width / dx))

    grid = InterpolationGrid(
        num_rows=num_rows,
        num_cols=num_cols,
        dx=dx,
        ss=np.zeros(shape=(num_rows, num_cols)),
        xs=np.zeros(shape=(num_rows, num_cols)),
        ys=np.zeros(shape=(num_rows, num_cols))
    )

    for i in range(num_rows):
        s = total_length * i / (num_rows - 1)
        for section0, section1 in pairwise(cross_sections):
            if section0.station <= s <= section1.station:
                break

        alpha = (s - section0.station) / (section1.station - section0.station)
        for j in range(num_cols):
            beta = float(j) / (num_cols - 1)

            grid.xs[i, j], grid.ys[i, j] = (
                (1 - alpha) * (section0.p_left + (section0.p_right - section0.p_left) * beta) +
                alpha * (section1.p_left + (section1.p_right - section1.p_left) * beta))
        grid.ss[i, :] = s

    return grid


def pointXYtoRowCol(grid, pointXY):
    # Find nearest row, col
    dist_sq = np.power(
        grid.xs - pointXY.p[0], 2) + np.power(grid.ys - pointXY.p[1], 2)
    if np.amin(dist_sq) > (10*grid.dx)**2:
        return None
    i_min, j_min = np.unravel_index(
        np.argmin(dist_sq), shape=grid.xs.shape)

    return PointRowCol(row=i_min, col=j_min, z=pointXY.z)


@print_decorate
def align_points_to_grid(grid, pointXYs):
    points = [pointXYtoRowCol(grid, pointXY) for pointXY in pointXYs]
    return list(filter(lambda point: point is not None, points))


@print_decorate
def interpolateIDW(grid, points, anisotropy=20, num_neighbours=10, power=1):
    res_points = []
    eps = grid.dx / 10
    print(f"num_rows={grid.num_rows}, num_cols={grid.num_cols}")
    for i in range(grid.num_rows):
        for j in range(grid.num_cols):
            data = []
            for point in points:
                dist = ((float(point.row - i) / anisotropy)**2 +
                        (float(point.col - j)**2))**0.5 + eps
                data.append((dist, point))
            data.sort(key=lambda x: x[0])

            if len(data) > num_neighbours:
                data = data[0:num_neighbours]

            z = (sum(row[1].z / (row[0]**power) for row in data)
                 / sum(1.0 / (row[0]**power) for row in data))

            res_points.append(PointXY(
                p=np.array([grid.xs[i, j], grid.ys[i, j]]),
                z=z
            ))
    return res_points


def main():
    parameters = load_parameters()

    cross_sections, cross_sections_crs = load_cross_sections(
        parameters["cross_section_file_name"],
        parameters["cross_section_order_field_name"]
    )
    grid = create_interpolation_grid(
        cross_sections,
        parameters["dx"]
    )

    pointXYs, points_crs = load_points(
        parameters["points_file_name"],
        parameters["points_z_field_name"]
    )

    if cross_sections_crs != points_crs:
        raise Exception("CRS doesn't match")

    save_river_outline(
        cross_sections,
        parameters["river_outline_file_name"],
        cross_sections_crs
    )

    points = align_points_to_grid(grid, pointXYs)

    res_points = interpolateIDW(
        grid,
        points,
        anisotropy=parameters["anisotropy"]
    )

    save_res_points(
        res_points,
        parameters["results_file_name"],
        cross_sections_crs
    )


if __name__ == "__main__":
    main()
