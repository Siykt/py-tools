#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------
# 检查身份证工具
import time

index_code = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
verify_code = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
now_year = time.localtime().tm_year + 1


# 查询card信息
def checkIdCardLastRight(id_card):
    if type(id_card) == int:
        id_card = str(id_card)
    if len(id_card) != 18:
        return False

    count = 0
    for i, v in enumerate(index_code):
        try:
            count += v * int(id_card[i])
        except ValueError as err:
            return False
        if i == 16:
            vc = str(verify_code[count % 11])
            ic = id_card[-1:]
            if vc == ic.upper() or vc == ic:
                return True
            else:
                return False


# 遍历查询
def foreachRight(start_id, between_list, end_id):
    id_card_list = []
    for between_id in between_list:
        card = start_id + between_id + end_id
        state = checkIdCardLastRight(card)
        if state:
            id_card_list.append(card)

    return id_card_list


# 月份补全
def monthMissing():
    ROOMDER_MONTH = [str(x).zfill(2) for x in range(1, 13)]
    ROOMDER_DAY = [str(x).zfill(2) for x in range(1, 32)]
    CHECK_DAY = {
        '1': 31, '2': 29, '3': 31,
        '4': 30, '5': 31, '6': 30,
        '7': 31, '8': 31, '9': 30,
        '10': 31, '11': 30, '12': 31
    }
    between_list = []
    for month in ROOMDER_MONTH:

        for day in ROOMDER_DAY:
            between_id = month + day

            if (CHECK_DAY[str(int(month))] > (int(day) - 1)):
                between_list.append(between_id)

    return between_list


# 年份补全
def yeryMissing(beg_year=1900, end_yaer=now_year):
    return [str(x) for x in range(beg_year, end_yaer)]


# 年份+月份补全
def bigYeryMissing(month_list):
    year_list = yeryMissing()
    year_and_month_list = []

    def addYear(month, year):
        year_and_month_list.append(str(year) + month)

    start_input_year = 0
    end_input_year = now_year

    try:
        print('-------------------------------------------')
        start_input_year = int(input('开始年份: '))
    except:
        pass

    try:
        print('-------------------------------------------')
        end_input_year = int(input('结束年份: '))
    except:
        pass

    if start_input_year > 1900 and start_input_year < now_year:
        year_list = yeryMissing(start_input_year)
        if end_input_year >= start_input_year and end_input_year <= now_year:
            year_list = yeryMissing(start_input_year, end_input_year)

    if not len(year_list):
        year_and_month_list = [
            str(start_input_year) + month for month in month_list]
    else:
        year_and_month_list = [
            year + month for year in year_list for month in month_list]

    return year_and_month_list


# 反查身份证信息
def queryIdCard(idcard):
    start_index = idcard.find('*')
    end_index = idcard.rfind('*') + 1
    idcard_list = []
    error_str = '身份证错误或校验码为星号'
    if start_index < 0 or end_index == len(idcard):
        return error_str
    else:
        start_id = idcard[:start_index]
        end_id = idcard[end_index:]

    month_list = monthMissing()
    year_list = yeryMissing()

    # 年份补全
    if start_index == 6:
        if end_index == 10:
            return foreachRight(start_id, year_list, end_id)

        elif end_index == 14:
            print('数据量过大, 请尝试输入年份(默认为 start => 1900, end => now)')
            print('-------------------------------------------')
            return foreachRight(start_id, bigYeryMissing(month_list), end_id)

    # 月份补全
    if start_index == 10:
        if end_index == 14:
            return foreachRight(start_id, month_list, end_id)

    return ['Error: Not checking id-card']


def main():
    checking_idcard = input('反查身份号:  ')
    if not checking_idcard:
        print('请重新输入')
        return main()

    queryList = queryIdCard(checking_idcard)
    print('-------------------------------------------')
    print('结果列表 ->', queryList, '\n结果长度 ->', len(queryList))

if __name__ == "__main__":
    main()
