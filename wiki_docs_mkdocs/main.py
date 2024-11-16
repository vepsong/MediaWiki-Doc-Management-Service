def define_env(env):
    """
    This is the hook for the variables, macros and filters.
    """
    env.variables['github_link'] = "https://github.com/vepsong/MediaWiki-Doc-Management-Service"
    env.variables['repository_name'] = "MediaWiki-Doc-Management-Service"

    env.variables['vm_0_full_name'] = "vm-0-service-virtual-machine"
    env.variables['vm_1_full_name'] = "vm-1-monitoring-system"
    env.variables['vm_2_full_name'] = "vm-2-nginx-proxy-server"
    env.variables['vm_3_full_name'] = "vm-3-mediawiki-server-1"
    env.variables['vm_4_full_name'] = "vm-4-mediawiki-server-2"
    env.variables['vm_5_full_name'] = "vm-5-haproxy-proxy-server"
    env.variables['vm_6_full_name'] = "vm-6-primary-db"
    env.variables['vm_7_full_name'] = "vm-7-standby-db"
    env.variables['vhdd_1_full_name'] = "vhdd-1-monitoring-system-db"
    env.variables['vhdd_2_full_name'] = "vhdd-2-standby-db" 
    env.variables['vhdd_3_full_name'] = "vhdd-3-dump-db" 
    env.variables['vssd_1_full_name'] = "vssd-1-primary-db"

    @env.macro
    def showTooltip(definition, description):
        """Generates HTML for a tooltip with customizable text."""
        return f'<span class="tooltip" onclick="showTooltip(event)">{definition}<span class="tooltip-text">{description}</span></span>'

    @env.macro
    def showTooltip_Direction(definition, description):
        """Generates HTML for a tooltip with customizable direction text."""
        return f'<span class="tooltip" onclick="showTooltip(event)">{definition}<span class="tooltip-text">``~/{env.variables["repository_name"]}{description}``</span></span>'

    @env.macro
    def showTooltip_VM_0():
        """Generates HTML for a tooltip with vm-0 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VM-0<span class="tooltip-text">{env.variables["vm_0_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VM_1():
        """Generates HTML for a tooltip with vm-1 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VM-1<span class="tooltip-text">{env.variables["vm_1_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VM_2():
        """Generates HTML for a tooltip with vm-2 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VM-2<span class="tooltip-text">{env.variables["vm_2_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VM_3():
        """Generates HTML for a tooltip with vm-3 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VM-3<span class="tooltip-text">{env.variables["vm_3_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VM_4():
        """Generates HTML for a tooltip with vm-4 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VM-4<span class="tooltip-text">{env.variables["vm_4_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VM_5():
        """Generates HTML for a tooltip with vm-5 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VM-5<span class="tooltip-text">{env.variables["vm_5_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VM_6():
        """Generates HTML for a tooltip with vm-6 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VM-6<span class="tooltip-text">{env.variables["vm_6_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VM_7():
        """Generates HTML for a tooltip with vm-7 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VM-7<span class="tooltip-text">{env.variables["vm_7_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VHDD_1():
        """Generates HTML for a tooltip with vm-7 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VHDD-1<span class="tooltip-text">{env.variables["vhdd_1_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VHDD_2():
        """Generates HTML for a tooltip with vm-7 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VHDD-2<span class="tooltip-text">{env.variables["vhdd_2_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VHDD_3():
        """Generates HTML for a tooltip with vm-7 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VHDD-3<span class="tooltip-text">{env.variables["vhdd_3_full_name"]}</span></span>'

    @env.macro
    def showTooltip_VSSD_1():
        """Generates HTML for a tooltip with vm-7 full name."""
        return f'<span class="tooltip" onclick="showTooltip(event)">VSSD-1<span class="tooltip-text">{env.variables["vssd_1_full_name"]}</span></span>'


    # # Print all configuration variables for debugging
    # print("Available config variables:")
    # for key in env.config:
    #     print(f"{key}: {env.config[key]}")

    # # Print all custom variables in env.variables
    # print("Available custom variables:")
    # for key, value in env.variables.items():
    #     print(f"{key}: {value}")


# def on_pre_page_macros(env):
#     """
#     Modify the content before rendering macros.
#     """
#     # footer = "\n\n---\n\nCopyright &copy; 2024 [Dmitrii Kirsanov]({{ github_link }})"
#     footer_content = "\n\n---\n\n<footer><div info' role='contentinfo'><p>Copyright &copy; 2024 <a href='{{ github_link }}'>Dmitrii Kirsanov</a></p></div></footer>"
#     env.markdown += footer_content
#     # env.markdown += footer
