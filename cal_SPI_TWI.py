import arcpy
import time
import numpy as np
from math import pi
from arcpy.sa import FlowDirection, FlowAccumulation, Slope
from arcpy.sa import Ln, Tan, Con

# 设置工作空间
arcpy.env.workspace = r"D:\ShenZeyu20220913\02RS Image Verification\GF2\ArcGIS\Result.gdb"
arcpy.ClearWorkspaceCache_management()
arcpy.env.parallelProcessingFactor = "0"

# 设置输入文件路径
dem_filled = "Fill_SGH_DEM"  # 填方后的 DEM

# Get the minimum x and y coordinates of the input raster
x_min = arcpy.GetRasterProperties_management(dem_filled, "LEFT")
y_min = arcpy.GetRasterProperties_management(dem_filled, "BOTTOM")

# Set the x and y coordinates of the point
x_coord = float(x_min.getOutput(0))
y_coord = float(y_min.getOutput(0))

# Create a point object
point = arcpy.Point(x_coord, y_coord)

# 设置输出文件路径
out_gdb = r"E:\03Project\Arcgis\SGHClassifier.gdb"


def cal_SPI_TWI(dem: str, out_put_path: str):
    """
    计算水流强度指数和地形湿度指数
    :param dem: 填方后的数字地形
    :param out_put_path: 输出文件路径
    :return: 两个栅格文件
    """
    start_time = time.time()

    flow_direction = FlowDirection(dem)
    # flow_direction.save(r"D:\ShenZeyu20220913\02RS Image Verification\GF2\ArcGIS\Result.gdb\flowdir")

    flow_accumulation = FlowAccumulation(flow_direction)
    # flow_accumulation.save(r"D:\ShenZeyu20220913\02RS Image Verification\GF2\ArcGIS\Result.gdb\flowacc")

    # Convert flow accumulation and flow direction rasters to numpy arrays
    flow_accumulation_np = arcpy.RasterToNumPyArray(flow_accumulation)
    flow_direction_np = arcpy.RasterToNumPyArray(flow_direction)

    # Calculate sca using numpy array operations
    sca_np = np.where(flow_accumulation_np == 0, 1, flow_accumulation_np) * 0.25 / np.where(
        np.isin(flow_direction_np, [1, 4, 16, 64]), 0.5,
        np.where(np.isin(flow_direction_np, [2, 8, 32, 128]), 0.5 * np.sqrt(2), 1))

    # Convert sca numpy array back to raster
    sca = arcpy.NumPyArrayToRaster(sca_np, lower_left_corner=point, x_cell_size=0.5, y_cell_size=0.5)

    slope_radians = Slope(dem) * pi / 180
    """
    assign the value of to itself where it is not equal to 0 and 
    assign the value of 0.00001 where it is equal to 0.slope_radians
    """
    slope_radians = Con(slope_radians != 0, slope_radians, 0.00001)

    spi = Ln(sca * Tan(slope_radians))
    twi = Ln(sca / Tan(slope_radians))

    spi.save(f"{out_put_path}\\SPI")
    twi.save(f"{out_put_path}\\TWI")
    sca.save(f"{out_put_path}\\SCA")

    """
    # Split spi raster into smaller rasters
    # arcpy.SplitRaster_management(spi, out_put_path, "SPI_", "NUMBER_OF_TILES", "GRID", "#", "2 2")
    # arcpy.SplitRaster_management(twi, out_put_path, "TWI_", "NUMBER_OF_TILES", "GRID", "#", "2 2")
    """

    end_time = time.time()
    print(f"cal_SPI_TWI Execution Time is {end_time - start_time} seconds")


def main():
    cal_SPI_TWI(dem_filled, out_gdb)


if __name__ == "__main__":
    main()
