EXISTING_IDENTIFIER_DATA = {
    'completed_at': None,
    'component': {
        'component_type': 'SN',
        'created_at': '2023-07-27T20:57:03.492568+00:00',
        'id': '96f59fb6-a801-4cc6-9b50-17e21f181482',
        'is_active': True,
        'last_edited_at': '2023-07-27T20:57:03.492568+00:00',
        'last_edited_user_id': None,
        'name': 'Test Process Upload Component',
        'pn_metadata_data_key_ids': []},
    'component_id': '96f59fb6-a801-4cc6-9b50-17e21f181482',
    'created_at': '2023-08-09T00:29:03.176814+00:00',
    'id': '95db48e1-99ad-4e35-a86b-fa0beca5f313',
    'identifier': 'test-1691540942131',
    'is_archived': False,
    'last_updated_at': '2023-08-09T00:29:04.482+00:00',
    'part_number': None,
    'part_number_id': None,
    'status': 'WIP',
    'work_order': None,
    'work_order_id': None}

NEW_IDENTIFIER_SAMPLE_DATA = {'completed_at': None,
    'component_id': '96f59fb6-a801-4cc6-9b50-17e21f181482',
    'created_at': '2023-10-06T19:42:14.716444+00:00',
    'id': 'b0a39740-97fe-48bd-b587-7d9b38af479f',
    'identifier': 'test-1696621334',
    'is_archived': False,
    'last_updated_at': '2023-10-06T19:42:14.716444+00:00',
    'part_number_id': None,
    'status': 'PLANNED',
    'work_order_id': None}

SAMPLE_NEW_LINK = {"broken_links":
                    [
                        {"id":"6cb414b7-3d11-4427-b49e-84f5abc0e51b",
                         "company_id":"0a9f1a55-5d27-4774-b9d8-3ba2e9dd2a25",
                         "unique_identifier_id":"1e8b0529-f2d1-4eac-9acf-b394497c8600",
                         "has_child_of_id":"95db48e1-99ad-4e35-a86b-fa0beca5f313",
                         "process_entry_id":"1963ff32-cfb8-48a9-9a6d-41c7bfdcb67c",
                         "is_active":False,
                         "data_key_id":"42eb0ebc-2d28-48a7-ac33-2f8a63bc45cf",
                         "created_at":"2023-10-04T18:37:39.331615+00:00",
                         "removed_at":"2023-10-06T20:35:28.850196+00:00"}
                    ],
                   "new_link":{
                       "id":"10fe089f-2cd2-4e69-b7d2-fc7f4574b608",
                       "unique_identifier_id":"465436b1-b777-47f9-9e49-53aff51a0dee",
                       "has_child_of_id":"f489336d-632b-4d8b-967d-3d36200e8026",
                       "process_entry_id":"1963ff32-cfb8-48a9-9a6d-41c7bfdcb67c",
                       "is_active": True,
                       "data_key_id":"42eb0ebc-2d28-48a7-ac33-2f8a63bc45cf",
                       "created_at":"2023-10-06T20:35:28.94124+00:00",
                       "removed_at":"null"}
                   }
SAMPLE_TEXT_DATA = {'created_at': '2023-10-06T21:26:25.830419+00:00',
                    'data_key_id': '4764ac60-eeab-48ed-a86c-9dd38cc703c3',
                    'id': 'bd528062-0735-4ae8-a2ca-da4165e948b2',
                    'process_entry_id': '114b846e-5d5e-4f96-87d2-6c029192053a',
                    'unique_identifier_id': '95db48e1-99ad-4e35-a86b-fa0beca5f313',
                    'value': "Bob's Burgers"}
SAMPLE_NUMBER_DATA = {'created_at': '2023-10-06T21:29:33.685368+00:00',
                      'data_key_id': 'ac69b740-5cbd-4d97-9363-eccc61e003c0',
                      'id': '685c5530-11b4-41b1-b62f-97cdbfc9ca5c',
                      'is_discrete': True,
                      'is_pass': True,
                      'lsl': 1,
                      'process_entry_id': '114b846e-5d5e-4f96-87d2-6c029192053a',
                      'unique_identifier_id': '95db48e1-99ad-4e35-a86b-fa0beca5f313',
                      'unit': 'ft',
                      'usl': 2,
                      'value': 1.5}
SAMPLE_FILE_DATA = {'bucket_name': 'data-files',
                    'created_at': '2023-10-06T21:36:47.814916+00:00',
                    'data_key_id': 'f38f7410-16ab-4e26-a220-487703e0db05',
                    'file_id': '30567984-68e4-44c0-9781-1b18d8ef004f',
                    'file_name': 'test.txt',
                    'format': 'OTHER',
                    'id': '90438dab-f84d-4875-a1da-21e5b1b6f19d',
                    'process_entry_id': '114b846e-5d5e-4f96-87d2-6c029192053a',
                    'unique_identifier_id': '95db48e1-99ad-4e35-a86b-fa0beca5f313'}
SAMPLE_IMAGE_DATA = {
            'bucket_name': 'data-images',
            'created_at': '2023-10-06T21:40:02.435441+00:00',
            'data_key_id': '088befe0-171e-40bc-957b-686f3de01b51',
            'file_id': '4042fc9a-d7c9-4780-ae97-dc20c41c2793',
            'file_name': 'image.png',
            'id': 'cff92794-c66c-42b1-8269-220f36f30958',
            'process_entry_id': '8394c7d3-0615-4e55-890e-68e7e9bb74b9',
            'unique_identifier_id': '95db48e1-99ad-4e35-a86b-fa0beca5f313',        
            }
SAMPLE_BOOLEAN_DATA = {
            'created_at': '2023-10-06T21:43:13.251893+00:00',
            'data_key_id': 'b8b38d13-2931-4ab6-8e73-8ee65d3803fb',
            'id': '63a14fa5-7bf2-4c71-a197-a46bc90fd0ce',
            'is_checked': True,
            'is_pass': False,
            'process_entry_id': '556d3ddb-dabc-4f3d-97ce-b5f876382692',
            'prompt': '',
            'unique_identifier_id': '95db48e1-99ad-4e35-a86b-fa0beca5f313'
            }
SAMPLE_ENTRY_DATA = {
            'cycle_time': 50,
            'id': '9241242c-e334-4fe9-86f4-a3e2b1578f38',
            'is_pass': True,
            'operator_id': None,
            'override_user_id': None,
            'process_id': '9ecb9747-22d9-49eb-b5c1-1d9fff3fa6b8',
            'process_revision': None,
            'station_id': None,
            'timestamp': '2023-10-06T21:51:54.549684+00:00',
            'unique_identifier_id': '95db48e1-99ad-4e35-a86b-fa0beca5f313',
            'upload_error': False
            }
