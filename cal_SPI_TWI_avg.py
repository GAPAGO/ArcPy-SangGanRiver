import arcpy
import csv
import time
from tqdm import tqdm
from arcpy import management
from arcpy.sa import ZonalStatisticsAsTable

arcpy.env.workspace = r'E:\03Project\Arcgis\SGHClassifier.gdb'  # 设置工作空间
arcpy.ClearWorkspaceCache_management()
arcpy.env.parallelProcessingFactor = "0"
arcpy.env.overwriteOutput = True


def calculate_average_with_summarize_raster_within(spi_raster: str,
                                                   twi_raster: str,
                                                   feature_class: str,
                                                   output_csv: str):
    """

    :param spi_raster:
    :param twi_raster:
    :param feature_class:
    :param output_csv:
    :return:
    """
    start_time = time.time()

    # 为了 ZonalStatisticsAsTable 函数的输入要求，需要增加一列用来唯一识别（分类用）需要统计的要素类，且字段为整型或字符串
    fields = [field.name for field in arcpy.ListFields(feature_class)]
    if "FID_1_INT" not in fields:
        # 请关闭 Cells 属性表，否则无法编辑
        arcpy.AddField_management(feature_class, "FID_1_INT", "LONG")
        arcpy.CalculateField_management(feature_class, "FID_1_INT", "!FID_1!", "PYTHON3")
    """
    for field in fields:
        print(f"Field name: {field.name}, Field type: {field.type}")
    """
    # 计算 spi_raster 在 feature_class 边界内的平均值
    spi_summary_table = ZonalStatisticsAsTable(in_zone_data=feature_class,
                                               zone_field="FID_1_INT",
                                               in_value_raster=spi_raster,
                                               out_table="spi_summary",
                                               statistics_type="MEAN")
    # 计算 twi_raster 在 feature_class 边界内的平均值
    twi_summary_table = ZonalStatisticsAsTable(in_zone_data=feature_class,
                                               zone_field="FID_1_INT",
                                               in_value_raster=twi_raster,
                                               out_table="twi_summary",
                                               statistics_type="MEAN")
    # 将两个统计表连接起来
    arcpy.management.JoinField(spi_summary_table, "OBJECTID", twi_summary_table, "OBJECTID", ["MEAN"])
    arcpy.management.JoinField(spi_summary_table, "OBJECTID", feature_class, "OBJECTID", ["Cell_Index", "Mesh_Name"])
    """
    spi_fields = [field.name for field in arcpy.ListFields(spi_summary_table)]
    print(spi_fields)

    cursor = arcpy.SearchCursor(spi_summary_table, spi_fields)
    for row in cursor:
        values = [row.getValue(field) for field in spi_fields]
        print(values)
    del cursor
    """
    # 创建 csv 文件并写入列名
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['OBJECTID', 'Cell_Index', 'Mesh_Name', 'SPI_Avg', 'TWI_Avg']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 遍历 summary_table 中的每一行
        cursor = arcpy.SearchCursor(spi_summary_table)
        for row in tqdm(cursor, colour='red'):
            object_id = row.getValue('OBJECTID')
            cell_index = row.getValue('Cell_Index')
            mesh_name = row.getValue('Mesh_Name')
            spi_avg = row.getValue('MEAN')
            twi_avg = row.getValue('MEAN_1')

            # 写入 csv 文件
            writer.writerow({
                'OBJECTID': object_id,
                'Cell_Index': cell_index,
                'Mesh_Name': mesh_name,
                'SPI_Avg': spi_avg,
                'TWI_Avg': twi_avg
            })
        del cursor

    end_time = time.time()
    print(f"cal_SPI_TWI Execution Time is {end_time - start_time} seconds")


calculate_average_with_summarize_raster_within("SPI",
                                               "TWI",
                                               "Floodplain_shape\Cells",
                                               r"D:\ShenZeyu20230308\ArcPy_SangGanHe\calculated table\SPI_TWI_avg.csv")
