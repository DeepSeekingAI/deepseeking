from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from web3 import Web3

class BaseBlockchain(ABC):
    """
    Abstract base class for blockchain interactions.
    Defines the interface for blockchain operations.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the blockchain interface with configuration.
        
        Args:
            config: Dictionary containing blockchain configuration
        """
        self.config = config
        self.web3 = None
        self.contracts = {}

    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to the blockchain network.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    async def deploy_contract(self, contract_name: str, args: List[Any]) -> str:
        """
        Deploy a smart contract to the blockchain.
        
        Args:
            contract_name: Name of the contract to deploy
            args: Contract constructor arguments
            
        Returns:
            Deployed contract address
        """
        pass

    @abstractmethod
    async def call_contract(self, contract_address: str, method_name: str, args: List[Any]) -> Any:
        """
        Call a smart contract method.
        
        Args:
            contract_address: Address of the contract
            method_name: Name of the method to call
            args: Method arguments
            
        Returns:
            Result of the contract call
        """
        pass

    @abstractmethod
    async def send_transaction(self, transaction: Dict[str, Any]) -> str:
        """
        Send a blockchain transaction.
        
        Args:
            transaction: Transaction parameters
            
        Returns:
            Transaction hash
        """
        pass

    @abstractmethod
    async def get_events(self, contract_address: str, event_name: str, from_block: int) -> List[Dict[str, Any]]:
        """
        Get contract events.
        
        Args:
            contract_address: Address of the contract
            event_name: Name of the event to get
            from_block: Starting block number
            
        Returns:
            List of event data
        """
        pass 