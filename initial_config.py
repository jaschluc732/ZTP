#!/usr/bin/env python

import os
import sys

# Arista EOS CLI library
from AristaPy.eossdk import Cli

def main():
    # Initialize the CLI object
    cli = Cli()

    # Log file for debugging (optional)
    # with open("/mnt/flash/ztp_log.txt", "a") as f:
    #     f.write("ZTP script started at: " + str(os.path.getmtime("/mnt/flash/ztp_script.py")) + "\n")

    try:
        # Example: Set hostname based on serial number (or other unique identifier)
        # This assumes the script knows how to derive the desired hostname
        # For a real-world scenario, you might fetch this from a central source
        #hostname = "Arista-Switch-001" # Replace with logic to determine hostname
        #cli.run_commands(["configure terminal", f"hostname {hostname}", "end"])

        # Example: Configure management interface
        cli.run_commands([
            "configure terminal",
            "interface Management1",
            "ip address dhcp", # Replace with your IP address
            "no shutdown",
            "end"
        ])

        # Example: Configure default route
        cli.run_commands([
            "configure terminal",
            "ip route 0.0.0.0/0 192.168.5.1", # Replace with your default gateway
            "end"
        ])

        # Example: Copy a more comprehensive configuration from a remote server
        # This is a common ZTP pattern: a small script fetches the main config
        # cli.run_commands(["copy scp://user:password@10.0.0.1/path/to/full_config.cfg running-config"])

        # Example: Install an EOS extension (if needed)
        # cli.run_commands(["extension \"http://server/path/to/extension.rpm\"", "extension activate extension.rpm"])

        # Save the running configuration to startup-config
        cli.run_commands(["write memory"])

        # Log completion (optional)
        # with open("/mnt/flash/ztp_log.txt", "a") as f:
        #     f.write("ZTP script completed successfully.\n")

    except Exception as e:
        # Log any errors
        # with open("/mnt/flash/ztp_log.txt", "a") as f:
        #     f.write(f"ZTP script error: {e}\n")
        sys.exit(1) # Indicate failure

if __name__ == "__main__":
    main()
