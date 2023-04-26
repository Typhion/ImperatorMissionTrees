import codecs
from jinja2 import Template


def add_utf8_bom(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        content = f.read()
    with codecs.open(filename, 'w', 'utf-8') as f2:
        f2.write('\ufeff')
        f2.write(content)
    return


mission = Template('''{% if blank is not defined %}{% set blank = "" %}{% endif %}{% if name != blank %}{{name}}{% endif %} = {
    {% if header != blank %}header = "{{header}}"{% endif %}
    {% if icon != blank %}icon = "{{icon}}"{% endif %}
    
    {% if repeatable != blank %}repeatable = {{repeatable}}{% endif %}
    {% if chance != blank %}{{chance}}{% endif %}
    {% if abort != blank %}{{abort}}{% endif %}
    {% if potential != blank %}{{potential}}{% endif %}
    {% if on_potential != blank %}{{on_potential}}{% endif %}
    {% if on_start != blank %}{{on_start}}{% endif %}
    {% if on_abort != blank %}{{on_abort}}{% endif %}
    {% if on_completion != blank %}{{on_completion}}{% endif %}
    {% if tasks != blank %}{{tasks}}{% endif %}
''')

task = Template('''\n\t{% if blank is not defined %}{% set blank = "" %}{% endif %}{% if name != blank %}{{mission_name}}_task_{{task_id}}{% endif %} = {\n{% if icon != blank %}\t\ticon = "{{icon}}"\n{% endif %}{% if requires != blank %}\n\t\t{{requires}}\n{% endif %}{% if prevented_by != blank %}\n\t\t{{prevented_by}}\n{% endif %}{% if duration != blank %}\n\t\tduration = {{duration}}\n{% endif %}{% if monthly_on_action != blank %}\n\t\tmonthly_on_action = {{monthly_on_action}}\n{% endif %}{% if final != blank %}\n\t\tfinal = {{final}}\n{% endif %}{% if potential != blank %}\n\t\t{{potential}}\n{% endif %}{% if highlight != blank %}\n\t\t{{highlight}}\n{% endif %}{% if bypass != blank %}\n\t\t{{bypass}}\n{% endif %}{% if allow != blank %}\n\t\t{{allow}}\n{% endif %}{% if ai_chance != blank %}\n\t\t{{ai_chance}}\n{% endif %}{% if on_bypass != blank %}\n\t\t{{on_bypass}}\n{% endif %}{% if on_start != blank %}\n\t\t{{on_start}}\n{% endif %}{% if on_completion != blank %}\n\t\t{{on_completion}}{% endif %}
\t}\n
''')

missionLocFile = Template('''l_english:\n
 # Mission Tree
 {{mission_name}}:0 ""
 {{mission_name}}_DESCRIPTION:0 ""
 {{mission_name}}_CRITERIA_DESCRIPTION:0 ""
 {{mission_name}}_BUTTON_TOOLTIP:0 ""\n\n
''')

taskLocFile = Template(''' {{mission_name}}_task_{{task_id}}:0 ""
 {{mission_name}}_task_{{task_id}}_DESC:0 ""\n
''')


class Mission():
    """ Imperator: Rome Mission Tree class """

    def __init__(self,
                 name="",
                 header="",
                 icon="",
                 repeatable="",
                 chance="",
                 abort="",
                 on_potential="",
                 potential="",
                 on_start="",
                 on_abort="",
                 on_completion="",
                 tasks="",
                 tasks_list=""):
        self.tasks_list = tasks_list
        self.tasks = tasks
        self.mission = mission.render(
            name=name,
            header=header,
            icon=icon,
            repeatable=repeatable,
            chance=chance,
            abort=abort,
            on_potential=on_potential,
            potential=potential,
            on_start=on_start,
            on_abort=on_abort,
            on_completion=on_completion,
            tasks=tasks
        )

    def get_tasks(self):
        return self.tasks

    def get_tasks_list(self):
        return self.tasks_list


class Task():
    """ Imperator: Rome Mission Task class """

    def __init__(self,
                 mission_name="",
                 task_id="",
                 icon="",
                 requires="",
                 prevented_by="",
                 duration="",
                 monthly_on_action="",
                 final="",
                 potential="",
                 highlight="",
                 bypass="",
                 allow="",
                 ai_chance="",
                 on_bypass="",
                 on_start="",
                 on_completion=""):
        self.task = task.render(
            mission_name=mission_name,
            task_id=task_id,
            icon=icon,
            requires=requires,
            prevented_by=prevented_by,
            duration=duration,
            monthly_on_action=monthly_on_action,
            final=final,
            potential=potential,
            highlight=highlight,
            bypass=bypass,
            allow=allow,
            ai_chance=ai_chance,
            on_bypass=on_bypass,
            on_start=on_start,
            on_completion=on_completion
        )


class MissionFile():
    """ Imperator: Rome mission tree file"""

    def __init__(self, *args):
        self.file = ""
        self.loc_file = ""
        self.mission_name = args[0]
        self.make_file(args)
        self.make_loc_file(args)

    def make_file(self, args):
        # for i, j in enumerate(args):
        # if i == 0: j = f"# Generated file, don't change manually or changes will be lost.\n"
        self.file += args[1].mission + "\n"
        self.file += "}\n"
        self.write()

    def write(self, add_bom=True):
        path = f"02_{self.mission_name}.txt"
        with open(path, "w") as file:
            file.write(self.file)
        if add_bom:
            add_utf8_bom(path)

    def make_loc_file(self, args):
        # for i, j in enumerate(args):
        # if i == 0: j = f"# Generated file, don't change manually or changes will be lost.\n"
        self.loc_file += missionLocFile.render(
            mission_name=self.mission_name
        )
        for i in range(len(args[1].tasks_list)):
            self.loc_file += taskLocFile.render(
                mission_name=self.mission_name,
                task_id=i + 1
            )
        self.loc_file += "\n"
        self.write_loc()

    def write_loc(self, add_bom=True):
        path = f"{self.mission_name}_l_english.yml"
        with open(path, "w") as loc_file:
            loc_file.write(self.loc_file)
        if add_bom:
            add_utf8_bom(path)
