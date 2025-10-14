import yaml

def format_projects(data):
    formatted = {
        "controller_configuration_projects_async_retries": 60,
        "controller_configuration_projects_async_delay": 5,
        "controller_projects": []
    }
    for proj in data:
        formatted_proj = {
            "name": proj.get("name"),
            "scm_type": proj.get("scm_type", "git"),
            "scm_url": proj.get("scm_url"),
            "scm_branch": "main",
            "scm_clean": True,
            "description": proj.get("name"),
            "organization": proj.get("organization", {}).get("name", "Default"),
            "scm_update_on_launch": True,
            "wait": True,
            "update_project": True,
            "verbosity": 0
        }
        if proj.get("name") == "Demo Project":
            formatted_proj["state"] = "absent"
        formatted["controller_projects"].append(formatted_proj)
    return formatted

def format_inventories(data):
    inventories = []
    for inv in data:
        inventories.append({
            "name": inv.get("name"),
            "description": inv.get("description", ""),
            "organization": inv.get("organization", {}).get("name", "Default")
        })
    return {"controller_inventories": inventories}

def format_credentials(data):
    credentials = []
    for cred in data:
        cred_type = cred.get("credential_type", {}).get("name", "")
        org = cred.get("organization") or {}
        cred_obj = {
            "name": cred.get("name", cred_type),
            "description": cred.get("description", "created by Ansible"),
            "organization": org.get("name", "Default"),
            "credential_type": cred_type,
            "inputs": cred.get("inputs", {})
        }
        credentials.append(cred_obj)
    return {"controller_credentials": credentials}

def format_job_templates(data):
    templates_list = []
    for jt in data:
        jt_obj = {
            "name": jt.get("name"),
            "description": jt.get("description", ""),
            "job_type": jt.get("job_type", "run"),
            "inventory": jt.get("inventory"),
            "project": jt.get("project"),
            "playbook": jt.get("playbook"),
            "verbosity": jt.get("verbosity", 0)
        }
        # Optional fields
        if "state" in jt:
            jt_obj["state"] = jt["state"]
        if "credentials" in jt:
            jt_obj["credentials"] = jt["credentials"]
        if "execution_environment" in jt:
            jt_obj["execution_environment"] = jt["execution_environment"]
        if "extra_vars" in jt:
            jt_obj["extra_vars"] = jt["extra_vars"]
        if "webhook_service" in jt:
            jt_obj["webhook_service"] = jt["webhook_service"]
        if "webhook_credential" in jt:
            jt_obj["webhook_credential"] = jt["webhook_credential"]
        templates_list.append(jt_obj)
    return {"controller_templates": templates_list}

def format_execution_environments(data):
    ee_list = []
    for ee in data:
        ee_obj = {
            "name": ee.get("name"),
            "image": ee.get("image"),
            "pull": ee.get("pull", "always")
        }
        ee_list.append(ee_obj)
    return {"controller_execution_environments": ee_list}

def format_inventory_sources(data):
    formatted = {
        "controller_configuration_inventory_source_update_async_retries": 60,
        "controller_configuration_inventory_source_update_async_delay": 2,
        "controller_inventory_sources": []
    }
    for src in data:
        src_obj = {
            "name": src.get("name"),
            "source": src.get("source"),
            "inventory": src.get("inventory"),
            "organization": src.get("organization", "Default"),
            "credential": src.get("credential"),
            "overwrite": src.get("overwrite", True),
            "update_on_launch": src.get("update_on_launch", True),
            "update_cache_timeout": src.get("update_cache_timeout", 0),
            "wait": src.get("wait", True),
        }
        if "source_vars" in src:
            src_obj["source_vars"] = src["source_vars"]
        # Optionally include commented fields if present in input
        if "source_project" in src:
            src_obj["source_project"] = src["source_project"]
        if "source_path" in src:
            src_obj["source_path"] = src["source_path"]
        formatted["controller_inventory_sources"].append(src_obj)
    return formatted

def format_organizations(data):
    orgs = []
    for org in data:
        org_obj = {
            "name": org.get("name"),
            "description": "The default organization for Ansible Automation Platform" if org.get("name") == "Default" else org.get("description", ""),
            "galaxy_credentials": []
        }
        # Add static credentials for Default org, else parse from export
        if org.get("name") == "Default":
            org_obj["galaxy_credentials"] = ["certified", "validated", "Ansible Galaxy"]
        else:
            # Try to extract galaxy credentials from export if present
            creds = org.get("related", {}).get("galaxy_credentials", [])
            org_obj["galaxy_credentials"] = [c.get("name") for c in creds if c.get("name")]
        orgs.append(org_obj)
    return {"aap_organizations": orgs}

def format_users(data):
    return {"controller_users": data}

def parse_vars(variables):
    """Parse variables from string to dict if possible, else return as string."""
    if not variables or variables.strip() == "---":
        return {}
    try:
        return yaml.safe_load(variables)
    except Exception:
        return {"raw": variables}

def format_hosts(data):
    hosts_list = []
    for inv in data:
        inventory_name = inv.get("name")
        related = inv.get("related", {})
        hosts = related.get("hosts", [])
        for host in hosts:
            host_name = host.get("name")
            # Parse variables if present
            vars_dict = parse_vars(host.get("variables", ""))
            # Example: add a static variable for demonstration
            vars_dict["some_var"] = "some_val"
            hosts_list.append({
                "name": host_name,
                "inventory": inventory_name,
                "variables": vars_dict
            })
    return {"controller_hosts": hosts_list}

def format_groups(data):
    groups_list = []
    for inv in data:
        inventory_name = inv.get("name")
        related = inv.get("related", {})
        groups = related.get("groups", [])
        for group in groups:
            group_name = group.get("name")
            # Parse variables if present
            vars_dict = parse_vars(group.get("variables", ""))
            vars_dict["some_var"] = "some_val"
            vars_dict["ansible_connection"] = "local"
            group_obj = {
                "name": group_name,
                "inventory": inventory_name,
                "variables": vars_dict
            }
            # Add hosts if present
            hosts = group.get("related", {}).get("hosts", [])
            if hosts:
                group_obj["hosts"] = [h.get("name") for h in hosts]
            # Add children if present
            children = group.get("related", {}).get("children", [])
            if children:
                group_obj["children"] = [c.get("name") for c in children]
            groups_list.append(group_obj)
    return {"controller_groups": groups_list}