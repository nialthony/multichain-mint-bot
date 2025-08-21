from web3 import Web3
from web3.exceptions import TransactionNotFound
import asyncio
import json
from eth_account import Account
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from colorama import init
import time
import itertools
import sys

# Initialize colorama for cross-platform colored text
init(strip=False, convert=True)

# Initialize rich console with force_terminal for better compatibility
console = Console(force_terminal=True, force_jupyter=False)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Check terminal ANSI support
if not console.is_terminal:
    logger.warning("Terminal may not fully support ANSI colors, some formatting may be affected.")

# Network configurations
NETWORKS = {
    'ethereum': {
        'rpc_url': 'https://ethereum.publicnode.com',
        'chain_id': 1
    },
    'base': {
        'rpc_url': 'https://mainnet.base.org',
        'chain_id': 8453
    },
    'polygon': {
        'rpc_url': 'https://polygon-rpc.com',
        'chain_id': 137
    },
    'abstract': {
        'rpc_url': 'https://api.mainnet.abs.xyz',
        'chain_id': 2741
    },
    'apechain': {
        'rpc_url': 'https://rpc.apechain.com/http',
        'chain_id': 33139
    }
}

# Default settings
selected_network = 'ethereum'
quantity = 1
price_per_token = Web3.to_wei('0.099', 'ether')
base_gas_limit = 200_000
gas_multiplier = 1.2
contract_address = '0x0000000000000000000000000000000000000000'
contract_abi = []
private_keys = []

# Animated credit display
def display_credit():
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    credit_text = "Created by Nial Script"
    for color in itertools.cycle(colors):
        console.print(f"[bold {color}]🌟 {credit_text} 🌟[/bold {color}]", justify="center")
        time.sleep(0.2)
        console.clear()
        break  # Single cycle for initial display

# Loading animation
def loading_animation(message="Loading"):
    with Progress(
        SpinnerColumn(),
        TextColumn(f"[bold cyan]{message}...[/bold cyan]"),
        transient=True
    ) as progress:
        progress.add_task(description=message, total=None)
        time.sleep(2)

# CLI Menu Functions
def select_network():
    global selected_network
    display_credit()
    console.print(Panel("🌍 Select Blockchain Network", style="bold magenta"))
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("No.", justify="center")
    table.add_column("Network", justify="left")
    table.add_column("RPC URL", justify="left")
    for i, net in enumerate(NETWORKS.keys(), 1):
        table.add_row(str(i), net.capitalize(), NETWORKS[net]['rpc_url'])
    console.print(table)
    try:
        choice = int(console.input("[cyan]Select network (number): [/cyan]")) - 1
        if 0 <= choice < len(NETWORKS):
            selected_network = list(NETWORKS.keys())[choice]
            console.print(f"[green]Selected network: {selected_network.capitalize()}[/green]")
        else:
            console.print("[red]Invalid choice.[/red]")
    except ValueError:
        console.print("[red]Invalid input. Enter a number.[/red]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

def set_rpc_url():
    global NETWORKS
    display_credit()
    console.print(Panel("🔗 Configure RPC URLs", style="bold magenta"))
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Network", justify="left")
    table.add_column("RPC URL", justify="left")
    for net in NETWORKS:
        table.add_row(net.capitalize(), NETWORKS[net]['rpc_url'])
    console.print(table)
    network = console.input("[cyan]Enter network name to edit RPC (e.g., ethereum): [/cyan]").lower()
    if network in NETWORKS:
        new_rpc = console.input(f"[cyan]Enter new RPC URL for {network}: [/cyan]")
        NETWORKS[network]['rpc_url'] = new_rpc
        console.print(f"[green]Updated RPC URL for {network}: {new_rpc}[/green]")
    else:
        console.print("[red]Invalid network.[/red]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

def set_quantity():
    global quantity
    display_credit()
    console.print(Panel("📦 Set Mint Quantity", style="bold magenta"))
    try:
        quantity = int(console.input("[cyan]Enter quantity to mint: [/cyan]"))
        console.print(f"[green]Quantity set to: {quantity}[/green]")
    except ValueError:
        console.print("[red]Invalid input. Quantity must be an integer.[/red]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

def set_price_per_token():
    global price_per_token
    display_credit()
    console.print(Panel("💰 Set Price per Token", style="bold magenta"))
    try:
        price = float(console.input("[cyan]Enter price per token in native token (e.g., 0.099): [/cyan]"))
        price_per_token = Web3.to_wei(price, 'ether')
        console.print(f"[green]Price per token set to: {price} (in native token)[/green]")
    except ValueError:
        console.print("[red]Invalid input. Price must be a number.[/red]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

def set_gas_limit():
    global base_gas_limit
    display_credit()
    console.print(Panel("⛽ Set Base Gas Limit", style="bold magenta"))
    try:
        base_gas_limit = int(console.input("[cyan]Enter base gas limit: [/cyan]"))
        console.print(f"[green]Base gas limit set to: {base_gas_limit}[/green]")
    except ValueError:
        console.print("[red]Invalid input. Gas limit must be an integer.[/red]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

def set_gas_multiplier():
    global gas_multiplier
    display_credit()
    console.print(Panel("⚡ Set Gas Multiplier", style="bold magenta"))
    try:
        gas_multiplier = float(console.input("[cyan]Enter gas multiplier (e.g., 1.2): [/cyan]"))
        console.print(f"[green]Gas multiplier set to: {gas_multiplier}[/green]")
    except ValueError:
        console.print("[red]Invalid input. Gas multiplier must be a number.[/red]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

def set_contract_address():
    global contract_address
    display_credit()
    console.print(Panel("🏠 Set Contract Address", style="bold magenta"))
    try:
        addr = console.input("[cyan]Enter contract address: [/cyan]")
        contract_address = Web3.to_checksum_address(addr)
        console.print(f"[green]Contract address set to: {contract_address}[/green]")
    except ValueError:
        console.print("[red]Invalid contract address.[/red]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

def set_contract_abi():
    global contract_abi
    display_credit()
    console.print(Panel("📜 Set Contract ABI", style="bold magenta"))
    try:
        abi_str = console.input("[cyan]Enter contract ABI (JSON format): [/cyan]")
        contract_abi = json.loads(abi_str)
        console.print("[green]Contract ABI updated successfully.[/green]")
    except json.JSONDecodeError:
        console.print("[red]Invalid JSON format for ABI.[/red]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

def set_private_keys():
    global private_keys
    display_credit()
    console.print(Panel("🔑 Set Private Keys", style="bold magenta"))
    private_keys_str = console.input("[cyan]Enter private keys (comma-separated): [/cyan]")
    private_keys = [key.strip() for key in private_keys_str.split(',') if key.strip()]
    console.print(f"[green]Set {len(private_keys)} private keys.[/green]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

def main_menu():
    while True:
        console.clear()
        display_credit()
        console.print(Panel("🚀 Nial Script's NFT Minting Bot 🚀", style="bold magenta", title="Main Menu"))
        table = Table(show_header=False, show_lines=True)
        table.add_column(justify="left")
        table.add_row(f"[cyan]1. Select Network[/cyan] (Current: {selected_network.capitalize()})")
        table.add_row(f"[cyan]2. Set RPC URL[/cyan]")
        table.add_row(f"[cyan]3. Set Quantity[/cyan] (Current: {quantity})")
        table.add_row(f"[cyan]4. Set Price per Token[/cyan] (Current: {Web3.from_wei(price_per_token, 'ether')} native)")
        table.add_row(f"[cyan]5. Set Base Gas Limit[/cyan] (Current: {base_gas_limit})")
        table.add_row(f"[cyan]6. Set Gas Multiplier[/cyan] (Current: {gas_multiplier})")
        table.add_row(f"[cyan]7. Set Contract Address[/cyan] (Current: {contract_address})")
        table.add_row(f"[cyan]8. Set Contract ABI[/cyan] (Current: {'Set' if contract_abi else 'Not set'})")
        table.add_row(f"[cyan]9. Set Private Keys[/cyan] (Current: {len(private_keys)} keys)")
        table.add_row(f"[cyan]10. Run Minting[/cyan]")
        table.add_row(f"[red]0. Exit[/red]")
        console.print(table)
        choice = console.input("[cyan]Enter choice: [/cyan]")

        loading_animation("Processing")
        if choice == '1':
            select_network()
        elif choice == '2':
            set_rpc_url()
        elif choice == '3':
            set_quantity()
        elif choice == '4':
            set_price_per_token()
        elif choice == '5':
            set_gas_limit()
        elif choice == '6':
            set_gas_multiplier()
        elif choice == '7':
            set_contract_address()
        elif choice == '8':
            set_contract_abi()
        elif choice == '9':
            set_private_keys()
        elif choice == '10':
            run_minting()
        elif choice == '0':
            console.print("[red]Exiting... Thank you for using Nial Script's Minting Bot![/red]")
            break
        else:
            console.print("[red]Invalid choice.[/red]")
            console.input("[yellow]Press Enter to continue...[/yellow]")

# Minting Functions
def get_web3():
    config = NETWORKS[selected_network]
    return Web3(Web3.HTTPProvider(config['rpc_url'], request_kwargs={'timeout': 60}))

def check_minting_availability(contract):
    try:
        is_minting_active = contract.functions.mintingActive().call()
        max_supply = contract.functions.maxSupply().call()
        total_supply = contract.functions.totalSupply().call()
        return is_minting_active and total_supply < max_supply
    except Exception as e:
        logger.error(f"Error checking minting availability: {e}")
        return False

def get_optimized_gas_price(web3):
    try:
        gas_price = web3.eth.gas_price
        return int(gas_price * gas_multiplier)
    except Exception as e:
        logger.error(f"Error fetching gas price: {e}")
        return web3.to_wei('50', 'gwei')

async def mint_nft(quantity, price_per_token, private_key, max_retries=3):
    web3 = get_web3()
    config = NETWORKS[selected_network]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    sender_account = Account.from_key(private_key)
    sender_address = sender_account.address
    retries = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Minting for {task.fields[address]}...[/bold cyan]"),
        transient=True
    ) as progress:
        task = progress.add_task("Minting", address=sender_address)
        while retries < max_retries:
            try:
                if not check_minting_availability(contract):
                    progress.console.print(f"[red]Minting not available for {sender_address}[/red]")
                    return False

                nonce = web3.eth.get_transaction_count(sender_address, 'pending')
                txn = contract.functions.mint(
                    quantity,
                ).build_transaction({
                    'from': sender_address,
                    'gas': base_gas_limit,
                    'gasPrice': get_optimized_gas_price(web3),
                    'nonce': nonce,
                    'value': price_per_token * quantity,
                    'chainId': config['chain_id']
                })

                signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                progress.console.print(f"[green]Mint transaction sent from {sender_address} on {selected_network}. Hash: {tx_hash.hex()}[/green]")

                receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                if receipt.status == 1:
                    progress.console.print(f"[green]Transaction confirmed for {sender_address}: {tx_hash.hex()}[/green]")
                    return True
                else:
                    progress.console.print(f"[red]Transaction failed for {sender_address}: {tx_hash.hex()}[/red]")
                    return False

            except TransactionNotFound:
                progress.console.print(f"[yellow]Transaction not found for {sender_address}, retrying ({retries + 1}/{max_retries})[/yellow]")
                retries += 1
                await asyncio.sleep(2 ** retries)
            except Exception as e:
                progress.console.print(f"[red]Error during minting for {sender_address}: {e}[/red]")
                retries += 1
                await asyncio.sleep(2 ** retries)
        return False

async def mint_concurrently(quantity, price_per_token, private_keys):
    if not private_keys:
        console.print("[red]No private keys provided.[/red]")
        return
    if not contract_abi:
        console.print("[red]Contract ABI not set.[/red]")
        return
    if contract_address == '0x0000000000000000000000000000000000000000':
        console.print("[red]Invalid contract address.[/red]")
        return

    tasks = [mint_nft(quantity, price_per_token, pk) for pk in private_keys]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            console.print(f"[red]Failed to mint for account {i + 1}: {result}[/red]")
        elif result:
            console.print(f"[green]Successfully minted for account {i + 1}[/green]")
        else:
            console.print(f"[yellow]Minting failed or not available for account {i + 1}[/yellow]")

def run_minting():
    web3 = get_web3()
    if not web3.is_connected():
        console.print(f"[red]Failed to connect to {selected_network} network[/red]")
        return

    console.print(f"[cyan]Starting minting on {selected_network} for {len(private_keys)} accounts[/cyan]")
    asyncio.run(mint_concurrently(quantity, price_per_token, private_keys))
    console.print("[cyan]Minting process complete.[/cyan]")
    console.input("[yellow]Press Enter to continue...[/yellow]")

if __name__ == "__main__":
    console.clear()
    loading_animation("Starting Nial Script's NFT Minting Bot")
    main_menu()