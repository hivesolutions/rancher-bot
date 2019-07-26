#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Rancher Bot
# Copyright (c) 2008-2019 Hive Solutions Lda.
#
# This file is part of Hive Rancher Bot.
#
# Hive Rancher Bot is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Rancher Bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Rancher Bot. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from . import adapter

class WorkloadController(adapter.AdapterController):

    @appier.route("/clusters/<str:cluster>/projects/<str:project>/workloads/<str:id>", "GET")
    def show(self, cluster, project, id):
        api = self.get_api()
        cluster = api.get_cluster_safe(cluster)["id"]
        project = api.get_project_safe(cluster, project)["id"]
        id = self._resolve_id(project, id)
        self.ensure_key()
        workload = api.get_workload(project, id)
        return workload

    @appier.route("/clusters/<str:cluster>/projects/<str:project>/workloads/<str:id>/redeploy", ("GET", "POST"))
    def redeploy(self, cluster, project, id):
        api = self.get_api()
        cluster = api.get_cluster_safe(cluster)["id"]
        project = api.get_project_safe(cluster, project)["id"]
        id = self._resolve_id(project, id)
        self.ensure_key()
        workload = api.upgrade_workload(project, id)
        return workload

    def _resolve_id(self, project, id):
        resolve = self.field("resolve", True, cast = bool)
        if not resolve: return id
        api = self.get_api()
        workload = api.get_workload_safe(project, id)
        if not workload: return id
        return workload.get("id", id)
