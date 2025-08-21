# Nial Script's NFT Minting Bot 🌟

A vibrant, animated Python CLI tool for minting NFTs on multiple blockchain networks, including Ethereum, Base, Polygon, Abstract, and ApeChain. Crafted by **Nial Script**, this bot features a colorful, interactive menu with animations, concurrent minting, gas optimization, and robust error handling.

## Features
- **Multi-Network Support**: Mint NFTs on Ethereum, Base, Polygon, Abstract, and ApeChain.
- **Animated CLI Interface**: Rich, colorful menus with loading animations and a dynamic credit banner for **Nial Script**.
- **Concurrent Minting**: Process transactions simultaneously for multiple accounts to maximize speed.
- **Gas Optimization**: Dynamically adjusts gas prices for faster confirmations.
- **Error Handling**: Includes retries with exponential backoff and detailed logging.
- **Manual Configuration**: Input all settings (contract address, ABI, private keys, RPC URLs) via an interactive menu, no `.env` file required.

## Prerequisites
- Python 3.8+
- A reliable RPC provider for each network (e.g., Alchemy, Infura, or public RPCs).
- Contract address and ABI for the target NFT project.
- Private keys for the accounts you want to mint with.
- A terminal supporting ANSI colors (e.g., Windows Terminal, VS Code terminal, or Linux/macOS terminals).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/nialthony/multichain-mint-bot.git
   cd multichain-mint-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup and Usage

### Running the Bot
1. **Start the Script**:
   ```bash
   python mint.py
   ```

2. **Configure Settings via Menu**:
   The animated CLI menu, powered by **Nial Script**, offers:
   - **1. Select Network**: Choose from Ethereum, Base, Polygon, Abstract, or ApeChain (🌍).
   - **2. Set RPC URL**: Update RPC URLs for any network (🔗).
   - **3. Set Quantity**: Specify the number of NFTs to mint (📦).
   - **4. Set Price per Token**: Enter the price per NFT in the network's native token (💰).
   - **5. Set Base Gas Limit**: Set the gas limit for transactions (⛽).
   - **6. Set Gas Multiplier**: Adjust the gas price multiplier (⚡).
   - **7. Set Contract Address**: Input the NFT contract address (🏠).
   - **8. Set Contract ABI**: Paste the contract's ABI in JSON format (📜).
   - **9. Set Private Keys**: Enter comma-separated private keys (🔑).
   - **10. Run Minting**: Execute the minting process (🚀).
   - **0. Exit**: Quit the program.

3. **Example Inputs**:
   - **Contract Address**: `0xYourContractAddress`
   - **Contract ABI** (simplified example):
     ```json
     [{"inputs":[{"internalType":"uint256","name":"quantity","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"mintingActive","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
     ```
   - **Private Keys**: `0xabc123...,0xdef456...`
   - **RPC URL**: `https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY`

### Tutorial: Minting NFTs with Nial Script's Bot
1. **Prepare Contract Details**:
   - Obtain the NFT contract address and ABI from the project (e.g., Magic Eden, OpenSea).
   - Verify the mint function signature (e.g., `mint(uint256 quantity)`). Update the `mint_nft` function if needed.

2. **Configure RPC URLs**:
   - Use reliable RPC providers:
     - Ethereum: Alchemy, Infura, or public nodes.
     - Base: `https://mainnet.base.org`.
     - Polygon: `https://polygon-rpc.com`.
     - Abstract: `https://api.mainnet.abs.xyz`.
     - ApeChain: `https://rpc.apechain.com/http`.
   - Update via menu option 2 if defaults are insufficient.

3. **Set Up Accounts**:
   - Generate or use existing private keys for Ethereum-compatible wallets (e.g., MetaMask).
   - Ensure accounts have sufficient funds for minting fees and gas.

4. **Run the Bot**:
   - Launch the script and enjoy the animated menu by **Nial Script**.
   - Select the network, set contract details, and input private keys.
   - Adjust quantity, price, and gas settings as needed.
   - Run minting (option 10) and watch the animated progress.

5. **Monitor Output**:
   - The bot displays colorful logs for transaction hashes, confirmations, and errors.
   - Check transaction status on block explorers (e.g., Etherscan, Polygonscan).

### Troubleshooting
- **Raw ANSI Codes (e.g., `[36m`, `[0m`)**:
   - If you see raw ANSI codes, your terminal may not fully support them. Try:
     - Using Windows Terminal or VS Code terminal instead of Command Prompt.
     - Ensuring `colorama` is installed (`pip install colorama`).
     - Running the script in a Linux/macOS terminal or a compatible IDE.
   - The script includes a fallback to ensure functionality even if colors are not rendered.

## Security Notes
- **Private Keys**: Enter private keys securely in the CLI. Never share or expose them.
- **Mainnet Caution**: Verify all settings before minting on mainnet to avoid costly errors.
- **Rate Limits**: Ensure your RPC provider supports the transaction volume for concurrent minting.

## Customization
- **Contract Functions**: Update the `mint_nft` function for custom mint functions (e.g., `mintPublic`, `mintWhitelist`).
- **Additional Networks**: Add new networks to the `NETWORKS` dictionary with their RPC URL and chain ID.
- **Gas Strategy**: Modify `gas_multiplier` or add EIP-1559 support for dynamic fees.

## Dependencies
See `requirements.txt` for required Python packages.

## License
MIT License

## Contributing
Submit issues or pull requests to enhance **Nial Script's NFT Minting Bot**. Suggestions for new features or networks are welcome!

## Credits
- **Developed by**: Nial Script 🌟
- **Built with**: Python, web3.py, rich, and colorama for a vibrant, animated experience.

## Disclaimer
This tool is for educational purposes. Use at your own risk, especially on mainnet. Ensure compliance with the NFT project's terms and conditions.