import smbus
import time

# I2C setup 
I2C_BUS = 1
I2C_ADDRESS = 0x20  
OUTPUT_REGISTER = 0x01  
CONFIG_REGISTER = 0x03  

i2c_bus = smbus.SMBus(I2C_BUS)

# Function to write a value to the Output Register
def set_output(value):
    """
    Writes a value to the output register to set the I/O expander pins.
    value: The n-bit value to write to the register.
    """
    i2c_bus.write_byte_data(I2C_ADDRESS, OUTPUT_REGISTER, value)
    print(f"Written value: {bin(value)} ({value})")

# Function to configure the expander by turning all bits off and allowing the user to select which bits to turn on
def configure_bits_to_turn_on():
    """
    Configures the expander by starting with all bits off and allowing the user to select which bits to turn on.
    """
    # Start with all bits off (value = 0)
    current_value = 0
    set_output(current_value)
    print("All bits turned off (0b00000000).")

    while True:
        print("\nEnter the bit positions you want to turn on (0-7), separated by spaces.")
        print("Example: '0 3 5' will turn on bits 0, 3, and 5.")
        print("Enter 'done' to finish and apply the configuration.")

        user_input = input("Your choice: ")

        if user_input.lower() == "done":
            break

        try:
            # Parse the input and update the bits
            bit_positions = map(int, user_input.split())
            for bit_position in bit_positions:
                if 0 <= bit_position <= 7:
                    current_value |= (1 << bit_position)  # Turn on the specified bit
                else:
                    print(f"Invalid bit position: {bit_position}. Must be between 0 and 7.")
            set_output(current_value)
            print(f"Updated value: {bin(current_value)} ({current_value})")
        except ValueError:
            print("Invalid input. Please enter bit positions as integers separated by spaces.")

# Function to toggle a single bit multiple times
def toggle_bit_multiple_times(bit_position, num_toggles):
    """
    Toggles a single bit at the specified position multiple times.
    bit_position: The bit to toggle (0 to 7).
    num_toggles: The number of times to toggle the bit.
    """
    if not (0 <= bit_position <= 7):
        print("Error: Bit position must be between 0 and 7.")
        return

    current_value = i2c_bus.read_byte_data(I2C_ADDRESS, OUTPUT_REGISTER)
    print(f"Initial value: {bin(current_value)} ({current_value})")

    for i in range(num_toggles):
        # Toggle the specified bit
        current_value ^= (1 << bit_position)
        set_output(current_value)
        print(f"Toggle {i + 1}/{num_toggles}. New value: {bin(current_value)} ({current_value})")
        time.sleep(1)  # Fixed delay of 1 second

if __name__ == "__main__":
    # Set all pins as outputs
    i2c_bus.write_byte_data(I2C_ADDRESS, CONFIG_REGISTER, 0x00)  # Set all pins as outputs
    print("All pins set to output mode.")

    while True:
        # Main menu
        print("\nMenu:")
        print("1. Start with all bits off and select which ones to turn on")
        print("2. Toggle a single bit multiple times")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            configure_bits_to_turn_on()
        elif choice == "2":
            bit_position = int(input("Enter the bit position to toggle (0-7): "))
            num_toggles = int(input("Enter the number of times to toggle the bit: "))
            toggle_bit_multiple_times(bit_position, num_toggles)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
