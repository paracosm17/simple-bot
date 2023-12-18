from aiogram.fsm.state import StatesGroup, State


class ProfileStates(StatesGroup):
    language_state = State()
    main_menu_state = State()
    add_new_group_state = State()
    my_groups_state = State()
    change_language_state = State()
    group_settings_state = State()
