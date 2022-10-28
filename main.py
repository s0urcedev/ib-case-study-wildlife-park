import json
import sys
import os
import random

if getattr(sys, 'frozen', False):
    APP_PATH: str = os.path.dirname(sys.executable)
elif __file__:
    APP_PATH: str = os.path.dirname(__file__)
else:
    APP_PATH: str = "C:"
APP_PATH = APP_PATH.replace("\\", "/")

with open(f"{APP_PATH}/options.json") as options_file:
    OPTIONS: dict = json.loads(options_file.read())

MAX_INDEX_LEN_TICKETS: int = max(len('Index') - 1, len(str(len(OPTIONS['tickets']['types']) - 1) + ' / ' + str(len(OPTIONS['tickets']['types']))))
MAX_NAME_LEN_TICKETS: int = max(len('Name') - 1, max([len(name["name"]) for name in OPTIONS["tickets"]["types"]]))
MAX_ONE_DAY_COST_LEN_TICKETS: int = max(len('Cost for one day') - 1, max([len(str(cost["cost_for_one_day"])) + 1 for cost in OPTIONS["tickets"]["types"]]))
MAX_TWO_DAYS_COST_LEN_TICKETS: int = max(len('Cost for two days') - 1, max([len(str(cost["cost_for_two_days"])) + 1 for cost in OPTIONS["tickets"]["types"]]))

MAX_INDEX_LEN_EXTRA: int = max(len('Index') - 1, len(str(len(OPTIONS['tickets']['types']))))
MAX_NAME_LEN_EXTRA: int = max(len('Name') - 1, max([len(name["name"]) for name in OPTIONS["extra"]["types"]]))
MAX_COST_LEN_EXTRA: int = max(len('Cost') - 1, max([len(str(cost["cost"])) + 1 for cost in OPTIONS["extra"]["types"]]))

def get_extra_spaces(maximum: int, text: str) -> str:
    return (maximum - len(text) + 1) * ' '

TOP_TICKETS: str = f"| Index{get_extra_spaces(MAX_INDEX_LEN_TICKETS, 'Index')} | Name{(MAX_NAME_LEN_TICKETS - len('Name') + 1) * ' '} | Cost for one day{(MAX_ONE_DAY_COST_LEN_TICKETS - len('Cost for one day') + 1) * ' '} | Cost for two days{(MAX_TWO_DAYS_COST_LEN_TICKETS - len('Cost for two days') + 1) * ' '} |"
TOP_EXTRA: str = f"| Index{get_extra_spaces(MAX_INDEX_LEN_EXTRA, 'Index')} | Name{(MAX_NAME_LEN_EXTRA - len('Name') + 1) * ' '} | Cost{(MAX_COST_LEN_EXTRA - len('Cost') + 1) * ' '} |"
    
if __name__ == "__main__":
    print(f"{OPTIONS['tickets']['name']}: ")
    option_index: int = 1
    print(len(TOP_TICKETS) * '-')
    print(TOP_TICKETS)
    print(len(TOP_TICKETS) * '-')
    for type in OPTIONS["tickets"]["types"]:
        print(f"| {option_index} / {option_index + 1}{get_extra_spaces(MAX_INDEX_LEN_TICKETS, str(option_index) + ' / ' + str(option_index + 1))} | {type['name']}{get_extra_spaces(MAX_NAME_LEN_TICKETS, type['name'])} | ${type['cost_for_one_day']}{get_extra_spaces(MAX_ONE_DAY_COST_LEN_TICKETS, '$' + str(type['cost_for_one_day']))} | ${type['cost_for_two_days']}{get_extra_spaces(MAX_TWO_DAYS_COST_LEN_TICKETS, '$' + str(type['cost_for_two_days']))} |")
        option_index += 2
    print(len(TOP_TICKETS) * '-')
    print("")
    print(f"{OPTIONS['extra']['name']}: ")
    print(len(TOP_EXTRA) * '-')
    print(TOP_EXTRA)
    print(len(TOP_EXTRA) * '-')
    for type in OPTIONS["extra"]["types"]:
        print(f"| {option_index}{get_extra_spaces(MAX_INDEX_LEN_EXTRA, str(option_index))} | {type['name']}{get_extra_spaces(MAX_NAME_LEN_EXTRA, type['name'])} | ${type['cost']}{get_extra_spaces(MAX_COST_LEN_EXTRA, '$' + str(type['cost']))} |")
        option_index += 1
    print(len(TOP_EXTRA) * '-')
    print("")
    try:
        CHOSEN_OPTIONS_INDEXES: list[int] = list(map(lambda x: int(x) - 1, input("Put options using space: ").split(" ")))
    except:
        print(f"Wrong input")
        sys.exit()
    order_sum: int = 0
    for chosen_option_index in CHOSEN_OPTIONS_INDEXES:
        if chosen_option_index < len(OPTIONS["tickets"]["types"]) * 2:
            if chosen_option_index % 2 == 0:
                order_sum += OPTIONS["tickets"]["types"][chosen_option_index // 2]["cost_for_one_day"]
            else:
                order_sum += OPTIONS["tickets"]["types"][chosen_option_index // 2]["cost_for_two_days"]
        elif chosen_option_index < len(OPTIONS["tickets"]["types"]) * 2 + len(OPTIONS["extra"]["types"]):
            order_sum += OPTIONS["extra"]["types"][chosen_option_index - len(OPTIONS["tickets"]["types"]) * 2]["cost"]
        else:
            print(f"First wrong index: '{chosen_option_index + 1}'")
            sys.exit()
    print(f"Total cost of the order: ${order_sum}")
    print(f"Order number: {''.join([str(random.randint(1, 9)) for _ in range(0, 9)])}")