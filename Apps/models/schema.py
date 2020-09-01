# # -*- coding: utf-8 -*-
#
# from flasgger import Schema, fields
#
#
# class IdentSchema(Schema):
#     ident = fields.Str()
#
#
# class IdSchema(Schema):
#     id = fields.Int()
#
#
# class PlotIDSchema(Schema):
#     plot_id = fields.Int()
#
#
# class DeviceIDSchema(Schema):
#     device_id = fields.Int()
#
#
# class QPageSchema(Schema):
#     """
#     parameters:
#       - name: page
#         in: query
#         type: integer
#         description: input page num
#     """
#     page = fields.Int()
#
#
# class Page(QPageSchema):
#     status = fields.Int()
#     msg = fields.Str()
#     pages = fields.Int()
#     total = fields.Int()
#     has_prev = fields.Bool()
#     has_next = fields.Bool()
#
#
# class QTimeSchema(QPageSchema):
#     start_time = fields.DateTime()
#     end_time = fields.DateTime()
#     delta_time = fields.Int()
#     page = fields.Int()
#     type_time = fields.Str()
#
#
# class QPLandIDSchema(QPageSchema, PlotIDSchema):
#     pass
#
#
# class QIPSchema(QPageSchema, IdentSchema):
#     pass
#
#
# class QTPLandIDSchema(QTimeSchema, PlotIDSchema):
#     pass
#
#
# class BasicLayerSchema(Schema):
#     layer_type = fields.Str()
#     layer_path = fields.Str()
#     land_id = fields.Int()
#     layer_name = fields.Str()
#
#
# class QILayerSchema(IdentSchema, BasicLayerSchema):
#     pass
#
#
# class LayerSchema(Schema):
#     id = fields.Str()
#     layer_type = fields.Str()
#     layer_path = fields.Str()
#     land_id = fields.Int()
#     layer_name = fields.Str()
#
#
# class LayersSchema(Page):
#     data = fields.Nested(LayerSchema, many=True)
#
#
# class AdminUserSchema(Schema):
#     id = fields.Int()
#     username = fields.Str()
#     is_deleted = fields.Bool()
#     is_super = fields.Bool()
#     permission = fields.Int()
#     join_time = fields.DateTime()
#
#
# class AdminUsersSchema(Page):
#     data = fields.Nested(AdminUserSchema, many=True)
#
#
# class TokenSchema(Schema):
#     token = fields.Str()
#
#
# class BasicDeviceSchema(Schema):
#     device_num = fields.Int()
#     net_id = fields.Int()
#     slave_index = fields.Int()
#     longitude = fields.Str()
#     latitude = fields.Str()
#     altitude = fields.Str()
#     join_time = fields.DateTime()
#     device_land_id = fields.Int()
#
#
# class DeviceSchema(BasicDeviceSchema):
#     id = fields.Int()
#
#
# class QIDeviceSchema(BasicDeviceSchema):
#     ident = fields.Str()
#
#
# class DevicesSchema(Page):
#     data = fields.Nested(DeviceSchema, many=True)
#
#
# class BasicIOTDatumSchema(Schema):
#     device_num = fields.Int()
#     net_id = fields.Int()
#     slave_index = fields.Int()
#     longitude = fields.Str()
#     latitude = fields.Str()
#     altitude = fields.Str()
#     device_land_id = fields.Int()
#     value = fields.Str()
#     time = fields.DateTime()
#
#
# class IOTDatumSchema(BasicIOTDatumSchema):
#     id = fields.Int()
#
#
# class IOTDataSchema(Page):
#     data = fields.Nested(IOTDatumSchema, many=True)
#
#
# class QTIOTDataSchema(QTimeSchema, PlotIDSchema, DeviceIDSchema):
#     pass
#
#
# # class QIIOTDatumSchema(IdentSchema, IOTDatumSchema):
# #     pass
#
# class BasicLandSchema(Schema):
#     land_name = fields.Str()
#     latitude = fields.Str()
#     longitude = fields.Str()
#     altitude = fields.Str()
#     land_crop_id = fields.Int()
#
#
# class LandSchema(BasicLandSchema):
#     id = fields.Int()
#
#
# class LandsSchema(Page):
#     data = fields.Nested(LandSchema, many=True)
#
#
# class QTLandSchema(QTimeSchema):
#     ident = fields.Int()
#
#
# class QILandSchema(BasicLandSchema, IdentSchema):
#     pass
#
#
# class BasicCropSchema(Schema):
#     crop_name = fields.Str()
#     seeding_time = fields.DateTime()
#     fertilizing_time = fields.DateTime()
#     fertilizing_amount = fields.Int()
#     pesticide_time = fields.DateTime()
#     pesticide_amount = fields.Int()
#     pesticide_type = fields.Str()
#     describe = fields.Str()
#     join_time = fields.DateTime()
#
#
# class CropSchema(BasicCropSchema):
#     id = fields.Int()
#
#
# class CropsSchema(Page):
#     data = fields.Nested(CropSchema, many=True)
#
#
# # class QTLandIDCropSchema(QTimeSchema, LandIDSchema):
# #     pass
#
# class QICropSchema(BasicCropSchema, IdentSchema):
#     pass
#
#
# class WeatherSchema(Schema):
#     id = fields.Int()
#     station_id = fields.Str()
#     join_time = fields.DateTime
#     prs = fields.Float
#     prs_sea = fields.Float
#     prs_max = fields.Float
#     prs_min = fields.Float
#     tem = fields.Float
#     tem_max = fields.Float
#     tem_min = fields.Float
#     rhu = fields.Int()
#     rhu_Min = fields.Int()
#     vap = fields.Float
#     pre_1h = fields.Float
#     win_d_inst_max = fields.Int()
#     win_s_max = fields.Float
#     win_d_s_max = fields.Int()
#     win_s_avg_2mi = fields.Float
#     win_d_avg_2mi = fields.Int()
#     wep_now = fields.Int()
#     win_s_inst_Max = fields.Float
#     tem_apparent = fields.Float
#     wind_power = fields.Int()
#     vis = fields.Float
#     clo_cov = fields.Int()
#     clo_cov_Low = fields.Int()
#     clo_cov_lm = fields.Int()
#
#
# class WeatherListSchema(Page):
#     data = fields.Nested(WeatherSchema, many=True)
