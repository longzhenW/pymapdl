# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Submit PyHPS jobs to a cluster"""

import logging
import os
from typing import Optional, Union

import click

from ansys.mapdl.core.cli import main

logger = logging.getLogger()
logging.basicConfig(
    format="[%(asctime)s | %(levelname)s] %(message)s", level=logging.DEBUG
)


@main.command(
    short_help="Submit jobs to an HPC cluster using PyHPS package.",
    help="""Submit jobs to an HPC cluster using PyHPS package.""",
)
@click.argument("main_file")
@click.option(
    "--name",
    default=None,
    type=str,
    help="""Name of the PyHPS project to be created.""",
)
@click.option(
    "--url",
    default=None,
    type=str,
    help="""URL where the HPS cluster is deployed. For example: "https://myserver:3000/hps" """,
)
@click.option(
    "--user", default=None, type=str, help="Username to login into the HPC cluster."
)
@click.option(
    "--password",
    default=None,
    type=str,
    help="Password used to login into the HPC cluster.",
)
@click.option(
    "--python",
    default=None,
    type=str,
    help="""Set python version to be used to create the virtual environment and
run the python file. By default it uses python3 (default in cluster).""",
)
@click.option(
    "--output_files",
    default=None,
    type=str,
    help="""Set the output files to be monitored. This is optional. """,
)
@click.option(
    "--shell_file",
    default=None,
    type=str,
    help="""If desired, you can provide a shell script to execute instead of
the python file. You can call your python file from it if you wish. By default,
it is not used.""",
)
@click.option(
    "--requirements_file",
    default=None,
    type=str,
    help="""If provided, the created virtual environment is installed with the
libraries specified in this file. If not, the activated virtual environment is
cloned through a temporary 'pip list' file. If you are using editable package,
it is recommended you attach your own requirement file. """,
)
@click.option(
    "--extra_files",
    default=None,
    type=str,
    help="""To upload extra files which can be called from your main python file
(or from the shell file).""",
)
@click.option(
    "--config_file",
    default=None,
    type=str,
    help="""To load job configuration from a file.""",
)
@click.option(
    "--num_cores",
    default=None,
    type=str,
    help=""" """,
)
@click.option(
    "--memory",
    default=None,
    type=str,
    help=""" """,
)
@click.option(
    "--disk_space",
    default=None,
    type=str,
    help=""" """,
)
@click.option(
    "--exclusive",
    default=None,
    type=str,
    help=""" """,
)
@click.option(
    "--max_execution_time",
    default=None,
    type=str,
    help=""" """,
)
@click.option(
    "--wait",
    default=None,
    type=str,
    help=""" """,
)
@click.option(
    "--save_config_file",
    default=False,
    type=bool,
    is_flag=False,
    flag_value=True,
    help="""If true, it also write the configuration to the config file, after successfully
submit the job.
It overwrites the configuration.""",
)
def submit(
    main_file: str,
    name: str = None,
    url: str = None,
    user: str = None,
    password: str = None,
    python: float = 3.9,
    output_files: Optional[Union[str, list]] = None,
    shell_file: str = None,
    requirements_file: str = None,
    extra_files: Optional[Union[str, list]] = None,
    config_file: str = None,
    num_cores: int = None,
    memory: int = None,
    disk_space: int = None,
    exclusive: bool = None,
    max_execution_time: int = None,
    wait: bool = False,
    save_config_file: bool = False,
):
    """Example code:
    pymapdl submit my_file.sh my_file_01.py my_file_02  --name="my job" --url="https://10.231.106.91:3000/hps" --user=repuser --password=repuser --python=3.9
    """
    import json

    from ansys.mapdl.core.hpc.pyhps import (
        create_pymapdl_pyhps_job,
        get_value_from_json_or_default,
        wait_for_completion,
    )

    if config_file is None:
        config_file = os.path.join(os.getcwd(), "hps_config.json")

    url = get_value_from_json_or_default(url, config_file, "url", None)
    user = get_value_from_json_or_default(user, config_file, "user", None)
    password = get_value_from_json_or_default(password, config_file, "password", None)
    python = get_value_from_json_or_default(python, config_file, "python", 3)
    name = get_value_from_json_or_default(name, config_file, "name", "My PyMAPDL job")

    num_cores = get_value_from_json_or_default(num_cores, config_file, "num_cores", 1)
    memory = get_value_from_json_or_default(memory, config_file, "memory", 100)
    disk_space = get_value_from_json_or_default(
        disk_space, config_file, "disk_space", 100
    )
    exclusive = get_value_from_json_or_default(
        exclusive, config_file, "exclusive", False
    )
    max_execution_time = get_value_from_json_or_default(
        max_execution_time, config_file, "max_execution_time", 1000
    )

    proj = create_pymapdl_pyhps_job(
        main_file=main_file,
        name=name,
        url=url,
        user=user,
        password=password,
        python=python,
        output_files=output_files,
        shell_file=shell_file,
        requirements_file=requirements_file,
        extra_files=extra_files,
        config_file=config_file,
        num_cores=num_cores,
        memory=memory,
        disk_space=disk_space,
        exclusive=exclusive,
        max_execution_time=max_execution_time,
    )

    if save_config_file:
        config = {
            "url": url,
            "user": user,
            "password": password,
            "python": python,
            "name": name,
            "num_cores": num_cores,
            "memory": memory,
            "disk_space": disk_space,
            "exclusive": exclusive,
            "max_execution_time": max_execution_time,
        }
        with open(config_file, "w") as fid:
            json.dump(config, fid)

    if wait:
        print(f"Waiting for project {name} to be completed...")
        wait_for_completion(proj, evaluated=True, failed=True)


def list_jobs():
    pass


def stop_job():
    pass
