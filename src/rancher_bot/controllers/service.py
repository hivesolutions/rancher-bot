#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Rancher Bot
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from . import adapter

class ServiceController(adapter.AdapterController):

    @appier.route("/services/<str:id>", "GET")
    def show(self, id):
        id = self._resolve_id(id)
        self.ensure_key()
        api = self.get_api()
        service = api.get_service(id)
        return service

    @appier.route("/services/<str:id>/redeploy", ("GET", "POST"))
    def redeploy(self, id):
        id = self._resolve_id(id)
        self.ensure_key()
        api = self.get_api()
        service = api.upgrade_service(id)
        return service

    @appier.route("/services/<str:id>/restart", ("GET", "POST"))
    def restart(self, id):
        id = self._resolve_id(id)
        self.ensure_key()
        api = self.get_api()
        service = api.restart_service(id)
        return service

    def _resolve_id(self, id):
        resolve = self.field("resolve", True, cast = bool)
        if not resolve: return id
        api = self.get_api()
        service = api.get_service_safe(id)
        if not service: return id
        return service.get("id", id)
