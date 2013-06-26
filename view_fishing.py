# -*- coding: utf-8 -*-

from flask import request
from utils import ProtocolTypes, ResultCodes, checkSessionId, checkContainKeys
import json

from database import db_session
from sqlalchemy import exc
from models import Fishing, PirateShip


def getFishing():
    result = {'type': ProtocolTypes.GetFishing}

    if request.method == 'POST' and request.form['data']:
        got_data = json.loads(request.form['data'])
        from_keys = ['session_id', 'zone_index']
        if checkContainKeys(from_keys, got_data):
            result['result'], got_user = checkSessionId(got_data['session_id'])

            if got_user:
                find_fishing = Fishing.query.filter_by(zone_index=got_data['zone_index']).first()
                if find_fishing:
                    import random
                    got_random_rate = random.random() * 100
                    got_rate_list = [
                        find_fishing.no_item, find_fishing.general_ship_rate, find_fishing.special_ship_rate,
                        find_fishing.item_rate_1, find_fishing.item_rate_2, find_fishing.item_rate_3,
                        find_fishing.item_rate_4, find_fishing.item_rate_5, find_fishing.item_rate_6,
                        find_fishing.item_rate_7, find_fishing.item_rate_8, find_fishing.item_rate_9,
                        find_fishing.item_rate_10, find_fishing.item_rate_11, find_fishing.item_rate_12,
                        find_fishing.item_rate_13
                    ]
                    if got_random_rate < sum(got_rate_list[:1]):
                        result['item_index'] = ''
                    elif got_random_rate < sum(got_rate_list[:2]):
                        result['item_index'] = find_fishing.general_ship_index
                        made_ship = PirateShip(got_user.id)
                        made_ship.hp = 200
                        db_session.add(made_ship)
                        try:
                            db_session.commit()
                        except exc.SQLAlchemyError:
                            result['result'] = ResultCodes.DBInputError
                    elif got_random_rate < sum(got_rate_list[:3]):
                        result['item_index'] = find_fishing.special_ship_index
                        made_ship = PirateShip(got_user.id)
                        made_ship.hp = 400
                        made_ship.type = 's'
                        db_session.add(made_ship)
                        try:
                            db_session.commit()
                        except exc.SQLAlchemyError:
                            result['result'] = ResultCodes.DBInputError
                    elif got_random_rate < sum(got_rate_list[:4]):
                        result['item_index'] = find_fishing.item_index_1
                        result['item_count'] = find_fishing.item_count_1
                    elif got_random_rate < sum(got_rate_list[:5]):
                        result['item_index'] = find_fishing.item_index_2
                        result['item_count'] = find_fishing.item_count_2
                    elif got_random_rate < sum(got_rate_list[:6]):
                        result['item_index'] = find_fishing.item_index_2
                        result['item_count'] = find_fishing.item_count_2
                    elif got_random_rate < sum(got_rate_list[:7]):
                        result['item_index'] = find_fishing.item_index_3
                        result['item_count'] = find_fishing.item_count_3
                    elif got_random_rate < sum(got_rate_list[:8]):
                        result['item_index'] = find_fishing.item_index_4
                        result['item_count'] = find_fishing.item_count_4
                    elif got_random_rate < sum(got_rate_list[:9]):
                        result['item_index'] = find_fishing.item_index_5
                        result['item_count'] = find_fishing.item_count_5
                    elif got_random_rate < sum(got_rate_list[:10]):
                        result['item_index'] = find_fishing.item_index_6
                        result['item_count'] = find_fishing.item_count_6
                    elif got_random_rate < sum(got_rate_list[:11]):
                        result['item_index'] = find_fishing.item_index_7
                        result['item_count'] = find_fishing.item_count_7
                    elif got_random_rate < sum(got_rate_list[:12]):
                        result['item_index'] = find_fishing.item_index_8
                        result['item_count'] = find_fishing.item_count_8
                    elif got_random_rate < sum(got_rate_list[:13]):
                        result['item_index'] = find_fishing.item_index_9
                        result['item_count'] = find_fishing.item_count_9
                    elif got_random_rate < sum(got_rate_list[:14]):
                        result['item_index'] = find_fishing.item_index_10
                        result['item_count'] = find_fishing.item_count_10
                    elif got_random_rate < sum(got_rate_list[:15]):
                        result['item_index'] = find_fishing.item_index_11
                        result['item_count'] = find_fishing.item_count_11
                    elif got_random_rate < sum(got_rate_list[:16]):
                        result['item_index'] = find_fishing.item_index_12
                        result['item_count'] = find_fishing.item_count_12
                    else:
                        result['item_index'] = find_fishing.item_index_13
                        result['item_count'] = find_fishing.item_count_14
                else:
                    result['result'] = ResultCodes.NoData
        else:
            result['result'] = ResultCodes.InputParamError
    else:
        result['result'] = ResultCodes.AccessError

    return str(json.dumps(result))


getFishing.methods = ['POST']