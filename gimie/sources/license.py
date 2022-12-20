# Gimie
# Copyright 2022 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from scancode.api import get_licenses
import re
from rdflib import Graph, Literal, URIRef

path = r"C:\Users\franken\gimie"  # this is to be filled with the path from the CLI input, not sure how to access it


def find_licenses(path: str):
    """returns a python list of licenses found at destination path"""
    path_files = os.listdir(path)
    g = Graph()
    found_licenses = []
    for file in path_files:
        result = re.match(
            "((licens.*)|(reuse)|(copy))", file, flags=re.IGNORECASE
        )
        # regex used is very basic right now, what are other common license file names?
        if result:
            license_location = str(path) + "\\" + str(file)
            license_mappings = get_licenses(license_location, min_score=50)
            # todo we need some tests to see how to set this min_score param

            extracted_license = (license_mappings.get("licenses")[0]).get(
                "spdx_url"
            )
            found_licenses.append(extracted_license)
            g.add(
                (
                    URIRef("https://www.gimie.org/repo"),
                    URIRef("https://schema.org/license"),
                    URIRef(str(extracted_license)),
                )
            )
            g.serialize(destination="extractedtriple.ttl", format="ttl")
    return found_licenses


# todo write a similar function for online repositories using just the repository URL

# class LicenseMetadata:
#     def __init__(self, path: str):
#         raise NotImplementedError
