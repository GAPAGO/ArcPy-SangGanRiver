import arcpy
import os
from arcpy.sa import ExtractByMask
from tqdm import tqdm

# 设置工作空间
arcpy.env.workspace = r"D:\ShenZeyu20220913\02RS Image Verification\GF2\ArcGIS\SangGanHe.gdb"
arcpy.ClearWorkspaceCache_management()
arcpy.env.parallelProcessingFactor = "0"
arcpy.env.overwriteOutput = True

# 设置输出文件路径
out_gdb = r"D:\ShenZeyu20220913\02RS Image Verification\GF2\ArcGIS\Result.gdb"

# 输入栅格数据文件A
in_raster = "UAV"

# 输入shp文件
in_shp = "Fp_Face_HECRAS"

# 遍历shp文件中的每个面要素
rows = arcpy.SearchCursor(in_shp)
for row in tqdm(rows):
    # 获取当前面要素的ID
    mask_id = row.getValue("Fp_ID")
    # 获取当前面要素的几何形状
    mask_geom = row.getValue("Shape")
    # 使用当前面要素作为掩膜范围提取栅格数据文件A
    out_raster = ExtractByMask(in_raster, mask_geom)
    # 输出结果
    out_raster.save(os.path.join(out_gdb, "UAV_Fp_A_{}".format(mask_id)))
