class Identifier: 
    def __init__(self, identifier, component, part_number=None):
        """
        Initializes a new Identifier object.

        Args:
        - identifier: The identifier for the object.
        - component: The component for the object.
        - part_number: The part number for the object.

        Returns:
        - A new Identifier object.
        """
        self.identifier = identifier
        self.component = component
        self.part_number = part_number