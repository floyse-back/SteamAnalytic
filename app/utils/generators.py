from typing import Tuple


def key_generator_args_and_kwargs(args_list:Tuple,kwargs_list:dict):
    type_tuple = (
        str,
        int,
        float,
        bool,
        type(None),  # None
        list,
        tuple,
        dict,
    )
    new_args_list = []
    for arg in args_list:
        if isinstance(arg,type_tuple):
            new_args_list.append(arg)

    new_kwargs_list = []
    for kwarg in kwargs_list.values():
        if isinstance(kwarg,type_tuple):
            new_kwargs_list.append(kwarg)

    return new_args_list, new_kwargs_list
