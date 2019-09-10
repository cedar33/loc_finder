import zhconv
import pypinyin
import pickle
import re

def get_loc_dict():
    with open("data/loc_dict.pkl", "rb") as f:
        loc_dict = pickle.load(f)
    return loc_dict

class Finder():
    def __init__(self):
        self.loc_dict = get_loc_dict()
        self.city_regex, self.city_py_regex = self.get_regex("city")
        self.province_regex, self.province_py_regex = self.get_regex("province")
        self.nation_regex = re.compile("|".join(self.loc_dict["nation"]))
        self.city_word_list = [city[0] for city in self.loc_dict["city"]]
        self.city_pinyin_list = ["".join(pypinyin.lazy_pinyin(c)) for c in self.city_word_list]
        self.city_code_dict = {city[0]: city[1] for city in self.loc_dict["city"]}
        self.province_word_list = [province[0] for province in self.loc_dict["province"]]
        self.province_pinyin_list = ["".join(pypinyin.lazy_pinyin(p)) for p in self.province_word_list]
        self.province_code_dict = {province[0]: province[1] for province in self.loc_dict["province"]}
        self.city_province_dict = self.get_city_province_dict()
        self.province_code_dict["重庆"] = "50"
        self.province_code_dict["北京"] = "11"
        self.province_code_dict["天津"] = "12"
        self.province_code_dict["上海"] = "31"


    def get_regex(self, loc_type):
        loc_list = []
        loc_py_list = []
        for _type in self.loc_dict[loc_type]:
            loc_list.append(_type[0])
            loc_py_list.append("".join(pypinyin.lazy_pinyin(_type[0])))
        loc_regex = re.compile("|".join(loc_list))
        loc_py_regex = re.compile("|".join(loc_py_list))
        return loc_regex, loc_py_regex

    def get_city_province_dict(self):
        city_province_dict = {}
        for city in self.loc_dict["city"]:
            for province in self.loc_dict["province"]:
                if province[1] == city[1][0:2]:
                    city_province_dict[city[0]] = province[0]
        city_province_dict["北京"] = "北京"
        city_province_dict["天津"] = "天津"
        city_province_dict["上海"] = "上海"
        city_province_dict["重庆"] = "重庆"
        return city_province_dict

    def find_nation(self, text):
        result = re.findall(self.nation_regex, text)
        if len(result) > 0:
            return ["中国"]
        else:
            return []
    
    def find_province(self, text):
        result = re.findall(self.province_regex, text)
        result_py = re.findall(self.province_py_regex, text)
        if len(result_py) > 0:
            for r in result_py:
                result.append(self.province_word_list[self.province_pinyin_list.index(r)])
        return list(set(result))


    def find_city(self, text):
        result = re.findall(self.city_regex, text)
        result_py = re.findall(self.city_py_regex, text)
        if len(result_py) > 0:
            for r in result_py:
                result.append(self.city_word_list[self.city_pinyin_list.index(r)])
        return list(set(result))

    def find_loc(self, text):
        text = zhconv.convert(text, "zh-cn")
        text = text.lower()
        text = text.replace(" ", "")
        city = self.find_city(text)
        province = self.find_province(text)
        nation = self.find_nation(text)
        if len(city) > 1:
            if "吉安" in city:
                city.pop(city.index("吉安"))
            elif "吉林" in city and "吉林" in province:
                city.pop(city.index("吉林"))
            else:
                for c in city:
                    if self.city_province_dict[c] not in province:
                        city.pop(city.index(c))
            if len(city) > 1:
                city = [city[0]]
        if city.__contains__("阿里") and self.city_province_dict["阿里"] not in province:
            city = []
        if len(city) > 0:
            province = [self.city_province_dict[city[0]]]
        elif len(province) > 1:
            province = [province[-1]]
        if (len(province)+len(city)+len(nation)) > 0:
            nation = "中国"
            return (nation, province, city)
        else:
            return 0   
