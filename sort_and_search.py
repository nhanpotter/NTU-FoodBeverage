def search_by_food(foodname, foodcourt_list):
    __results = []
    for foodcourts in foodcourt_list:
        list1 = foodcourts.searchFoodByName(
            foodname)  # extracting each result out from the dict, because searchFoodByName function returns a list of dict
        for result in list1:
            __results.append(result)
    return __results


def search_by_price(min_price, max_price, foodcourt_list):
    __results = []
    for foodcourts in foodcourt_list:
        list1 = foodcourts.searchByPrice(min_price,
                                         max_price)  # extracting each result out from the dict, because searchByPrice function returns a list of dict.
        for result in list1:
            __results.append(result)
    return __results


def merge(left_list, right_list,key_name,reverse):
    result_list = []

    # while left and right list has elements
    while left_list and right_list:
        if reverse == False:
            if left_list[0][key_name] < right_list[0][key_name]:
                result_list.append(left_list[0])
                left_list.pop(0)
            else:
                result_list.append(right_list[0])
                right_list.pop(0)
        if reverse == True:
            if left_list[0][key_name] > right_list[0][key_name]:
                result_list.append(left_list[0])
                left_list.pop(0)
            else:
                result_list.append(right_list[0])
                right_list.pop(0)
    # left list still contain elements. Append its contents to end of the result list
    if left_list:
        result_list.extend(left_list)
    else:
        # right list still contain elements. Append its contents to end of the result list
        result_list.extend(right_list)

    return result_list


def mergesort(list_of_items, key_name,reverse):
    list_len = len(list_of_items)

    # base case
    if list_len < 2:
        return list_of_items
    left_list = list_of_items[:list_len // 2]  # //
    right_list = list_of_items[list_len // 2:]  # "//" to force division

    # merge sort left and right list recursively
    left_list = mergesort(left_list,key_name,reverse)
    right_list = mergesort(right_list,key_name,reverse)
    return merge(left_list, right_list,key_name,reverse)

# def sortBy(__result, key_name,sortBy):
#     __result = sorted(__result, key=lambda k: k[key_name],
#                       reverse=sortBy)  # sort the results according to price/ ratings
#     return __result


def search_by_category(user_food_category,foodcourt_list):
    __results = []
    for foodcourts in foodcourt_list:
        list1 = foodcourts.searchByCategory(
            user_food_category)  # extracting each result out from the dict, because searchByCategory function returns a list of dict.
        for result in list1:
            __results.append(result)
    return __results

def search_by_aircon_availability(list):
    __results = []
    for i in list:
        if i["Aircon Availability"] == "Yes":
            __results.append(i)
    return __results


def search_for_foodlist(user_fcname, user_stallname,foodcourt_list):
    __results = []
    for fc in foodcourt_list:
        if fc.name == user_fcname:
            stall = fc.getStallByName(user_stallname)
            list1 = stall.getFoods()
            for result in list1:
                __results.append(result)
    return __results

def intersection(list1,list2):
    __results =[]
    for i in list1:
        for j in list2:
            if i ==j:
                __results.append(i)
    return __results

def get_all_stalls(foodcourt_list):
    __results = []
    for fc in foodcourt_list:
        list1 = fc.getStalls()
        for i in list1:
            __results.append(i)
    return __results
def get_fc_name(user_input,foodcourt_list):
    __results = []
    for fc in foodcourt_list:
        if user_input.lower() in fc.name.lower():
            __results.append(fc)
    return __results

def update(new_price,new_rating,fc_name,stall_name,food_name,foodcourt_list):
    for fc in foodcourt_list:
        if fc_name.lower() == fc.name.lower():
            for stall in fc.stall_list:
                if stall_name.lower() == stall.name.lower():
                    for food in stall.food_list:
                        if food_name.lower() == food.name.lower():
                            food.price = new_price
                            food.rating = new_rating

def add(new_price,new_rating,fc_name,stall_name,food_name,foodcourt_list):
    for fc in foodcourt_list:
        if fc_name.lower() == fc.name.lower():
            fc.addFood(stall_name,food_name,new_price,new_rating)






