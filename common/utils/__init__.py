import linecache
import logging
import os
import sys

from flask import current_app

from .hr import hr

logger = logging.getLogger(__name__)


class ExceptionLogger:
    # http://stackoverflow.com/a/20264059/2422840
    @staticmethod
    def print_exception():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        error_details = 'EXCEPTION IN:\nFILE:{}\nLINE No. {}\nLINE:"{}"\nERROR:{}'.format(
            filename, lineno, line.strip(), exc_obj)
        print(error_details)
        hr('-')

    @staticmethod
    def log_exception(logger):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        error_details = 'EXCEPTION IN:\nFILE:{}\nLINE No. {}\nLINE:"{}"\nERROR:{}'.format(
            filename, lineno, line.strip(), exc_obj)
        logger.error(error_details)
        hr('-')

    @staticmethod
    def print_and_log_exception(logger):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        error_details = 'EXCEPTION IN:\nFILE:{}\nLINE No. {}\nLINE:"{}"\nERROR:{}'.format(
            filename, lineno, line.strip(), exc_obj)
        print(error_details)
        logger.error(error_details)
        hr('-')


def parse_request_dict(request_dict, params_map):
    """
    Parses a request & retrieves the parameters as per the params mapping
    :param request_dict: the request dictionary -- request.data or request.query_params.dict() or request.META
    :param params_map: the map for the arguments to be retrieved. Consists of tuples of structure
    (<param_name>, <param_type>, <default>)
    OR
    ((<param_from_name>, <param_to_name>), <param_type>, <default>)

    [
        ('store_id', int, None),
        (('product_price', 'price'), float, 0),
        ('order_date', DtOps.ist_datetime, None),
        ('store_name', str, '')
    ]

    If default is not defined in any tuple & the item is not found, it is not added to the resultant dictionary
    :return: the dict of params
    """
    result_params = {}
    if not isinstance(request_dict, dict):
        return result_params

    for param_map in params_map:
        if len(param_map) == 2:
            has_default = False
            param_default = None
            param_name, param_type = param_map
        else:
            has_default = True
            param_name, param_type, param_default = param_map

        if isinstance(param_name, tuple) or isinstance(param_name, list):
            to_name = param_name[1]
            param_name = param_name[0]
        else:
            to_name = param_name

        try:
            value = request_dict.get(param_name)
            if value is not None:
                result_params[to_name] = param_type(value)
            elif has_default:
                result_params[to_name] = param_default
        except:
            # Invalid data type passed in for parameter value. Skip value assignment
            ExceptionLogger.log_exception(logger)

    return result_params


def merge_lists(list_1, list_2, key):
    """
    https://mmxgroup.net/2012/04/12/merging-python-list-of-dictionaries-based-on-specific-key/
    list1 = [{'id':2 , 'name': 'majid'} , {'id':3 , 'name':'maral'}]
    list2 = [{'id':2 , 'num': 22} , {'id':3 , 'num': 33}]
    key = 'id'

    merged_list = [{'num': 22, 'id': 2, 'name': 'majid'}, {'num': 33, 'id': 3, 'name': 'maral'}]
    """
    merged_list = {}
    for item in list_1 + list_2:
        if item[key] in merged_list:
            merged_list[item[key]].update(item)
        else:
            merged_list[item[key]] = item
    return [val for (_, val) in merged_list.items()]


def log_request_sent(log_source, url, headers=None, request_data=None, use_logger=None):
    logger_to_use = use_logger or logger
    logger_to_use.info("~" * 10 + " REQUEST {} -- url: {}\nheader: {}\ndata: {}".format(
        log_source, url, headers, request_data))


def log_response_received(log_source, response, use_logger=None):
    logger_to_use = use_logger or logger
    logger_to_use.info("~" * 10 + " RESPONSE {} -- status: {}\ncontent: {}".format(
        log_source, response.status_code, response.content))


def get_var(variable_name, default=None):
    """
    method to raise exception if some environment variable is not set
    :param variable_name: the environment variable being searched for
    :param default: default value of the environment var
    :return: the value of the variable
    """
    val = os.environ.get(variable_name, default)
    if val is None:
        raise EnvironmentError(
            'Please set the environment variable {0}'.format(variable_name))
    return val


def get_config_or_var(var, default=''):
    """
    Returns value from current app config if running in app mode. If called outside of app context, it returns the
    value of that environment variable
    :param var: the name of config to fetch
    :param default: the default value to use
    :return: the app config value or environment variable
    """
    try:
        return current_app.config[var]
    except RuntimeError:
        return get_var(var, default)
