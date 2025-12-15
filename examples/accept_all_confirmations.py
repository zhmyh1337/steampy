"""
Example script to accept all pending Steam confirmations.
This script will fetch all pending confirmations and accept them automatically.
"""
import os
import time
from dotenv import load_dotenv

from steampy.client import SteamClient
from steampy.confirmation import ConfirmationExecutor

# Load environment variables from .env file
load_dotenv()

# Set API key
api_key = os.getenv('STEAM_API_KEY', '')
# Set path to SteamGuard file
steamguard_path = os.getenv('STEAM_GUARD_PATH', '')
# Steam username
username = os.getenv('STEAM_USERNAME', '')
# Steam password
password = os.getenv('STEAM_PASSWORD', '')


def main() -> None:
    print('This script accepts all pending confirmations.')

    if not are_credentials_filled():
        print('You have to fill credentials in .env file to run the example')
        print('Required: STEAM_API_KEY, STEAM_USERNAME, STEAM_PASSWORD, STEAM_GUARD_PATH')
        return

    # Login to Steam
    print('Logging in...')
    client = SteamClient(api_key)
    client.login(username, password, steamguard_path)
    print('Login successful!')

    # Create confirmation executor
    confirmation_executor = ConfirmationExecutor(
        client.steam_guard['identity_secret'],
        client.steam_guard['steamid'],
        client._session
    )

    # Get all pending confirmations
    print('Fetching confirmations...')
    try:
        confirmations = confirmation_executor._get_confirmations()
        print(f'Found {len(confirmations)} pending confirmation(s)')

        if not confirmations:
            print('No pending confirmations found.')
            return

        # Accept each confirmation with a small delay to avoid rate limiting
        accepted_count = 0
        failed_count = 0
        for i, confirmation in enumerate(confirmations, 1):
            try:
                print(f'[{i}/{len(confirmations)}] Accepting confirmation {confirmation.data_confid}...')
                result = confirmation_executor._send_confirmation(confirmation)

                if result.get('success'):
                    print(f'  ✓ Successfully accepted')
                    accepted_count += 1
                else:
                    print(f'  ✗ Failed: {result}')
                    failed_count += 1

            except Exception as e:
                print(f'  ✗ Error: {e}')
                failed_count += 1
            
            # Add a small delay to avoid rate limiting (except for the last one)
            if i < len(confirmations):
                time.sleep(0.5)

        print(f'\n=== Summary ===')
        print(f'Total: {len(confirmations)} confirmations')
        print(f'✓ Accepted: {accepted_count}')
        print(f'✗ Failed: {failed_count}')

    except Exception as e:
        print(f'Error fetching confirmations: {e}')


def are_credentials_filled() -> bool:
    return all((api_key, steamguard_path, username, password))


if __name__ == '__main__':
    main()
