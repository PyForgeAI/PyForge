# Copyright 2021-2025 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os
from unittest import mock

import pytest

from pyforge.common.config import Config
from pyforge.core.common.frequency import Frequency
from tests.core.utils.named_temporary_file import NamedTemporaryFile


def my_func():
    pass


def _configure_scenario_in_toml():
    return NamedTemporaryFile(
        content="""
[TAIPY]

[TASK.task1]
inputs = []
outputs = []

[TASK.task2]
inputs = []
outputs = []

[SCENARIO.scenarios1]
tasks = [ "task1:SECTION", "task2:SECTION"]
    """
    )


def _check_tasks_instance(task_id, scenario_id):
    """Check if the task instance in the task config correctly points to the Config._applied_config,
    not the Config._python_config or the Config._file_config
    """
    task_config_applied_instance = Config.tasks[task_id]
    task_config_instance_via_scenario = None
    for task in Config.scenarios[scenario_id].tasks:
        if task.id == task_id:
            task_config_instance_via_scenario = task

    task_config_python_instance = None
    if Config._python_config._sections.get("TASK", None):
        task_config_python_instance = Config._python_config._sections["TASK"][task_id]

    task_config_file_instance = None
    if Config._file_config._sections.get("TASK", None):
        task_config_file_instance = Config._file_config._sections["TASK"][task_id]

    assert task_config_python_instance is not task_config_applied_instance
    assert task_config_python_instance is not task_config_instance_via_scenario
    assert task_config_file_instance is not task_config_applied_instance
    assert task_config_file_instance is not task_config_instance_via_scenario
    assert task_config_instance_via_scenario is task_config_applied_instance


def test_task_instance_when_configure_scenario_in_python():
    task1_config = Config.configure_task("task1", [])
    task2_config = Config.configure_task("task2", print)
    Config.configure_scenario("scenarios1", [task1_config, task2_config])

    _check_tasks_instance("task1", "scenarios1")
    _check_tasks_instance("task2", "scenarios1")


def test_task_instance_when_configure_scenario_by_loading_toml():
    toml_config = _configure_scenario_in_toml()
    Config.load(toml_config.filename)

    _check_tasks_instance("task1", "scenarios1")
    _check_tasks_instance("task2", "scenarios1")


def test_task_instance_when_configure_scenario_by_overriding_toml():
    toml_config = _configure_scenario_in_toml()
    Config.override(toml_config.filename)

    _check_tasks_instance("task1", "scenarios1")
    _check_tasks_instance("task2", "scenarios1")


def test_scenario_creation():
    dn_config_1 = Config.configure_data_node("dn1")
    dn_config_2 = Config.configure_data_node("dn2")
    dn_config_3 = Config.configure_data_node("dn3")
    dn_config_4 = Config.configure_data_node("dn4")
    task_config_1 = Config.configure_task("task1", sum, [dn_config_1, dn_config_2], dn_config_3)
    task_config_2 = Config.configure_task("task2", print, dn_config_3)
    scenario_cfg = Config.configure_scenario(
        "scenarios1",
        [task_config_1, task_config_2],
        [dn_config_4],
        comparators={"dn_cfg": [my_func]},
        sequences={"sequence": []},
    )

    assert list(Config.scenarios.keys()) == ["default", scenario_cfg.id]

    scenario2 = Config.configure_scenario("scenarios2", [task_config_1], frequency=Frequency.MONTHLY)
    assert list(Config.scenarios.keys()) == ["default", scenario_cfg.id, scenario2.id]


def test_datanode_config_ranks():
    dn_config_1 = Config.configure_data_node("dn1")
    dn_config_2 = Config.configure_data_node("dn2")
    dn_config_3 = Config.configure_data_node("dn3")
    dn_config_4 = Config.configure_data_node("dn4")
    dn_config_5 = Config.configure_data_node("dn5")
    dn_config_6 = Config.configure_data_node("dn6")

    task_config_1 = Config.configure_task("task1", sum, dn_config_1, dn_config_2)
    task_config_2 = Config.configure_task("task2", sum, dn_config_2, dn_config_3)
    task_config_3 = Config.configure_task("task3", sum, [dn_config_1, dn_config_2], dn_config_3)
    task_config_4 = Config.configure_task("task4", sum, dn_config_3, [dn_config_4, dn_config_5])
    task_config_5 = Config.configure_task("task5", sum, dn_config_5, dn_config_6)

    # s1 additional: dn3
    # s1 dag:  dn1 -> dn2
    Config.configure_scenario("s1", [task_config_1],[dn_config_3])
    # s2 additional: dn4
    # s2 dag:  dn2 -> dn3
    Config.configure_scenario("s2", [task_config_2],[dn_config_4])
    # s3 additional: None
    # s3 dag:  dn1 -> dn2 -> dn3
    Config.configure_scenario("s3", [task_config_1, task_config_2])
    # s4 additional: None
    # s4 dag:  dn1 --                 --> dn4
    #                \               /
    #                 |----> dn3 ---|
    #                /               \
    #          dn2 --                 --> dn5 ---> dn6
    Config.configure_scenario("s4", [task_config_3, task_config_4, task_config_5])

    assert len(dn_config_1._ranks) == 3
    assert dn_config_1._ranks["s1"] == 1
    assert dn_config_1._ranks["s3"] == 1
    assert dn_config_1._ranks["s4"] == 1

    assert len(dn_config_2._ranks) == 4
    assert dn_config_2._ranks["s1"] == 2
    assert dn_config_2._ranks["s2"] == 1
    assert dn_config_2._ranks["s3"] == 2
    assert dn_config_2._ranks["s4"] == 1

    assert len(dn_config_3._ranks) == 4
    assert dn_config_3._ranks["s1"] == 0
    assert dn_config_3._ranks["s2"] == 2
    assert dn_config_3._ranks["s3"] == 3
    assert dn_config_3._ranks["s4"] == 2

    assert len(dn_config_4._ranks) == 2
    assert dn_config_4._ranks["s2"] == 0
    assert dn_config_4._ranks["s4"] == 3

    assert len(dn_config_5._ranks) == 1
    assert dn_config_5._ranks["s4"] == 3

    assert len(dn_config_6._ranks) == 1
    assert dn_config_6._ranks["s4"] == 4


def test_scenario_count():
    task_config_1 = Config.configure_task("task1", my_func)
    task_config_2 = Config.configure_task("task2", print)
    Config.configure_scenario("scenarios1", [task_config_1, task_config_2])
    assert len(Config.scenarios) == 2

    Config.configure_scenario("scenarios2", [task_config_1])
    assert len(Config.scenarios) == 3

    Config.configure_scenario("scenarios3", [task_config_2])
    assert len(Config.scenarios) == 4


def test_scenario_getitem():
    dn_config_1 = Config.configure_data_node("dn1")
    dn_config_2 = Config.configure_data_node("dn2")
    dn_config_3 = Config.configure_data_node("dn3")
    dn_config_4 = Config.configure_data_node("dn4")
    task_config_1 = Config.configure_task("task1", sum, [dn_config_1, dn_config_2], dn_config_3)
    task_config_2 = Config.configure_task("task2", print, dn_config_3)
    scenario_id = "scenarios1"
    scenario = Config.configure_scenario(scenario_id, [task_config_1, task_config_2], [dn_config_4])

    assert Config.scenarios[scenario_id].id == scenario.id

    assert Config.scenarios[scenario_id].task_configs == scenario.task_configs
    assert Config.scenarios[scenario_id].tasks == scenario.tasks
    assert Config.scenarios[scenario_id].task_configs == scenario.tasks

    assert Config.scenarios[scenario_id].additional_data_node_configs == scenario.additional_data_node_configs
    assert Config.scenarios[scenario_id].additional_data_nodes == scenario.additional_data_nodes
    assert Config.scenarios[scenario_id].additional_data_node_configs == scenario.additional_data_nodes

    assert Config.scenarios[scenario_id].data_node_configs == scenario.data_node_configs
    assert Config.scenarios[scenario_id].data_nodes == scenario.data_nodes
    assert Config.scenarios[scenario_id].data_node_configs == scenario.data_nodes

    assert scenario.tasks == [task_config_1, task_config_2]
    assert scenario.additional_data_node_configs == [dn_config_4]
    assert set(scenario.data_nodes) == {dn_config_4, dn_config_1, dn_config_2, dn_config_3}

    assert Config.scenarios[scenario_id].properties == scenario.properties


def test_scenario_creation_no_duplication():
    task_config_1 = Config.configure_task("task1", my_func)
    task_config_2 = Config.configure_task("task2", print)
    dn_config = Config.configure_data_node("dn")
    Config.configure_scenario("scenarios1", [task_config_1, task_config_2], [dn_config])

    assert len(Config.scenarios) == 2

    Config.configure_scenario("scenarios1", [task_config_1, task_config_2], [dn_config])
    assert len(Config.scenarios) == 2


def test_scenario_get_set_and_remove_comparators():
    task_config_1 = Config.configure_task("task1", my_func)
    task_config_2 = Config.configure_task("task2", print)
    dn_config_1 = "dn_config_1"
    scenario_config_1 = Config.configure_scenario(
        "scenarios1", [task_config_1, task_config_2], comparators={dn_config_1: my_func}
    )

    assert scenario_config_1.comparators is not None
    assert scenario_config_1.comparators[dn_config_1] == [my_func]
    assert len(scenario_config_1.comparators.keys()) == 1

    dn_config_2 = "dn_config_2"
    scenario_config_1.add_comparator(dn_config_2, my_func)
    assert len(scenario_config_1.comparators.keys()) == 2

    scenario_config_1.delete_comparator(dn_config_1)
    assert len(scenario_config_1.comparators.keys()) == 1

    scenario_config_1.delete_comparator(dn_config_2)
    assert len(scenario_config_1.comparators.keys()) == 0

    scenario_config_2 = Config.configure_scenario("scenarios2", [task_config_1, task_config_2])

    assert scenario_config_2.comparators is not None

    scenario_config_2.add_comparator(dn_config_1, my_func)
    assert len(scenario_config_2.comparators.keys()) == 1

    scenario_config_2.delete_comparator("dn_config_3")


def test_scenario_config_with_env_variable_value():
    task_config_1 = Config.configure_task("task1", my_func)
    task_config_2 = Config.configure_task("task2", print)
    with mock.patch.dict(os.environ, {"FOO": "bar"}):
        Config.configure_scenario("scenario_name", [task_config_1, task_config_2], prop="ENV[FOO]")
        assert Config.scenarios["scenario_name"].prop == "bar"
        assert Config.scenarios["scenario_name"].properties["prop"] == "bar"
        assert Config.scenarios["scenario_name"]._properties["prop"] == "ENV[FOO]"


def test_clean_config():
    task1_config = Config.configure_task("task1", print, [], [])
    task2_config = Config.configure_task("task2", print, [], [])
    scenario1_config = Config.configure_scenario(
        "id1",
        [task1_config, task2_config],
        [],
        Frequency.YEARLY,
        {"foo": "bar"},
        prop="foo",
        sequences={"sequence_1": []},
    )
    scenario2_config = Config.configure_scenario(
        "id2",
        [task2_config, task1_config],
        [],
        Frequency.MONTHLY,
        {"foz": "baz"},
        prop="bar",
        sequences={"sequence_2": []},
    )

    assert Config.scenarios["id1"] is scenario1_config
    assert Config.scenarios["id2"] is scenario2_config

    scenario1_config._clean()
    scenario2_config._clean()

    # Check if the instance before and after _clean() is the same
    assert Config.scenarios["id1"] is scenario1_config
    assert Config.scenarios["id2"] is scenario2_config

    assert scenario1_config.id == "id1"
    assert scenario2_config.id == "id2"
    assert scenario1_config.tasks == scenario1_config.task_configs == []
    assert scenario1_config.additional_data_nodes == scenario1_config.additional_data_node_configs == []
    assert scenario1_config.data_nodes == scenario1_config.data_node_configs == []
    assert scenario1_config.sequences == scenario1_config.sequences == {}
    assert scenario1_config.frequency is scenario1_config.frequency is None
    assert scenario1_config.comparators == scenario1_config.comparators == {}
    assert scenario1_config.properties == scenario1_config.properties == {}

    assert scenario2_config.tasks == scenario2_config.task_configs == []
    assert scenario2_config.additional_data_nodes == scenario2_config.additional_data_node_configs == []
    assert scenario2_config.data_nodes == scenario2_config.data_node_configs == []
    assert scenario2_config.sequences == scenario1_config.sequences == {}
    assert scenario2_config.frequency is scenario2_config.frequency is None
    assert scenario2_config.comparators == scenario2_config.comparators == {}
    assert scenario2_config.properties == scenario2_config.properties == {}


def test_add_sequence():
    task1_config = Config.configure_task("task1", print, [], [])
    task2_config = Config.configure_task("task2", print, [], [])
    task3_config = Config.configure_task("task3", print, [], [])
    task4_config = Config.configure_task("task4", print, [], [])
    scenario_config = Config.configure_scenario(
        "id", [task1_config, task2_config, task3_config, task4_config], [], Frequency.YEARLY, prop="foo"
    )

    assert Config.scenarios["id"] is scenario_config

    assert scenario_config.id == "id"
    assert (
        scenario_config.tasks
        == scenario_config.task_configs
        == [task1_config, task2_config, task3_config, task4_config]
    )
    assert scenario_config.additional_data_nodes == scenario_config.additional_data_node_configs == []
    assert scenario_config.data_nodes == scenario_config.data_node_configs == []
    assert scenario_config.frequency is scenario_config.frequency == Frequency.YEARLY
    assert scenario_config.comparators == scenario_config.comparators == {}
    assert scenario_config.properties == {"prop": "foo"}

    scenario_config.add_sequences(
        {
            "sequence1": [task1_config],
            "sequence2": [task2_config, task3_config],
            "sequence3": [task1_config, task2_config, task4_config],
        }
    )
    assert len(scenario_config.sequences) == 3
    assert scenario_config.sequences["sequence1"] == [task1_config]
    assert scenario_config.sequences["sequence2"] == [task2_config, task3_config]
    assert scenario_config.sequences["sequence3"] == [task1_config, task2_config, task4_config]

    scenario_config.remove_sequences("sequence1")
    assert len(scenario_config.sequences) == 2
    scenario_config.remove_sequences(["sequence2", "sequence3"])
    assert len(scenario_config.sequences) == 0

@pytest.mark.skip(reason="Generates a png that must be visually verified.")
def test_draw_1():
    dn_config_1 = Config.configure_data_node("dn1")
    dn_config_2 = Config.configure_data_node("dn2")
    dn_config_3 = Config.configure_data_node("dn3")
    dn_config_4 = Config.configure_data_node("dn4")
    dn_config_5 = Config.configure_data_node("dn5")
    task_config_1 = Config.configure_task("task1", sum, input=[dn_config_1, dn_config_2], output=dn_config_3)
    task_config_2 = Config.configure_task("task2", sum, input=[dn_config_1, dn_config_3], output=dn_config_4)
    task_config_3 = Config.configure_task("task3", print, input=dn_config_4)
    scenario_cfg = Config.configure_scenario(
        "scenario1",
        [task_config_1, task_config_2, task_config_3],
        [dn_config_5],
    )
    scenario_cfg.draw()

@pytest.mark.skip(reason="Generates a png that must be visually verified.")
def test_draw_2():
    data_node_1 = Config.configure_data_node("s1")
    data_node_2 = Config.configure_data_node("s2")
    data_node_4 = Config.configure_data_node("s4")
    data_node_5 = Config.configure_data_node("s5")
    data_node_6 = Config.configure_data_node("s6")
    data_node_7 = Config.configure_data_node("s7")
    task_1 = Config.configure_task("t1", print, [data_node_1, data_node_2], [data_node_4])
    task_2 = Config.configure_task("t2", print, None, [data_node_5])
    task_3 = Config.configure_task("t3", print, [data_node_5, data_node_4], [data_node_6])
    task_4 = Config.configure_task("t4", print, [data_node_4], [data_node_7])
    scenario_cfg = Config.configure_scenario("scenario1", [task_4, task_2, task_1, task_3])

    #  6  |   t2 _____
    #  5  |           \
    #  4  |            s5 _________________ t3 _______ s6
    #  3  |   s1 __            _ s4 _____/
    #  2  |        \ _ t1 ____/          \_ t4 _______ s7
    #  1  |        /
    #  0  |   s2 --
    #     |________________________________________________
    #         0        1         2          3          4
    scenario_cfg.draw("draw_2")

@pytest.mark.skip(reason="Generates a png that must be visually verified.")
def test_draw_3():
    data_node_1 = Config.configure_data_node("s1")
    data_node_2 = Config.configure_data_node("s2")
    data_node_3 = Config.configure_data_node("s3")
    data_node_4 = Config.configure_data_node("s4")
    data_node_5 = Config.configure_data_node("s5")
    data_node_6 = Config.configure_data_node("s6")
    data_node_7 = Config.configure_data_node("s7")

    task_1 = Config.configure_task("t1", print, [data_node_1, data_node_2, data_node_3], [data_node_4])
    task_2 = Config.configure_task("t2", print, [data_node_4], None)
    task_3 = Config.configure_task("t3", print, [data_node_4], [data_node_5])
    task_4 = Config.configure_task("t4", print, None, output=[data_node_6])
    task_5 = Config.configure_task("t5", print, [data_node_7], None)
    scenario_cfg = Config.configure_scenario("scenario1", [task_5, task_3, task_4, task_2, task_1])


    #  12 |  s7 __
    #  11 |       \
    #  10 |        \
    #  9  |  t4 _   \_ t5
    #  8  |      \                     ____ t3 ___
    #  7  |       \                   /           \
    #  6  |  s3 _  \__ s6      _ s4 _/             \___ s5
    #  5  |      \            /      \
    #  4  |       \          /        \____ t2
    #  3  |  s2 ___\__ t1 __/
    #  2  |        /
    #  1  |       /
    #  0  |  s1 _/
    #     |________________________________________________
    #         0         1         2          3          4
    scenario_cfg.draw("draw_3")
