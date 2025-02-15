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

from collections import defaultdict
from copy import copy
from typing import Any, Callable, Dict, List, Optional, Union

import networkx as nx

from pyforge.common.config import Config
from pyforge.common.config._config import _Config
from pyforge.common.config.common._template_handler import _TemplateHandler as _tpl
from pyforge.common.config.common._validate_id import _validate_id
from pyforge.common.config.section import Section

from ..common.frequency import Frequency
from .data_node_config import DataNodeConfig
from .task_config import TaskConfig


class ScenarioConfig(Section):
    """Configuration fields needed to instantiate an actual `Scenario^`."""

    name = "SCENARIO"

    _SEQUENCES_KEY = "sequences"
    _TASKS_KEY = "tasks"
    _ADDITIONAL_DATA_NODES_KEY = "additional_data_nodes"
    _FREQUENCY_KEY = "frequency"
    _COMPARATOR_KEY = "comparators"

    frequency: Optional[Frequency]
    """The frequency of the scenario's cycle. The default value is None."""
    comparators: Dict[str, List[Callable]]
    """The comparator functions used to compare scenarios.

    The default value is None.

    Each comparator function is attached to a scenario's data node configuration.
    The key of the dictionary parameter corresponds to the data node configuration id.
    The value is a list of functions that are applied to all the data nodes instantiated
    from the data node configuration attached to the comparator.
    """
    sequences: Dict[str, List[TaskConfig]]
    """Dictionary of sequence descriptions. The default value is None."""

    def __init__(
        self,
        id: str,
        tasks: Optional[Union[TaskConfig, List[TaskConfig]]] = None,
        additional_data_nodes: Optional[Union[DataNodeConfig, List[DataNodeConfig]]] = None,
        frequency: Optional[Frequency] = None,
        comparators: Optional[Dict[str, Union[List[Callable], Callable]]] = None,
        sequences: Optional[Dict[str, List[TaskConfig]]] = None,
        **properties,
    ):
        if tasks:
            self._tasks = [tasks] if isinstance(tasks, TaskConfig) else copy(tasks)
        else:
            self._tasks = []

        if additional_data_nodes:
            self._additional_data_nodes = (
                [additional_data_nodes]
                if isinstance(additional_data_nodes, DataNodeConfig)
                else copy(additional_data_nodes)
            )
        else:
            self._additional_data_nodes = []

        self.sequences = sequences if sequences else {}
        self.frequency = frequency
        self.comparators = defaultdict(list)

        if comparators:
            for k, v in comparators.items():
                if isinstance(v, list):
                    self.comparators[_validate_id(k)].extend(v)
                else:
                    self.comparators[_validate_id(k)].append(v)
        super().__init__(id, **properties)
        self.__build_datanode_configs_ranks()

    def __copy__(self):
        comp = None if self.comparators is None else self.comparators
        return ScenarioConfig(
            self.id,
            copy(self._tasks),
            copy(self._additional_data_nodes),
            self.frequency,
            copy(comp),
            copy(self.sequences),
            **copy(self._properties),
        )

    def __getattr__(self, item: str) -> Optional[Any]:
        return _tpl._replace_templates(self._properties.get(item))

    @property
    def task_configs(self) -> List[TaskConfig]:
        """List of task configurations used by this scenario configuration."""
        return self._tasks

    @property
    def tasks(self) -> List[TaskConfig]:
        """List of task configurations used by this scenario configuration."""
        return self._tasks

    @property
    def additional_data_node_configs(self) -> List[DataNodeConfig]:
        """List of additional data nodes used by this scenario configuration."""
        return self._additional_data_nodes

    @property
    def additional_data_nodes(self) -> List[DataNodeConfig]:
        """List of additional data nodes used by this scenario configuration."""
        return self._additional_data_nodes

    @property
    def data_node_configs(self) -> List[DataNodeConfig]:
        """List of all data nodes used by this scenario configuration."""
        return self.__get_all_unique_data_nodes()

    @property
    def data_nodes(self) -> List[DataNodeConfig]:
        """List of all data nodes used by this scenario configuration."""
        return self.__get_all_unique_data_nodes()

    def add_comparator(self, dn_config_id: str, comparator: Callable) -> None:
        """Add a comparator to the scenario configuration.

        Arguments:
            dn_config_id (str): The data node configuration id to which the comparator
                will be applied.
            comparator (Callable): The comparator function to be added.
        """
        self.comparators[dn_config_id].append(comparator)

    def delete_comparator(self, dn_config_id: str) -> None:
        """Delete a comparator from the scenario configuration."""
        if dn_config_id in self.comparators:
            del self.comparators[dn_config_id]

    def add_sequences(self, sequences: Dict[str, List[TaskConfig]]) -> None:
        """Add sequence descriptions to the scenario configuration.

        When a `Scenario^` is instantiated from this configuration, the
        sequence descriptions are used to add new sequences to the scenario.

        Arguments:
            sequences (Dict[str, List[TaskConfig]]): Dictionary of sequence descriptions.
        """
        self.sequences.update(sequences)

    def remove_sequences(self, sequence_names: Union[str, List[str]]) -> None:
        """Remove sequence descriptions from the scenario configuration.

        Arguments:
            sequence_names (Union[str, List[str]]): The name of the sequence or a list
                of sequence names.
        """
        if isinstance(sequence_names, List):
            for sequence_name in sequence_names:
                self.sequences.pop(sequence_name)
        else:
            self.sequences.pop(sequence_names)

    @classmethod
    def default_config(cls) -> "ScenarioConfig":
        """Get a scenario configuration with all the default values.

        Returns:
            A scenario configuration with all the default values.
        """
        return ScenarioConfig(cls._DEFAULT_KEY, [], [], None, {})

    def draw(self, file_path: Optional[str] = None) -> None:
        """
        Export the scenario configuration graph as a PNG file.

        This function uses the `matplotlib` library to draw the scenario configuration graph.
        `matplotlib` must be installed independently of `pyforge` as it is not a dependency.
        If `matplotlib` is not installed, the function will log an error message, and do nothing.

        Arguments:
            file_path (Optional[str]): The path to save the PNG file.
                If not provided, the file will be saved with the scenario configuration id.
        """
        from importlib import util

        from pyforge.common.logger._pyforge_logger import _PyForgeLogger
        logger = _PyForgeLogger._get_logger()

        if not util.find_spec("matplotlib"):
            logger.error("Cannot draw the scenario configuration as `matplotlib` is not installed.")
            return
        import matplotlib.pyplot as plt

        from pyforge.core._entity._dag import _DAG
        graph = self.__build_nx_dag()
        positioned_nodes = _DAG(graph).nodes.values()
        pos = {node.entity: (node.x, node.y) for node in positioned_nodes}
        labls = {node.entity: node.entity.id for node in positioned_nodes}

        # Draw the graph
        plt.figure(figsize=(10, 10))
        nx.draw_networkx_nodes(graph, pos,
                               nodelist=[node for node in graph.nodes if isinstance(node, DataNodeConfig)],
                               node_color="skyblue",
                               node_shape="s",
                               node_size=2000)
        nx.draw_networkx_nodes(graph, pos,
                               nodelist=[node for node in graph.nodes if isinstance(node, TaskConfig)],
                               node_color="orange",
                               node_shape="D",
                               node_size=2000)
        nx.draw_networkx_labels(graph, pos, labels=labls)
        nx.draw_networkx_edges(graph, pos, node_size=2000, edge_color="black", arrowstyle="->", arrowsize=25)

        # Save the graph as a PNG file
        path = file_path or f"{self.id}.png"
        plt.savefig(path)
        plt.close()  # Close the plot to avoid display
        logger.info(f"The graph image of the scenario configuration `{self.id}` is exported: {path}")

    def _clean(self):
        self._tasks = []
        self._additional_data_nodes = []
        self.frequency = None
        self.comparators = {}
        self.sequences = {}
        self._properties = {}

    def _to_dict(self) -> Dict[str, Any]:
        return {
            self._COMPARATOR_KEY: self.comparators,
            self._TASKS_KEY: self._tasks,
            self._ADDITIONAL_DATA_NODES_KEY: self._additional_data_nodes,
            self._FREQUENCY_KEY: self.frequency,
            self._SEQUENCES_KEY: self.sequences,
            **self._properties,
        }

    @classmethod
    def _from_dict(cls, as_dict: Dict[str, Any], id: str,
                   config: Optional[_Config] = None) -> "ScenarioConfig":  # type: ignore
        as_dict.pop(cls._ID_KEY, id)

        tasks = cls.__get_task_configs(as_dict.pop(cls._TASKS_KEY, []), config)

        additional_data_node_ids = as_dict.pop(cls._ADDITIONAL_DATA_NODES_KEY, [])
        additional_data_nodes = cls.__get_additional_data_node_configs(additional_data_node_ids, config)

        frequency = as_dict.pop(cls._FREQUENCY_KEY, None)
        comparators = as_dict.pop(cls._COMPARATOR_KEY, {})
        sequences = as_dict.pop(cls._SEQUENCES_KEY, {})

        for sequence_name, sequence_tasks in sequences.items():
            sequences[sequence_name] = cls.__get_task_configs(sequence_tasks, config)

        return ScenarioConfig(
            id=id,
            tasks=tasks,
            additional_data_nodes=additional_data_nodes,
            frequency=frequency,
            comparators=comparators,
            sequences=sequences,
            **as_dict,
        )

    def _update(self, as_dict: Dict[str, Any], default_section=None):
        self._tasks = as_dict.pop(self._TASKS_KEY, self._tasks)
        if self._tasks is None and default_section:
            self._tasks = default_section._tasks

        self._additional_data_nodes = as_dict.pop(self._ADDITIONAL_DATA_NODES_KEY, self._additional_data_nodes)
        if self._additional_data_nodes is None and default_section:
            self._additional_data_nodes = default_section._additional_data_nodes

        self.frequency = as_dict.pop(self._FREQUENCY_KEY, self.frequency)
        if self.frequency is None and default_section:
            self.frequency = default_section.frequency

        self.comparators = as_dict.pop(self._COMPARATOR_KEY, self.comparators)
        if self.comparators is None and default_section:
            self.comparators = default_section.comparators

        self.sequences = as_dict.pop(self._SEQUENCES_KEY, self.sequences)
        if self.sequences is None and default_section:
            self.sequences = default_section.sequences

        self._properties.update(as_dict)
        if default_section:
            self._properties = {**default_section.properties, **self._properties}

    @staticmethod
    def _types_to_register() -> List[type]:
        return [Frequency]

    @staticmethod
    def _configure(
        id: str,
        task_configs: Optional[List[TaskConfig]] = None,
        additional_data_node_configs: Optional[List[DataNodeConfig]] = None,
        frequency: Optional[Frequency] = None,
        comparators: Optional[Dict[str, Union[List[Callable], Callable]]] = None,
        sequences: Optional[Dict[str, List[TaskConfig]]] = None,
        **properties,
    ) -> "ScenarioConfig":
        """Configure a new scenario configuration.

        Arguments:
            id (str): The unique identifier of the new scenario configuration.
            task_configs (Optional[List[TaskConfig^]]): The list of task configurations used by this
                scenario configuration. The default value is None.
            additional_data_node_configs (Optional[List[DataNodeConfig^]]): The list of additional data nodes
                related to this scenario configuration. The default value is None.
            frequency (Optional[Frequency^]): The scenario frequency.<br/>
                It corresponds to the recurrence of the scenarios instantiated from this
                configuration. Based on this frequency each scenario will be attached to the
                relevant cycle.
            comparators (Optional[Dict[str, Union[List[Callable], Callable]]]): The list of
                functions used to compare scenarios. A comparator function is attached to a
                scenario's data node configuration. The key of the dictionary parameter
                corresponds to the data node configuration id. During the scenarios'
                comparison, each comparator is applied to all the data nodes instantiated from
                the data node configuration attached to the comparator. See
                `(pyforge.)compare_scenarios()^` more details.
            sequences (Optional[Dict[str, List[TaskConfig]]]): Dictionary of sequence descriptions.
                The default value is None.
            **properties (dict[str, any]): A keyworded variable length list of additional arguments.

        Returns:
            The new scenario configuration.
        """
        section = ScenarioConfig(
            id,
            task_configs,
            additional_data_node_configs,
            frequency=frequency,
            comparators=comparators,
            sequences=sequences,
            **properties,
        )
        Config._register(section)
        return Config.sections[ScenarioConfig.name][id]

    @staticmethod
    def _set_default_configuration(
        task_configs: Optional[List[TaskConfig]] = None,
        additional_data_node_configs: List[DataNodeConfig] = None,
        frequency: Optional[Frequency] = None,
        comparators: Optional[Dict[str, Union[List[Callable], Callable]]] = None,
        sequences: Optional[Dict[str, List[TaskConfig]]] = None,
        **properties,
    ) -> "ScenarioConfig":
        """Set the default values for scenario configurations.

        This function creates the *default scenario configuration* object,
        where all scenario configuration objects will find their default
        values when needed.

        Arguments:
            task_configs (Optional[List[TaskConfig^]]): The list of task configurations used by this
                scenario configuration.
            additional_data_node_configs (Optional[List[DataNodeConfig^]]): The list of additional data nodes
                related to this scenario configuration.
            frequency (Optional[Frequency^]): The scenario frequency.
                It corresponds to the recurrence of the scenarios instantiated from this
                configuration. Based on this frequency each scenario will be attached to
                the relevant cycle.
            comparators (Optional[Dict[str, Union[List[Callable], Callable]]]): The list of
                functions used to compare scenarios. A comparator function is attached to a
                scenario's data node configuration. The key of the dictionary parameter
                corresponds to the data node configuration id. During the scenarios'
                comparison, each comparator is applied to all the data nodes instantiated from
                the data node configuration attached to the comparator. See
                `pyforge.compare_scenarios()^` more details.
            sequences (Optional[Dict[str, List[TaskConfig]]]): Dictionary of sequences. The default value is None.
            **properties (dict[str, any]): A keyworded variable length list of additional arguments.

        Returns:
            The new default scenario configuration.
        """
        section = ScenarioConfig(
            _Config.DEFAULT_KEY,
            task_configs,
            additional_data_node_configs,
            frequency=frequency,
            comparators=comparators,
            sequences=sequences,
            **properties,
        )
        Config._register(section)
        return Config.sections[ScenarioConfig.name][_Config.DEFAULT_KEY]

    def __get_all_unique_data_nodes(self) -> List[DataNodeConfig]:
        data_node_configs = set(self._additional_data_nodes)
        for task in self._tasks:
            data_node_configs.update(task.inputs)
            data_node_configs.update(task.outputs)

        return list(data_node_configs)

    @staticmethod
    def __get_task_configs(task_config_ids: List[str], config: Optional[_Config]):
        task_configs = set()
        if config:
            if task_config_section := config._sections.get(TaskConfig.name):
                for task_config_id in task_config_ids:
                    if task_config := task_config_section.get(task_config_id, None):
                        task_configs.add(task_config)
        return list(task_configs)

    @staticmethod
    def __get_additional_data_node_configs(additional_data_node_ids: List[str], config: Optional[_Config]):
        additional_data_node_configs = set()
        if config:
            if data_node_config_section := config._sections.get(DataNodeConfig.name):
                for additional_data_node_id in additional_data_node_ids:
                    if additional_data_node_config := data_node_config_section.get(additional_data_node_id):
                        additional_data_node_configs.add(additional_data_node_config)
        return list(additional_data_node_configs)

    def __build_nx_dag(self) -> nx.DiGraph:
        g = nx.DiGraph()
        for task in set(self.tasks):
            if has_input := task.inputs:
                for predecessor in task.inputs:
                    g.add_edges_from([(predecessor, task)])
            if has_output := task.outputs:
                for successor in task.outputs:
                    g.add_edges_from([(task, successor)])
            if not has_input and not has_output:
                g.add_node(task)
        return g

    def __build_datanode_configs_ranks(self):
        # build the DAG
        dag = self.__build_nx_dag()
        # Remove tasks with no input
        to_remove = [t for t, degree in dict(dag.in_degree).items() if degree == 0 and isinstance(t, TaskConfig)]
        dag.remove_nodes_from(to_remove)
        # get data nodes in the dag
        dn_cfgs = [nodes for nodes in nx.topological_generations(dag) if (DataNodeConfig in (type(n) for n in nodes))]

        # assign ranks to data nodes configs starting from 1
        rank = 1
        for same_rank_datanode_cfgs in dn_cfgs:
            for dn_cfg in same_rank_datanode_cfgs:
                dn_cfg._ranks[self.id] = rank
            rank += 1
        # additional data nodes (not in the dag) have a rank of 0
        for add_dn_cfg in self._additional_data_nodes:
            add_dn_cfg._ranks[self.id] = 0
