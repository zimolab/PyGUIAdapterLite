class bool_t(int):
    pass


class text_t(str):
    pass


class int_r(int):
    pass


class int_s(int):
    pass


class int_ss(int):
    pass


class float_r(float):
    pass


class float_s(float):
    pass


class float_ss(float):
    pass


class file_t(str):
    pass


class dir_t(str):
    pass


directory_t = dir_t


class choice_t(object):
    pass


loose_choices_t = choice_t


class choices_t(list):
    pass


class color_t(object):
    pass


class color_tuple_t(tuple):
    pass


class color_hex_t(str):
    pass


class key_sequence_t(str):
    pass


class string_list_t(list):
    pass


str_list = string_list_t
string_list = string_list_t


class path_list_t(list):
    pass


path_list = path_list_t
paths_t = path_list_t


class dirs_t(list):
    pass


dir_list_t = dirs_t


class files_t(list):
    pass


file_list_t = files_t


class plain_dict_t(dict):
    pass


class json_obj_t(object):
    pass


class font_t(str):
    pass


class string_dict_t(dict):
    pass
