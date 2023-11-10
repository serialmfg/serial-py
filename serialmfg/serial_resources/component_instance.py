"""
This file contains the ComponentInstance class, which represents a component instance
"""
from ..api_client import APIClient
from .component_instance_link import ComponentInstanceLink

class ComponentInstance:
    """
    A component instance object, as defined at
    https://docs.serial.io/api-reference/component-instances/get-component-instance
    """
    def __init__(self, component_instance_data):
        """
        Args:
        - component_instance_data: A component instance object, as defined at
        https://docs.serial.io/api-reference/component-instances/get-component-instance
        
        Returns:
        - A component instance python object, which holds the api object at data,
        its links created during this session at created_links, and the client
        """
        self.client = APIClient()
        self.data = component_instance_data
        self.created_links = [] 

    def add_link(self, link_name, child_identifier, break_prior_links=False, process_entry=None):
        """
        Creates a link between this component instance and a child at a specific
        process_entry

        Args: 
        - link_name: User facing name for the link
        - child_identifier: Identifier for the child component instance to be linked
        - break_prior_links?: Boolean for whether to break prior links
        - process_entry?: Override for the process entry this component instance object 
        was created with. Must be included if this component instance object was not 
        created with a process entry.

        Returns:
        - New component instance link
        """

        # TODO: debug logging
        #print(f"Adding link: {link_name} with child identifier: {child_identifier}")
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
                "parent_component_instance_id": self.data["id"],
                "child_component_instance_id": child_component_instance["id"],
                "dataset_id": link_dataset["id"],
                "process_entry_id": process_entry_id,
                "break_prior_links": break_prior_links,
                }
        new_link = ComponentInstanceLink(self.client.make_api_request("/components/instances/links", "PUT", data=data)) 
        self.created_links.append(new_link)
        return new_link

class ComponentInstances:
    """
    A class for component instance data methods
    """
    @staticmethod
    def get(identifier):
        """
        Gets a component instance, if it exists
        
        Args:
        - identifier: Component's user facing identifier

        Returns:
        - A component instance object 
        """
        client = APIClient() 
        # TODO: debug logging
        #print(f"Getting component instance: {identifier}")
        return ComponentInstance(client.make_api_request(f"/components/instances/{identifier}", "GET"))
    
    @staticmethod
    def create(identifier, component_name):
        """
        Creates a component instance
        
        Args:
        - identifier: Component's user facing identifier
        - component_name: User facing name for the component
            
        Returns:
        - A component instance, as defined at 
        https://docs.serial.io/api-reference/component-instances/get-component-instance
        """
        # TODO: debug logging
        #print(f"Creating component instance: {identifier} with component name: {component_name}")
        client = APIClient() 
        # Get the component id for the given component name
        component_name_params = {
                "name" : component_name,
                }
        component_id = client.make_api_request("/components",
                                                     "GET",
                                                     params=component_name_params)[0]["id"]
        data = {
                "component_id": component_id,
                "identifier": identifier,
                }
        return ComponentInstance(client.make_api_request(f"/components/instances", "PUT", data=data)) 

    @staticmethod
    def list(query_params):
        """
        Lists component instances

        Args:
        - query_params: A dictionary of query parameters, as defined at
        https://docs.serial.io/api-reference/component-instances/get-component-instance

        Returns:
        - A list of component instances, as defined at
        https://docs.serial.io/api-reference/component-instances/get-component-instance
        """
        # TODO: debug logging
        #print(f"Listing component instances with query params: {query_params}")

        client = APIClient()
        instances = client.make_api_request("/components/instances", "GET", params=query_params)
        instance_object_list = [ComponentInstance(instance) for instance in instances]
        return instance_object_list 
