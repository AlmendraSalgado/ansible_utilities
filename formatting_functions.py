import yaml

def parse_notification_templates(data):
    if not data:
        return []
    
    notif_list: list[str] = []
    for notif in data:
        notif_list.append(notif.get("name"))

    return notif_list

def parse_vars(variables):
    """Parse variables from string to dict if possible, else return as string."""
    if not variables or variables.strip() == "---":
        return {}
    try:
        return yaml.safe_load(variables)
    except Exception:
        return {"raw": variables}

def format_projects(data):
    formatted = {
        "controller_configuration_projects_async_retries": 60,
        "controller_configuration_projects_async_delay": 5,
        "controller_projects": []
    }
    for proj in data:
        formatted_proj = {
            "name": proj.get("name"),
            "scm_type": proj.get("scm_type"),
            "allow_override": proj.get("allow_override"),
            "credential": proj.get("credential").get("name"),
            "default_environment": (proj.get("default_environment", "") or {}).get("name"),
            "notification_templates_started": parse_notification_templates(proj.get("related").get("notification_templates_started")),
            "notification_templates_success": parse_notification_templates(proj.get("related").get("notification_templates_success")),
            "notification_templates_error": parse_notification_templates(proj.get("related").get("notification_templates_error")),
            "scm_delete_on_update": proj.get("scm_delete_on_update"),
            "scm_refspec": proj.get("scm_refspec"),
            "scm_track_submodules": proj.get("scm_track_submodules"),
            "scm_update_cache_timeout": proj.get("scm_update_cache_timeout"),
            "scm_branch": proj.get("scm_branch"),
            "scm_clean": proj.get("scm_clean"),
            "description": proj.get("name"),
            "local_path": proj.get("local_path"),
            "organization": proj.get("organization", {}).get("name", "Default"),
            "scm_update_on_launch": proj.get("scm_update_on_launch"),
            "signature_validation_credential": proj.get("signature_validation_credential"),
            "timeout": proj.get("timeout"),
            "scm_url": proj.get("scm_url")
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
            "kind": inv.get("kind"),
            "host_filter": inv.get("host_filter", ""),
            "instance_groups": inv.get("instance_groups", []),
            "prevent_instance_group_fallback": inv.get("prevent_instance_group_fallback"),
            "variables": parse_vars(inv.get("variables", {})),
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

def format_schedules(data):
    schedules = []
    for sched in data:
        sched_obj = {
            "name": sched.get("name"),
            "description": sched.get("description"),
            "unified_job_template": sched.get("unified_job_template"),
            "rrule": sched.get("rrule"),
            "limit": sched.get("limit"),
            "execution_environment": (sched.get("default_environment", "") or {}).get("name"),
            "forks": sched.get("forks"),
            "instance_groups": sched.get("instance_groups", {}),
            "labels": sched.get("labels", {}),
            "timeout": sched.get("instance_groups")
        }
        schedules.append(sched_obj)
    return {"controller_schedules": schedules}

def format_job_templates(data):
    print("This function is not complet right now, so used with caution")
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

def format_credential_types(data):
    credential_types = []
    for cred_type in data:
        cred_type_obj = {
            "name": cred_type.get("name"),
            "description": cred_type.get("description"),
            "kind": cred_type.get("kind"),
            "inputs": cred_type.get("inputs", {}),
            "injectors": cred_type.get("injectors", {})
        }
        credential_types.append(cred_type_obj)
    return {"controller_credential_types": credential_types}

def format_notifications(data):
    notifications = []
    for notif in data:
        notif_obj = {
            "name": notif.get("name"),
            "description": notif.get("description"),
            "organization": notif.get("organization", {}).get("name", "Default"),
            "notification_type": notif.get("notification_type"),
            "notification_configuration": notif.get("notification_configuration", {}),
            "messages": notif.get("messages", {})
        }
        notifications.append(notif_obj)
    return {"controller_notifications": notifications}

def format_teams(data):
    teams = []
    for team in data:
        team_obj = {
            "name": team.get("name"),
            "organization": team.get("organization", {}).get("name", "Default")
        }
        teams.append(team_obj)
    return {"aap_teams": teams}

def format_applications(data):
    applications = []
    for app in data:
        app_obj = {
            "name": app.get("name"),
            "description": app.get("description"),
            "organization": app.get("organization", {}).get("name", "Default"),
            "authorization_grant_type": app.get("authorization_grant_type"),
            "client_type": app.get("client_type"),
            "redirect_uris": app.get("redirect_uris", {}),
            "skip_authorization": app.get("skip_authorization")
        }
        applications.append(app_obj)
    return {"aap_applications": applications}

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
            "description": src.get("description"),
            "source": src.get("source"),
            "source_path": src.get("source_path", ""),
            "source_vars": parse_vars(src.get("source_vars", {})),
            "enabled_var": src.get("enabled_var", ""),
            "enabled_value": src.get("enabled_value", ""),
            "host_filter": src.get("host_filter", ""),
            "limit": src.get("limit", ""),
            "execution_environment": (src.get("execution_environment", "") or {}).get("name"),
            "overwrite_vars": src.get("overwrite_vars", ""),
            "custom_virtualenv": src.get("custom_virtualenv", ""),
            "timeout": src.get("timeout", ""),
            "verbosity": src.get("verbosity", ""),
            "scm_branch": src.get("scm_branch", ""),
            "source_project": src.get("source_project").get("name", ""),
            "inventory": src.get("inventory").get("name"),
            "organization": src.get("inventory").get("organization").get("name"),
            "credential": (src.get("credential", "") or {}).get("name"),
            "overwrite": src.get("overwrite", True),
            "update_on_launch": src.get("update_on_launch", True),
            "update_cache_timeout": src.get("update_cache_timeout", 0),
            "wait": src.get("wait", True),
            "notification_templates_started": parse_notification_templates(src.get("notification_templates_started")),
            "notification_templates_success": parse_notification_templates(src.get("notification_templates_started")),
            "notification_templates_error": parse_notification_templates(src.get("notification_templates_started"))
        }

        formatted["controller_inventory_sources"].append(src_obj)
    return formatted

def format_organizations(data):
    orgs = []
    for org in data:
        org_obj = {
            "name": org.get("name"),
            "description": org.get("description", ""),
            "custom_virtualenv": org.get("custom_virtualenv", ""),
            "max_hosts": org.get("max_hosts", ""),
            "instance_groups": org.get("instance_groups", []),
            "default_environment": (org.get("default_environment", "") or {}).get("name"),
            "galaxy_credentials": [],
            "notification_templates_started": org.get("notification_templates_started", []),
            "notification_templates_success": org.get("notification_templates_started", []),
            "notification_templates_error": org.get("notification_templates_started", [])
        }
        # Parse static credentials from export
        creds = org.get("related", {}).get("galaxy_credentials", [])
        org_obj["galaxy_credentials"] = [c.get("name") for c in creds if c.get("name")]

        orgs.append(org_obj)
    return {"aap_organizations": orgs}

def format_users(data):
    return {"controller_users": data}

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