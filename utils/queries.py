from utils.db_client import DatabaseClient
import logging
      
class Queries:


       def get_channel_info_by_reference_id(self, external_reference):


              GET_any_INFO_BY_EXTERNAL_REFERENCE_ID_QUERY = f"SELECT [asdsa],[asdsa],[staasdsrt],[asd],[asd],[language] FROM [asd].[dbo].[channel] WHERE [externalReference] = '{external_reference}'"
            
              db_client = DatabaseClient()
              project_details_dict = db_client.get_db_data_as_dict(GET_any_INFO_BY_EXTERNAL_REFERENCE_ID_QUERY)
             
              db_client.close()

              return project_details_dict
       
       
       def delete_channel_info_by_reference_id(self, external_reference_id):
              DELETE_ANY_INFO_BY_EXTERNAL_REFERENCE_ID_QUERY = f"""
                     DELETE
                     FROM [opera_db].[dbo].[channel]
                     WHERE externalReference = '{external_reference_id}'
              """
            
              db_client = DatabaseClient()
              channeldetails_dict = db_client.execute_query(DELETE_ANY_INFO_BY_EXTERNAL_REFERENCE_ID_QUERY)
              db_client.close()
             
              
              if channeldetails_dict == "No data found":
                     return "channel deletion failed"