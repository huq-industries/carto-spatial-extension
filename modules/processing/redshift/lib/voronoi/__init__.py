# Copyright (c) 2021, CARTO

from __future__ import division
from scipy.spatial import Voronoi
from ..helper import PRECISION
import helper as lib
import numpy as np
import geojson


def voronoi_generic(geom, bbox, voronoi_type):
    """
    Hihg level method for the computation of lines/polygons based voronoi diagrams
    Args:
        geom: Geojson with the input points
        bbox: Bound box used to clip the diagram. If this parameter
        is set to None a default envelope is applied extended by about
        50% in each direction
        voronoi_type: Type of voronoi (lines/polys)
    Return:
        Geojson with the resulting diagram. It'll return a MultiPolygon or
        MultiLineString in case of 'polys' or 'lines' are received as voronoy_type
        respectively
    """

    # Take the type of geometry
    coords = []
    if geom.type != 'MultiPoint':
        raise Exception('Invalid operation: Input points parameter must be MultiPoint.')
    else:
        coords = list(geojson.utils.coords(geom))

    # Compute some bounds
    coords_array = np.array(coords)
    min_x = min(coords_array[:, 0])
    max_x = max(coords_array[:, 0])
    min_y = min(coords_array[:, 1])
    max_y = max(coords_array[:, 1])

    x_extent = abs(max_x - min_x) * 0.5 if len(coords_array) > 1 else 0.5
    y_extent = abs(max_y - min_y) * 0.5 if len(coords_array) > 1 else 0.5

    extent = min(x_extent, y_extent)

    bottom_left = []
    upper_right = []

    if len(bbox) == 0:
        bottom_left = [min_x - extent, min_y - extent]
        upper_right = [max_x + extent, max_y + extent]
    else:
        bottom_left = bbox[0:2]
        upper_right = bbox[2:4]
        if (
            min_x < bottom_left[0]
            or min_y < bottom_left[1]
            or max_x > upper_right[0]
            or max_y > upper_right[1]
        ):
            raise Exception(
                'Invalid operation: Points should be within the bounding box supplied '
                + str(bbox)
                + '.'
            )

    bound_poly = [
        bottom_left,
        [bottom_left[0], upper_right[1]],
        upper_right,
        [upper_right[0], bottom_left[1]],
        bottom_left,
    ]

    if voronoi_type == 'poly':
        # Complete the diagram with some extra points
        # to construct polygons with infinite ridges
        coords.append((-180, -85))
        coords.append((180, -85))
        coords.append((-180, 85))
        coords.append((180, 85))

    vor = Voronoi(coords)
    vor_vertices = vor.vertices

    if voronoi_type == 'lines':
        center = vor.points.mean(axis=0)
        ptp_bound = vor.points.ptp(axis=0)
        lines = []
        for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
            simplex = np.asarray(simplex)
            if np.all(simplex >= 0):
                clipped_list = lib.clip_segment_bbox(
                    vor.vertices[simplex].tolist(), bottom_left, upper_right
                )

                if len(clipped_list) > 1:
                    lines.append(clipped_list)
            else:
                # finite end Voronoi vertex
                i = simplex[simplex >= 0][0]

                # direction
                d = vor.points[pointidx[1]] - vor.points[pointidx[0]]
                d /= np.linalg.norm(d)

                # normal
                n = np.array([-d[1], d[0]])

                # compute extension
                midpoint = vor.points[pointidx].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = vor.vertices[i] + direction * ptp_bound.max()

                vertices_list = [vor.vertices[i].tolist()]
                vertices_list.append(far_point.tolist())
                clipped_list = lib.clip_segment_bbox(
                    vertices_list, bottom_left, upper_right
                )

                if len(clipped_list) > 1:
                    lines.append(clipped_list)

        return geojson.MultiLineString(lines, precision=PRECISION)

    else:
        lines = []
        for region in vor.regions:
            if -1 not in region and len(region) > 0:
                region.append(region[0])
                point_list = [list(vor_vertices[p]) for p in region]
                clipped_list = lib.polygon_polygon_intersection(point_list, bound_poly)
                lines.append([clipped_list])

        return geojson.MultiPolygon(lines, precision=PRECISION)
