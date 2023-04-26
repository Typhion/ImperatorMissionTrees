from jinja2 import Template
from missions import Mission, Task, MissionFile

mission_name = "test_missions"

t1 = Task(
    mission_name=mission_name,
    task_id="1",
    icon="task_shiva",
    requires="",
    prevented_by="",
    duration="",
    monthly_on_action="",
    final="",
    potential="",
    highlight="",
    bypass="",
    allow=Template('''allow = {
            custom_tooltip = {
                text = tylos_missions_task_1_a_tt
                has_variable = made_giant_shark_statue
            }
            custom_tooltip = {
                text = tylos_missions_task_1_a_tt2
                deity:omen_awal = {
                    has_holy_site = yes
                    holy_site = {
                        this = p:7202
                    }
                }
            }
            religious_unity >= 75
        }''').render(),
    ai_chance="",
    on_bypass="",
    on_start="",
    on_completion=Template('''on_completion = {
            add_country_modifier = {
                name = people_of_the_sea
                duration = 3650
            }
            custom_tooltip = tylos_missions_task_1_c_tt
            hidden_effect = {
                p:7202 = {
                    while = {
                        count = 2
                        define_pop = {
                            type = nobles
                            culture = babylonian
                            religion = mesopotamian_religion
                        }
                    }
                }
            }
        }''').render()
)

t2 = Task(
    mission_name=mission_name,
    task_id="2",
    icon="task_political",
    requires=Template('''requires = { tylos_missions_task_11 }''').render(),
    prevented_by="",
    duration="",
    monthly_on_action="",
    final="",
    potential="",
    highlight="",
    bypass="",
    allow=Template('''allow = {
            p:7202 = {
                num_of_commerce_building >= 2
            }
            invention = state_trade_inv_1
            num_of_ships >= 15
        }''').render(),
    ai_chance="",
    on_bypass="",
    on_start="",
    on_completion=Template('''on_completion = {
            add_country_modifier = {
                name = tylos_cotton_trade
                duration = 3650
            }
            custom_tooltip = tylos_missions_task_2_c_tt
            hidden_effect = {
                every_country = {
                    limit = {
                        OR = {
                            country_culture_group = aryan
                            country_culture_group = south_levantine
                        }
                    }
                    add_opinion = {
                        modifier = aryan_arab_cotton_trade_relations_tylos
                        target = root
                    }
                }
            }
        }''').render()
)

m1 = Mission(
    name=mission_name,
    header="indian_mission_header",
    icon="seleukid_4",
    repeatable="no",
    chance=Template('''
    chance = {
        factor = 50000
    }''').render(),
    abort=Template('''
    abort = {
        ai_mission_back_out_trigger = yes
    }''').render(),
    on_potential=Template('''
    on_potential = {
        add_stability = 20
    }''').render(),
    potential=Template('''
    potential = {
        OR = {
            tag = TYO
            primary_culture = babylonian
        }
        NOT = { has_variable = tylos_mission_cooldown }
    }''').render(),
    on_start=Template('''
    on_start = {
        start_mission_ai_effect = yes
        save_scope_as = mission_country
        random_country_culture = {
            limit = {
                is_culture = babylonian
            }
            save_scope_as = babylonian_culture_scope
        }
        random_country_culture = {
            limit = {
                is_culture = makan
            }
            save_scope_as = makan_culture_scope
        }
    }''').render(),
    on_abort=Template('''
    on_abort = {
        custom_tooltip = general_mission_cooldown_tt
        set_variable = {
            name = tylos_mission_cooldown
            days = 7300
        }
        add_stability = -5
        current_ruler = {
            add_popularity = -25
        }
    }''').render(),
    on_completion=Template('''
    on_completion = {
        complete_mission_effect = yes
    }''').render(),
    tasks=t1.task + t2.task,
    tasks_list=[t1, t2]
)

if __name__ == '__main__':
    imperator_mission_tree = MissionFile(mission_name, m1)
