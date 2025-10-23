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
            "description": sched.get("description", ""),
            "rrule": sched.get("rrule"),
            "extra_data": sched.get("extra_data") if "extra_data" in sched else None,
            "inventory": (sched.get("inventory", {}) or {}).get("name") if isinstance(sched.get("inventory"), dict) else sched.get("inventory"),
            "credentials": [],
            "scm_branch": sched.get("scm_branch") if "scm_branch" in sched else None,
            "execution_environment": ((sched.get("execution_environment") or {}).get("name")
                                      if isinstance(sched.get("execution_environment"), dict)
                                      else sched.get("execution_environment")),
            "forks": sched.get("forks") if "forks" in sched else None,
            "instance_groups": sched.get("instance_groups", []),
            "job_slice_count": sched.get("job_slice_count") if "job_slice_count" in sched else None,
            "labels": None,
            "timeout": sched.get("timeout") if "timeout" in sched else None,
            "job_type": sched.get("job_type") if "job_type" in sched else None,
            "job_tags": sched.get("job_tags") if "job_tags" in sched else None,
            "skip_tags": sched.get("skip_tags") if "skip_tags" in sched else None,
            "limit": sched.get("limit") if "limit" in sched else None,
            "diff_mode": sched.get("diff_mode") if "diff_mode" in sched else None,
            "verbosity": sched.get("verbosity") if "verbosity" in sched else None,
            "organization": (sched.get("organization", {}) or {}).get("name") if isinstance(sched.get("organization"), dict) else sched.get("organization"),
            "unified_job_template": (sched.get("unified_job_template", {}) or {}).get("name"),
            "enabled": sched.get("enabled") if "enabled" in sched else None,
        }

        creds = sched.get("related", {}).get("credentials", [])
        sched_obj["credentials"] = [c.get("name") for c in creds if c.get("name")]

        schedules.append(sched_obj)
    return {"controller_schedules": schedules}

def format_job_templates(data):
    print("This function is not complet right now, so used with caution")

    templates_list = []
    for jt in data:
        jt_obj = {
            "name": jt.get("name"),
            "copy_from": jt.get("copy_from") if "copy_from" in jt else None,
            "description": jt.get("description", ""),
            "execution_environment": (jt.get("execution_environment", {}) or {}).get("name") if isinstance(jt.get("execution_environment"), dict) else jt.get("execution_environment"),
            "custom_virtualenv": jt.get("custom_virtualenv") if "custom_virtualenv" in jt else None,
            "job_type": jt.get("job_type", "run"),
            "inventory": (jt.get("inventory", {}) or {}).get("name") if isinstance(jt.get("inventory"), dict) else jt.get("inventory"),
            "organization": jt.get("natural_key").get("organization").get("name"),
            "project": (jt.get("project", {}) or {}).get("name") if isinstance(jt.get("project"), dict) else jt.get("project"),
            "playbook": jt.get("playbook"),
            "forks": jt.get("forks") if "forks" in jt else None,
            "limit": jt.get("limit") if "limit" in jt else None,
            "verbosity": jt.get("verbosity", 0) if ("verbosity" in jt or True) else None,
            "extra_vars": parse_vars(jt.get("extra_vars")) if isinstance(jt.get("extra_vars"), str) else jt.get("extra_vars", None),
            "job_tags": jt.get("job_tags") if "job_tags" in jt else None,
            "force_handlers": jt.get("force_handlers") if "force_handlers" in jt else None,
            "skip_tags": jt.get("skip_tags") if "skip_tags" in jt else None,
            "start_at_task": jt.get("start_at_task") if "start_at_task" in jt else None,
            "diff_mode": jt.get("diff_mode") if "diff_mode" in jt else None,
            "use_fact_cache": jt.get("use_fact_cache") if "use_fact_cache" in jt else None,
            "host_config_key": jt.get("host_config_key") if "host_config_key" in jt else None,
            "ask_scm_branch_on_launch": jt.get("ask_scm_branch_on_launch") if "ask_scm_branch_on_launch" in jt else None,
            "ask_diff_mode_on_launch": jt.get("ask_diff_mode_on_launch") if "ask_diff_mode_on_launch" in jt else None,
            "ask_variables_on_launch": jt.get("ask_variables_on_launch") if "ask_variables_on_launch" in jt else None,
            "ask_limit_on_launch": jt.get("ask_limit_on_launch") if "ask_limit_on_launch" in jt else None,
            "ask_tags_on_launch": jt.get("ask_tags") if "ask_tags" in jt or "ask_tags_on_launch" in jt else None,
            "ask_skip_tags_on_launch": jt.get("ask_skip_tags") if "ask_skip_tags" in jt or "ask_skip_tags_on_launch" in jt else None,
            "ask_job_type_on_launch": jt.get("ask_job_type_on_launch") if "ask_job_type_on_launch" in jt else None,
            "ask_verbosity_on_launch": jt.get("ask_verbosity_on_launch") if "ask_verbosity_on_launch" in jt else None,
            "ask_inventory_on_launch": jt.get("ask_inventory_on_launch") if "ask_inventory_on_launch" in jt else None,
            "ask_credential_on_launch": jt.get("ask_credential_on_launch") if "ask_credential_on_launch" in jt else None,
            "ask_execution_environment_on_launch": jt.get("ask_execution_environment_on_launch") if "ask_execution_environment_on_launch" in jt else None,
            "ask_forks_on_launch": jt.get("ask_forks_on_launch") if "ask_forks_on_launch" in jt else None,
            "ask_instance_groups_on_launch": jt.get("ask_instance_groups_on_launch") if "ask_instance_groups_on_launch" in jt else None,
            "ask_job_slice_count_on_launch": jt.get("ask_job_slice_count_on_launch") if "ask_job_slice_count_on_launch" in jt else None,
            "ask_labels_on_launch": jt.get("ask_labels_on_launch") if "ask_labels_on_launch" in jt else None,
            "ask_timeout_on_launch": jt.get("ask_timeout_on_launch") if "ask_timeout_on_launch" in jt else None,
            "prevent_instance_group_fallback": jt.get("prevent_instance_group_fallback") if "prevent_instance_group_fallback" in jt else None,
            "survey_enabled": jt.get("survey_enabled") if "survey_enabled" in jt else None,
            "become_enabled": jt.get("become_enabled") if "become_enabled" in jt else None,
            "allow_simultaneous": jt.get("allow_simultaneous") if "allow_simultaneous" in jt else None,
            "timeout": jt.get("timeout") if "timeout" in jt else None,
            "instance_groups": jt.get("instance_groups", []),
            "job_slice_count": jt.get("job_slice_count") if "job_slice_count" in jt else None,
            "webhook_service": jt.get("webhook_service") if "webhook_service" in jt else None,
            "webhook_credential": (jt.get("webhook_credential", {}) or {}).get("name") if isinstance(jt.get("webhook_credential"), dict) else jt.get("webhook_credential"),
            "scm_branch": jt.get("scm_branch") if "scm_branch" in jt else None,
            "labels": ((jt.get("related") or {}).get("labels")),
            "state": jt.get("state") if "state" in jt else None,
            "notification_templates_started": parse_notification_templates((jt.get("related") or {}).get("notification_templates_started")),
            "notification_templates_success": parse_notification_templates((jt.get("related") or {}).get("notification_templates_success")),
            "notification_templates_error": parse_notification_templates((jt.get("related") or {}).get("notification_templates_error")),
            "survey_spec": (jt.get("related") or {}).get("survey_spec") or jt.get("survey_spec") or jt.get("survey")
        }

        # credentials: prefer direct field, fallback to related.credentials, return only names
        creds = jt.get("related", {}).get("credentials", [])
        jt_obj["credentials"] = [c.get("name") for c in creds if c.get("name")]

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
            "notification_templates_started": parse_notification_templates(src.get("related").get("notification_templates_started")),
            "notification_templates_success": parse_notification_templates(src.get("related").get("notification_templates_success")),
            "notification_templates_error": parse_notification_templates(src.get("related").get("notification_templates_error"))
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