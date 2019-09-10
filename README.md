# loc_finder
中国地名结构化，不包括港澳台，考虑拼音表示地名的情况
```shell
>>> from loc_finder import Finder
>>> finder = Finder()
>>> finder.find_loc("beijing PRC")
('中国', ['北京'], ['北京'])
```
`province_code_dict`:省份对应编码，需要的直接把结果放入dict中即可  
`city_code_dict`:城市对应编码，需要的直接把结果放入dict中即可  
特殊城市说明:"吉安"拼音为"jian"，会被很多城市或省份的拼音包含，所以特殊处理当有两个以上城市时只有省份包含吉安所在省份才放入吉安, "吉林"省和市同名，特殊处理，“阿里”的拼音太广泛，特殊处理
***
不完善的地方共同提高
