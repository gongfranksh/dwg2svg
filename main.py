# -*- coding: utf-8 -*-
from BnPlanGisSvg import bn_floor_draw
from Entity.PlanGis import PlanGis


# def get_gis_data_from_eproject():
#     plangis=PlanGis()
#     return plangis.get_all(1044)

if __name__ == '__main__':
    plangis = PlanGis()
    shoplist= plangis.get_shop_all()
    for shop in shoplist:
        shopid=shop['lngshopid']
        floor_gis_list= plangis.get_all(shopid)
        for floor in floor_gis_list:
            bn_floor_draw(floor)
