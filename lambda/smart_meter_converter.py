import json
from datetime import datetime

def lambda_handler(event, context):
    """
    Convert meter reading data between utility formats
    Input: Toronto Hydro proprietary format
    Output: Standard ANSI C12.19 format for inter-utility exchange
    """
    
    try:
        meter_data = event.get('meter_reading', {})
        
        toronto_format = {
            'meter_id': meter_data.get('meter_id'),
            'customer_id': meter_data.get('customer_id'),
            'reading_value': meter_data.get('reading_value'),
            'reading_date': meter_data.get('reading_date'),
            'utility_type': meter_data.get('utility_type')
        }
        
        ansi_format = {
            'deviceID': toronto_format['meter_id'],
            'accountNumber': toronto_format['customer_id'],
            'registerReading': {
                'value': toronto_format['reading_value'],
                'timestamp': toronto_format['reading_date'],
                'unit': get_unit_code(toronto_format['utility_type'])
            },
            'qualityCode': 'VALID',
            'dataSource': 'AMI_TORONTO_HYDRO',
            'conversionTimestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        print(f"Converted reading for meter {toronto_format['meter_id']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Meter data converted successfully',
                'input_format': 'Toronto Hydro Proprietary',
                'output_format': 'ANSI C12.19 Standard',
                'converted_data': ansi_format,
                'conversion_time': datetime.utcnow().isoformat()
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Data conversion failed',
                'message': str(e)
            })
        }

def get_unit_code(utility_type):
    """Map utility types to ANSI standard unit codes"""
    unit_mapping = {
        'electric': 'kWh',
        'gas': 'm3',
        'water': 'gal'
    }
    return unit_mapping.get(utility_type, 'UNK')
