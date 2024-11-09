def define_env(env):
    """
    This is the hook for the variables, macros and filters.
    """
    env.variables['github_link'] = "https://github.com/vepsong/MediaWiki-Doc-Management-Service"

    @env.macro
    def price(unit_price, no):
        "Calculate price"
        return unit_price * no

    @env.macro
    def showTooltip(definition, description):
        """Generates HTML for a tooltip with customizable text."""
        return f'<span class="tooltip" onclick="showTooltip(event)">{definition}<span class="tooltip-text">{description}</span></span>'
    
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
