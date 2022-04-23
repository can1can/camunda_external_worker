#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


@dataclass
class ExternalTask:
    id: str
    activity_id: str
    activity_instance_id: str
    process_instance_id: str
    topic_name: str
    detected_at: Optional[float] = None


python_type_to_java_type_name = {
    str: "string",
    bool: "boolean",
    float: "double",
    int: "long",
    datetime.datetime: "date",
    datetime.date: "string",
}


@dataclass
class Process:
    AUTHOR_VARIABLE_KEY = "_started_by_client_id"
    id: str
    definition_id: str


@dataclass
class Activity:
    id: str
    parent_activity_instance_id: str
    process_instance_id: str
    name: str
    activity_name: str
    activity_id: str
    activity_type: str
    child_activity_instances: List['Activity']
    detected_at: Optional[float] = None
    started_by_client_id: Optional[float] = None

    def __post_init__(self):
        if len(self.child_activity_instances):
            if isinstance(self.child_activity_instances[0], Activity):
                return
        child_activity_instances = []
        for child_activity_instance in self.child_activity_instances:
            child_activity_instances.append(Activity(**child_activity_instance))
        self.child_activity_instances = child_activity_instances

    def has_changed(self, activity: 'Activity'):
        assert activity.id == self.id
        if len(self.child_activity_instances) != len(activity.child_activity_instances):
            return True
        for self_child, other_child in zip(self.child_activity_instances, activity.child_activity_instances):
            if self_child.id != other_child.id:
                return True
            if self.child_activity_instances:
                return self_child.has_changed(other_child)

        return False

    def add_after_init_ags(self, detected_at, started_by_client_id):
        self.detected_at = detected_at
        self.started_by_client_id= started_by_client_id
        for self_child in self.child_activity_instances:
            self_child.add_after_init_ags(detected_at, started_by_client_id)

class SchemaError(Exception):
    pass


class NoValue:
    pass


class IncidentType(str, Enum):
    failed_external_task = "failedExternalTask"
    failed_job = "failedJob"
