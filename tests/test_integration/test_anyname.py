from utils.api_client import APIClient
import logging
import pytest
from datetime import datetime
from tests.conftest import load_config
from utils.data_generator import DataGenerator
from models.channels; import channels

import json
from utils.queries import Queries
import time

@pytest.mark.staging
def test_create_channel(api_client,config):

    channel = channel()
    data_generator = DataGenerator()
    channel.name = data_generator.generate_channel_name()
    channel.reference_id = data_generator.generate_channel_reference_id()
    channel.start_date = data_generator.generate_channel_start_date(weekscount=0)
    channel.end_date = data_generator.generate_channel_end_date(weekscount=2)
    channel.description = data_generator.generate_channel_description()
    channel.language = "en" 
    
    channel_user_request_json = channel.to_dict()

    no_of_users = 5
    users = []
    for i in range(no_of_users):

        user = user()
        user.name = data_generator.user_name()
        user.reference_id = data_generator.user_reference_id()
        user.source_reference_id = data_generator.source_reference_id('KSC-2025')#create source user and use it
        user.start_date = data_generator.generate_user_start_date(channel.start_date)
        user.end_date = data_generator.generate_user_end_date(channel.end_date)
        user.description = data_generator.generate_user_description()
        user.length = 4
        user.frequency = data_generator.generate_user_frequency()

        user_request_json = user.to_dict()

        users.append(user_request_json)


    channel_user_request_json['users']= users

    logging.info(f"channel json: {channel_user_request_json}")

    channel_user_response = api_client.post("/channels",json_data=channel_user_request_json)

    assert channel_user_response.status_code == 201 , f"channel- user creation failed with status code {channel_user_response.status_code}"

    logging.info(f"channel created started verifying the channel details in the response and request")

    assert channel_user_response.json()['data']['name'] == channel_user_request_json['name'], f"channel name mismatch. Expected: {channel_user_request_json['name']}, Actual: {channel_user_response.json()['data']['name']}"
    assert channel_user_response.json()['data']['reference_id']== channel_user_request_json['reference_id'], f"channel reference id mismatch. Expected: {channel_user_request_json['reference_id']}, Actual: {channel_user_response.json()['data']['reference_id']}"
    assert channel_user_response.json()['data']['start_date'].split("T")[0] == channel_user_request_json['start_date'], f"channel start date mismatch. Expected: {channel_user_request_json['start_date']}, Actual: {channel_user_response.json()['data']['start_date']}"
    assert channel_user_response.json()['data']['end_date'].split("T")[0] == channel_user_request_json['end_date'], f"channel end date mismatch. Expected: {channel_user_request_json['end_date']}, Actual: {channel_user_response.json()['data']['end_date']}"
    assert channel_user_response.json()['data']['language'] == channel_user_request_json['language'], f"channel languages mismatch. Expected: {channel_user_request_json['languages']}, Actual: {channel_user_response.json()['data']['languages']}"
    
    
    logging.info(f"Created users veification response and request started")

    for request, response in zip(channel_user_request_json['users'], channel_user_response.json()['data']['users']):

        if request['reference_id'] == response['reference_id']:
            assert request['name'] == response['name'], f"user name mismatch. Expected: {request['name']}, Actual: {response['name']}"
            assert request['reference_id'] == response['reference_id'], f"user source reference id mismatch. Expected: {request['source_reference_id']}, Actual: {response['source_reference_id']}"
            assert request['start_date'] == response['start_date'].split("T")[0], f"user start date mismatch. Expected: {request['start_date']}, Actual: {response['start_date'].split('T')[0]}"
            assert request['end_date'] == response['end_date'].split("T")[0], f"user end date mismatch. Expected: {request['end_date']}, Actual: {response['end_date'].split('T')[0]}"
            assert request['length'] == response['length'], f"user length mismatch. Expected: {request['length']}, Actual: {response['length']}"
            assert request['frequency'] == response['frequency'], f"user frequency mismatch. Expected: {request['frequency']}, Actual: {response['frequency']}"

    
    channel_info_dict = Queries().get_channel_info_by_reference_id(channel_user_request_json['reference_id'])
    channel_info_db_list = channel_info_dict[0]
    assert len(channel_info_dict) > 0, f"channel details not found in the database"

    logging.info(f"Created channel veification request data with db started")

    assert channel_info_db_list['name'] == channel_user_request_json['name'], f"channel name mismatch. Expected: {channel.name}, Actual: {channel_info_dict[0]['name']}"
    assert channel_info_db_list['externalReference'] == channel_user_request_json['reference_id'], f"channel reference id mismatch. Expected: {channel.reference_id}, Actual: {channel_info_dict[0]['externalReference']}"
    assert channel_info_db_list['description'] == channel_user_request_json['description'], f"channel description mismatch. Expected: {channel.description}, Actual: {channel_info_dict[0]['description']}"
    assert channel_info_db_list['start'].strftime("%Y-%m-%d") == channel_user_request_json['start_date'], f"channel start date mismatch. Expected: {channel.start_date}, Actual: {channel_info_dict[0]['start'].strftime('%Y-%m-%d')}"
    assert channel_info_db_list['end'].strftime("%Y-%m-%d") == channel_user_request_json['end_date'], f"channel end date mismatch. Expected: {channel.end_date}, Actual: {channel_info_dict[0]['end'].strftime('%Y-%m-%d')}"
    assert channel_info_db_list['language'] == channel_user_request_json['language'], f"channel languages mismatch. Expected: {channel_user_request_json['languages']}, Actual: {channel_info_dict[0]['languages']}"


    logging.info(f"Created users veification request data with db started")

    channel_info_dict = Queries().get_channel_info_by_reference_id(channel_user_request_json['reference_id'])
    channel_info_db_list = channel_info_dict[0]
    assert len(channel_info_dict) > 0, f"channel details not found in the database"