"""
This file contains the ComponentInstanceLink class, which is used to represent
a component instance link
"""
class ComponentInstanceLink:
    """
    A component instance link object, as defined at
    https://docs.serial.io/api-reference/component-instance-links/get-component-instance-link
    """
    def __init__(self, link_data):
        """
        Args:
        - link_data: A component instance link object, as defined at
        https://docs.serial.io/api-reference/component-instance-links/get-component-instance-link

        Returns:
        - A component instance link object (available at data), as ned at
        https://docs.serial.io/api-reference/component-instance-links/get-component-instance-link
        """
        self.data = link_data
