# -*- coding: utf-8 -*-
from .BNMsSqlEproject import bnmssqleproject

svg_size_width = 800
svg_size_height = 735

class PlanGis(bnmssqleproject):

    def __init__(self):
        bnmssqleproject.__init__(self)


    def get_shop_all(self):
        sql="""
                    SELECT
                        lngshopid,
                        strShopName,
                        strName 
                    FROM
                        E_Shop 
                    WHERE
                        lngShopID IN (
                        1000,	1001,	1216,	1006,	1029,	1031,	1044,	1063,	1071,	1109,	1259,
                        1233,	1241,	1265,	1291,	1288,	1321,	1390 	)        
        """

        # sql = sql.format()
        # print(sql)
        # rst = s
        return self.get_remote_result_by_sql(sql)


    def get_all(self,shopid):
        sql ="""
                    SELECT
                        * 
                    FROM
                        View_gisinfo_Table 
                    WHERE
                        shopid ={0}
                        AND floorno + versionseril IN (
                         SELECT floorno + versionseril 
                         FROM 
                         ( 
                         SELECT floorno, MAX ( versionseril ) versionseril 
                         FROM View_gisinfo_Table WHERE shopid = {0} GROUP BY floorno ) a ) 
                    ORDER BY
                        shopid,
                        floorno,
                        xiweibianhao
	       """
        sql=sql.format(shopid)
        # print(sql)
        rst = self.get_remote_result_by_sql(sql)
        tmp_rst=[]
        result=[]

        tmp_shopid=rst[0]['shopid']
        tmp_floorno=rst[0]['floorno']
        tmp_versionseril=rst[0]['versionseril']

        for r in rst:
            if r['imageheight'] is not None:
                tmp_height=r['imageheight']
            else:
                tmp_height=svg_size_height

            if r['imagewidth'] is not None:
                tmp_width=r['imagewidth']
            else:
                tmp_width=svg_size_width

            if r['shopid']==tmp_shopid and  r['floorno']==tmp_floorno and r['versionseril']==tmp_versionseril:
                tmp_rst.append(r)
            else:
                tmp_sub={'shopid':str(tmp_shopid),
                         'floorno':tmp_floorno,
                         'versionseril':tmp_versionseril,
                         'plan_gis_list':tmp_rst,
                         'height':tmp_height,
                         'width': tmp_width
                }
                result.append(tmp_sub)
                tmp_shopid = r['shopid']
                tmp_floorno = r['floorno']
                tmp_versionseril =  r['versionseril']
                tmp_rst=[]
                tmp_rst.append(r)

        tmp_sub = {'shopid': str(tmp_shopid), 'floorno': tmp_floorno, 'versionseril': tmp_versionseril,
                   'plan_gis_list': tmp_rst, 'height':tmp_height,
                         'width': tmp_width
                   }
        result.append(tmp_sub)

        return result

        # return rst

