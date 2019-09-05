import json

import datetime

import numpy as np
from psycopg2._psycopg import Decimal


class MsSqlResultDataEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        return super(MsSqlResultDataEncoder, self).default(obj)

def points_list(str):
    pp=str.split(',')
    pplist=[]
    tmp1=[]
    for i in range(len(pp)):
        tmp1.append(int(pp[i]))
        if i%2 :
            t3=tuple(tmp1)
            print(t3)
            tmp1 = []
            pplist.append(t3)
    return pplist

def get_center_point(pointslist):
    x_list=[]
    y_list=[]
    for point in pointslist:
          x_list.append(point[0])
          y_list.append(point[1])

    c_x=int(np.mean(x_list)*0.98)
    c_y=int(np.mean(y_list))
    return (c_x,c_y)
