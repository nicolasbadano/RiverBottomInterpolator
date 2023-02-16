# RiverBottomInterpolator

This code allows interpolating partial river bathymetry points to the entire domain, taking into account the anisotropy of longitudinal and lateral bottom vaiations.

## Getting Started

* Change directory into one of the example folders

```bash
cd Examples/CDD
```

* Run the script

```bash
python3 ../../riverBottomInterpolator.py
```

* Inpect the input and output files geojson files using QGIS or other GIS software.

## Parameters

All the parameters for the interpolation are read from the `parameters.json` file in the current folder. For example:

```python
{
    # [Input] Name of the geojson file containing the cross sections that define
    # the river outline
    "cross_section_file_name": "cross_sections.geojson",

    # [Input] Name of the numeric field that defines the order of the cross
    # sections; can be float or integer
    "cross_section_order_field_name": "s",

    # [Input] Name of the geojson file containing the bottom elevation surveyed
    # points
    "points_file_name": "depth_points.geojson",

    # [Input] Name of the numeric field that defines the elevation of the bottom
    # on the surveyed point
    "points_z_field_name": "z",

    # [Input] Rate of lateral variability to longitudinal variability
    "anisotropy": 20.0,
    
    # [Input] Interpolation method
    "interpolation_method": "IDW",
   
    # [Input] Number of neighbours for the IDW method
    "IDW_num_neighbours": 12,
   
     # [Input] Power of distance for the IDW method
    "IDW_power": 1,

    # [Input] Desired average output resolution, in meters
    "dx": 5.0,

    # [Ouput] Name of the geojson file containing the river outline
    "river_outline_file_name": "river_outline.geojson",

    # [Ouput] Name of the geojson file containing the interpolated points
    "results_file_name": "interpolated_points.geojson"
}
```

All the input geojson files need to have **the same projected coordinate system**.

## How it works

The algorithm works a following:

- It reads a number of cross section segments that define the extent, and orientation of the river reach.

- It then creates a conformal grid of points following that outlines, with the desired resolution

- The conformal grid acts as a map between a cartesian rectangular space and the geometry in geographical coordinates.

- The surveyed points are transformed into the cartesian rectangular space.

- Interpolation is calculated on the cartesian rectangular space. Currently only Inverse Distance Weighted interpolation is supported, but it's easy to adapt any other interpolation technique, such a Krigging.

- Points on the cartesian space are exported with their original geographical coordinates


## Requirements

* Python 3
* Numpy

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Author

Nicolás Diego Badano (https://www.linkedin.com/in/nicolas-diego-badano/)
