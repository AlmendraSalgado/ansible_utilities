import yaml
import sys
import os
from formatting_functions import *


if len(sys.argv) != 4:
    print("Usage: python format_aap_export.py <resource_type> <input_file.yml> <output_file.yml>")
    print("resource_type_plural: projects | inventories | credentials | job_templates | execution_environments | inventory_sources | organizations | users | hosts | groups | schedules | credential_types | applications | teams | notifications")
    sys.exit(1)

resource_type = sys.argv[1].lower()
input_file = sys.argv[2]
output_file = sys.argv[3]

with open(input_file, "r") as f:
    data = yaml.safe_load(f)

if resource_type == "projects":
    formatted = format_projects(data)
elif resource_type == "inventories":
    formatted = format_inventories(data)
elif resource_type == "credentials":
    formatted = format_credentials(data)
# elif resource_type == "job_templates":
#     formatted = format_job_templates(data)
elif resource_type == "execution_environments":
    formatted = format_execution_environments(data)
elif resource_type == "inventory_sources":
    formatted = format_inventory_sources(data)
elif resource_type == "organizations":
    formatted = format_organizations(data)
# elif resource_type == "users":
#     formatted = format_users(data)
elif resource_type == "hosts":
    formatted = format_hosts(data)
elif resource_type == "groups":
    formatted = format_groups(data)
elif resource_type == "schedules":
    formatted = format_schedules(data)
elif resource_type == "credential_types":
    formatted = format_credential_types(data)
elif resource_type == "applications":
    formatted = format_applications(data)
elif resource_type == "teams":
    formatted = format_teams(data)
elif resource_type == "notifications":
    formatted = format_notifications(data)
else:
    print("Unsupported resource_type. Use: projects | inventories | credentials | job_templates | execution_environments | inventory_sources | organizations | users | hosts | groups | schedules | credential_types | applications | teams | notifications")
    sys.exit(1)

# Ensure output directory exists
output_dir = os.path.dirname(output_file)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Before writing the output file:
if os.path.exists(output_file):
    os.remove(output_file)

with open(output_file, "w") as f:
    f.write("---\n")
    yaml.dump(
        formatted,
        f,
        default_flow_style=False,
        sort_keys=False
    )