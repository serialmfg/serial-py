class ComponentInstance:
    def __init__(self, client, identifier, component, process_entry=None):
        """
        Creates a new component instance
        If the client alows, this will create a new component instance in 
        Serial. If not permitted by the client, it must be a component instance 
        that has already been created.

        Args:
        - client: a Serial client object
        - identifier: Component Instance's identifier 
        - component: Component Instance's new component name

        Returns:
        - A new component instance object 
        """
        self.client = client
        self.identifier = identifier
        self.component = component
        self.process_entry = process_entry 
        if self.client.allow_component_instance_creation:
            pass
        else:
            pass

    
    def add_link(self, link_name, child_identifier, process_entry=None):
        """
        Creates a link between this component instance and a child at a specific
        process_entry

        Args: 
        - link_name: User facing name for the link
        - child_identifier: Identifier for the child component instance to be linked
        - process_entry?: Override for the process entry this component instance object 
        was created with. Must be included if this component instance object was not 
        created with a process entry.

        Returns:
        - New component instance link
        """
        if self.client.debug:
            print(f"Adding link: {link_name} with child identifier: {child_identifier}")
        pass

