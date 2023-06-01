import arcpy
from arcpy import env
import os
from simpledbf import Dbf5

# 设置工作空间
env.workspace = "E:/03Project/Arcgis/SGHClassifier.gdb"

# 设置输出文件夹
out_folder = "D:/ShenZeyu20230308/ArcPy_SangGanHe/attribute table"

# 检查输出文件夹是否存在，如果不存在则创建它
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# 获取工作空间中的所有要素类
fcs = arcpy.ListFeatureClasses()

# 遍历所有要素类
for fc in fcs:
    # 获取要素类名称
    fc_name = arcpy.Describe(fc).name
    # 设置.dbf文件路径
    dbf_file = os.path.join(out_folder, fc_name + ".dbf")
    # 导出.dbf文件
    arcpy.TableToTable_conversion(fc, out_folder, fc_name + ".dbf")
    # 读取.dbf文件
    dbf = Dbf5(dbf_file)
    df = dbf.to_dataframe()
    # 设置.csv文件路径
    csv_file = os.path.join(out_folder, fc_name + ".csv")
    # 保存.csv文件
    df.to_csv(csv_file, index=False)
