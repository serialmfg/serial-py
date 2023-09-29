import requests

class ComponentInstance:
    def __init__(self, client, identifier, component_name=None, process_entry=None):
        """
        Creates a new component instance
        If the client alows, this will create a new component instance in 
        Serial. If not permitted by the client, it must be a component instance 
        that has already been created.

        Args:
        - client: a Serial client object
        - identifier: Component Instance's identifier 
        - component_name: Component Instance's new component name

        Returns:
        - A new component instance object 
        """
        self.client = client
        self.identifier = identifier
        self.component_name = component_name
        self.process_entry = process_entry 
        self.component_instance = None
        try:
            self.component_instance = self._get_component_instance(identifier);
        except requests.exceptions.HTTPError as http_err:
            print(f"Component with identifier {identifier} not found, {'Creating...' if self.client.allow_component_instance_creation else 'Please create the component in Serial'}")
        if self.client.allow_component_instance_creation and not self.component_instance:
            self.component_instance = self._create_component_instance(identifier, component_name)

    def _get_component_instance(self, identifier):
        """
        Gets a component instance, if it exists
        
        Args:
        - identifier: Component's user facing identifier

        Returns:
        - A component instance, as defined at 
        https://docs.serial.io/api-reference/component-instances/get-component-instance
        """
        if self.client.debug:
            print(f"Getting component instance: {identifier}")
        pass
        return self.client.make_api_request(f"/components/instances/{identifier}", "GET")
    
    def _create_component_instance(self, identifier, component_name):
        """
        Creates a component instance
        
        Args:
        - identifier: Component's user facing identifier
        - component_name: User facing name for the component
            
        Returns:
        - A component instance, as defined at 
        https://docs.serial.io/api-reference/component-instances/get-component-instance
        """
        if self.client.debug:
            print(f"Creating component instance: {identifier} with component name: {component_name}")
        pass
        # Get the component id for the given component name
        component_name_params = {
                "name" : component_name,
                }
        component_id = self.client.make_api_request("/components",
                                                     "GET",
                                                     params=component_name_params)[0]["id"]
        data = {
                "component_id": component_id,
                "identifier": identifier,
                }
        return self.client.make_api_request(f"/components/instances"
                                             , "PUT", data=data) 
    
    def add_link(self, link_name, child_identifier, break_prior_links=False, process_entry=None):
        """
        Creates a link between this component instance and a child at a specific
        process_entry

        Args: 
        - link_name: User facing name for the link
        - child_identifier: Identifier for the child component instance to be linked
        - break_prior_links: Boolean for whether to break prior links
        - process_entry?: Override for the process entry this component instance object 
        was created with. Must be included if this component instance object was not 
        created with a process entry.

        Returns:
        - New component instance link
        """

        if self.client.debug:
            print(f"Adding link: {link_name} with child identifier: {child_identifier}")
        child_component_instance_params = {
                "identifier": child_identifier
                }
        link_params = {
                "name": link_name
                }
        child_component_instance = self.client.make_api_request("/components/instances",
                                                                "GET",
                                                                params=child_component_instance_params)[0]
        link_dataset = self.client.make_api_request("/datasets",
                                                    "GET",
                                                    params=link_params)[0]
        process_entry_id = None
        if process_entry:
            process_entry_id = process_entry.id
        else:
            process_entry_id = self.process_entry.id
        data = {
                "parent_component_instance_id": self.component_instance["id"],
                "child_component_instance_id": child_component_instance["id"],
                "dataset_id": link_dataset["dataset"]["id"],
                "process_entry_id": process_entry_id,
                "break_prior_links": break_prior_links,
                }
        return self.client.make_api_request("/components/instances/links",
                                            "PUT",
                                            data=data) 
