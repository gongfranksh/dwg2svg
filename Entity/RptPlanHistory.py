# -*- coding: utf-8 -*-
from .BNMsSqlEproject import bnmssqleproject


class RptPlanHistory(bnmssqleproject):

    def __init__(self):
        bnmssqleproject.__init__(self)

    def get_all(self,procdate):
        sql ="""
            SELECT
                a.*,
                a.decSimpleShopPrice / a.plan_count_qty AS per_day_decSimpleShopPrice,
                a.decRealFactPrice / a.plan_count_qty AS per_day_decRealFactPrice,
            CASE
                
                WHEN a.contract_day <> 0 THEN
                a.lngRealTotalMoney / a.contract_day ELSE 0 
                END per_day_lngRealTotalMoney,
                isnull(
                CASE
                        
                        WHEN ( a.decSimpleShopPrice - a.decRealFactPrice ) >= 0 THEN
                        ( a.decSimpleShopPrice - a.decRealFactPrice ) / a.plan_count_qty 
                    END,
                    0 
                ) per_day_loss,
                isnull(
                CASE
                        
                        WHEN ( a.decSimpleShopPrice - a.decRealFactPrice ) < 0 THEN
                        ( a.decRealFactPrice - a.decSimpleShopPrice ) / a.plan_count_qty 
                    END,
                    0 
                ) per_day_more_profit,
                 isnull(
                CASE
                        
                        WHEN ( a.plan_count_qty ) <> 0 THEN
                        ( a.decSimpleShopPrice - a.decRealFactPrice ) / a.plan_count_qty 
                    END,
                    0 
                ) per_day_loss_total
            FROM
                (
                SELECT
                    esh.dtdate,
                    pmshop.strShopName,
                    plantype.strItemName AS strplantype,
                    resourcetype.strItemName AS strresourcetype,
                    esh.lngshopid,
                    esh.strFloor,
                    esh.strResourceCode,
                    esh.strPlaceGradeName,
                    unittype.strItemName,
                    esh.lngPlanTypeID,
                    esh.lngResourceType,
                    isnull( esh.decAreaQuantity, 0 ) decAreaQuantity,
                    isnull( esh.decSimpleShopPrice, 0 ) decSimpleShopPrice,
                    isnull( decRealFactPrice, 0 ) decRealFactPrice,
                    isnull( esh.lngRealTotalMoney, 0 ) lngRealTotalMoney,
                    esh.strBusinessName,
                    esh.dtBegin,
                    esh.dtEnd,
                    isnull( datediff( DAY, dtBegin, dtEnd ), 0 ) AS contract_day,
                    ( 32- DAY ( dtdate + 32- DAY ( dtdate ) ) ) AS month_day,
                CASE
                        Pm_Plan.lngUnitID 
                        WHEN 1 THEN
                        1 
                        WHEN 2 THEN
                        ( 32- DAY ( dtdate + 32- DAY ( dtdate ) ) ) 
                        WHEN 3 THEN
                        365 ELSE NULL 
                    END AS plan_count_qty, 
                     isnull(esh.strPlanID,'') strPlanID ,
                     isnull(esh.strBusinessID,'') strBusinessID,
                     isnull(esh.strContractID,'') strContractID
                FROM
                    E_SeatPlanAndHireInfo_History esh
                    LEFT JOIN NewPlaza.dbo.Pm_Shop pmshop ON esh.lngshopid = pmshop.lngshopid
                    LEFT JOIN Pm_Enum plantype ON esh.lngPlanTypeID = plantype.lngItemValue
                    LEFT JOIN ( SELECT strItemName, lngItemValue FROM Pm_Enum WHERE lngEnumTypeID = 3 ) resourcetype ON esh.lngResourceType = resourcetype.lngItemValue
                    LEFT JOIN NewPlaza.dbo.Pm_Plan Pm_Plan ON esh.strPlanID = Pm_Plan.strPlanID
                    INNER JOIN ( SELECT strItemName, lngItemValue FROM Pm_Enum WHERE lngEnumTypeID = 4 ) unittype ON Pm_Plan.lngUnitID = unittype.lngItemValue 
                WHERE
                        plantype.lngEnumTypeID = 8 
                    AND esh.lngResourceType NOT IN ( '301' ) 
                    AND datediff( DAY, dtdate, '{0}' ) = 0 
                ) a 
            ORDER BY
                dtdate,
            lngShopID 
       """
        sql=sql.format(procdate)
        # print(sql)
        rst = self.get_remote_result_by_sql(sql)
        return rst

    def get_record_count(self, procdate):
        sql = """
                SELECT
                  count(*) as cnt
                FROM
                    E_SeatPlanAndHireInfo_History esh
                WHERE    
                        esh.lngResourceType NOT IN ( '301' ) 
                    AND datediff( DAY, dtdate, '{0}' ) = 0 
       """
        sql = sql.format(procdate)
        # print(sql)
        rst = self.get_remote_result_by_sql(sql)
        if len(rst)==1:
            return rst[0]['cnt']
        else:
            return 0

        # return rst

