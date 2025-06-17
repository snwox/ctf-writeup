// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "./SafeToken.sol";
import "./libraries/TickMath.sol";

contract SafeExchanger {
    using SafeERC20 for SafeToken;
    using TickMath for int24;

    SafeToken public immutable token;
    int24 public currentTick;
    int24 public constant TICK_SPACING = 10;

    struct Liquidity {
        uint256 tokenAmount;
        uint256 ethAmount;
    }

    struct TickLiquidity {
        uint256 tokenAmount;
        uint256 ethAmount;
    }

    mapping(bytes32 => Liquidity) public userLiquidity;
    mapping(int24 => TickLiquidity) public liquidityByTick;

    event LiquidityAdded(address indexed user, int24 lowerTick, int24 upperTick, uint256 tokenAmount, uint256 ethAmount);
    event LiquidityRemoved(address indexed user, int24 lowerTick, int24 upperTick, uint256 tokenAmount, uint256 ethAmount);
    event Swap(address indexed user, bool ethToToken, uint256 amountIn, uint256 amountOut);

    constructor(SafeToken _token, int24 _currentTick) {
        token = _token;
        currentTick = _currentTick;
    }

    function addLiquidity(int24 lowerTick, int24 upperTick, uint256 tokenAmount) external payable {
        require(tokenAmount > 0, "Invalid token amount");
        require(lowerTick < upperTick, "Invalid tick range");
        require(lowerTick % TICK_SPACING == 0 && upperTick % TICK_SPACING == 0, "Invalid tick spacing");

        uint256 price = getPricebyRatio(currentTick);
        uint256 requiredEth = (tokenAmount * price) / 1e18;

        require(msg.value >= requiredEth, "Insufficient ETH provided");

        token.safeTransferFrom(msg.sender, address(this), tokenAmount);

        bytes32 positionKey = keccak256(abi.encodePacked(msg.sender, upperTick, lowerTick));
        userLiquidity[positionKey].tokenAmount += tokenAmount;
        userLiquidity[positionKey].ethAmount += requiredEth;

        uint24 tickCount = uint24((upperTick - lowerTick) / TICK_SPACING) + 1;
        uint256 tokenPerTick = tokenAmount / tickCount;
        uint256 ethPerTick = requiredEth / tickCount;

        for (int24 tick = lowerTick; tick <= upperTick; tick += TICK_SPACING) {
            liquidityByTick[tick].tokenAmount += tokenPerTick;
            liquidityByTick[tick].ethAmount += ethPerTick;
        }

        liquidityByTick[upperTick].tokenAmount += tokenAmount % tickCount;
        liquidityByTick[upperTick].ethAmount += requiredEth % tickCount;

        if (msg.value > requiredEth) {
            payable(msg.sender).transfer(msg.value - requiredEth);
        }

        emit LiquidityAdded(msg.sender, lowerTick, upperTick, tokenAmount, requiredEth);
    }

    function removeLiquidity(int24 lowerTick, int24 upperTick, uint256 liquidityPercentage) external {
        require(liquidityPercentage > 0 && liquidityPercentage <= 100, "Invalid liquidity percentage");

        bytes32 positionKey = keccak256(abi.encodePacked(msg.sender, upperTick, lowerTick));
        Liquidity storage position = userLiquidity[positionKey];

        uint256 tokenAmount = (position.tokenAmount * liquidityPercentage) / 100;
        uint256 ethAmount = (position.ethAmount * liquidityPercentage) / 100;

        require(tokenAmount > 0 && ethAmount > 0, "Insufficient liquidity");

        position.tokenAmount -= tokenAmount;
        position.ethAmount -= ethAmount;

        uint24 tickCount = uint24((upperTick - lowerTick) / TICK_SPACING) + 1;
        uint256 tokenPerTick = tokenAmount / tickCount;
        uint256 ethPerTick = ethAmount / tickCount;

        for (int24 tick = lowerTick; tick <= upperTick; tick += TICK_SPACING) {
            TickLiquidity storage tickLiquidity = liquidityByTick[tick];
            if (tickLiquidity.tokenAmount >= tokenPerTick) {
                tickLiquidity.tokenAmount -= tokenPerTick;
                tickLiquidity.ethAmount -= ethPerTick;
            } else {
                tickLiquidity.tokenAmount = 0;
                tickLiquidity.ethAmount = 0;
            }
        }

        TickLiquidity storage upperTickLiquidity = liquidityByTick[upperTick];
        if (upperTickLiquidity.tokenAmount >= tokenAmount % tickCount) {
            upperTickLiquidity.tokenAmount -= tokenAmount % tickCount;
            upperTickLiquidity.ethAmount -= ethAmount % tickCount;
        }

        token.safeTransfer(msg.sender, tokenAmount);
        payable(msg.sender).transfer(ethAmount);

        emit LiquidityRemoved(msg.sender, lowerTick, upperTick, tokenAmount, ethAmount);
    }

    function swap(bool ethToToken, uint256 amountIn) external payable {
        require(amountIn > 0, "Invalid amount");

        if (ethToToken) {
            require(msg.value == amountIn, "Incorrect ETH amount");
            liquidityByTick[currentTick].ethAmount += amountIn;
            uint256 amountOut = performSwap(true, amountIn);
            token.safeTransfer(msg.sender, amountOut);
            emit Swap(msg.sender, true, amountIn, amountOut);
        } else {
            token.safeTransferFrom(msg.sender, address(this), amountIn);
            liquidityByTick[currentTick].tokenAmount += amountIn;
            uint256 amountOut = performSwap(false, amountIn);
            payable(msg.sender).transfer(amountOut);
            emit Swap(msg.sender, false, amountIn, amountOut);
        }
    }

    function performSwap(bool ethToToken, uint256 amountIn) public returns (uint256) {
        uint256 amountOut = 0;
        uint256 remaining = amountIn;

        while (remaining > 0) {
            TickLiquidity storage tickLiquidity = liquidityByTick[currentTick];
            uint256 availableLiquidity = ethToToken ? tickLiquidity.tokenAmount : tickLiquidity.ethAmount;

            if (availableLiquidity == 0) {
                if (ethToToken) {
                    currentTick -= TICK_SPACING;
                } else {
                    currentTick += TICK_SPACING;
                }
                continue;
            }

            uint256 price = getPricebyRatio(currentTick);
            uint256 swapAmount;
            uint256 convertedAmount;

            if (ethToToken) {
                swapAmount = remaining;
                convertedAmount = (swapAmount * 1e18) / price;
                if (convertedAmount > availableLiquidity) {
                    convertedAmount = availableLiquidity;
                    swapAmount = (convertedAmount * price) / 1e18;
                }
            } else {
                swapAmount = remaining;
                convertedAmount = (swapAmount * price) / 1e18;
                if (convertedAmount > availableLiquidity) {
                    convertedAmount = availableLiquidity;
                    swapAmount = (convertedAmount * 1e18) / price;
                }
            }

            require(swapAmount <= remaining, "Swap amount exceeds remaining");
            require(convertedAmount <= availableLiquidity, "Insufficient liquidity");

            amountOut += ethToToken ? convertedAmount : convertedAmount;
            remaining -= swapAmount;

            if (ethToToken) {
                tickLiquidity.tokenAmount -= convertedAmount;
                tickLiquidity.ethAmount += swapAmount;
            } else {
                tickLiquidity.ethAmount -= convertedAmount;
                tickLiquidity.tokenAmount += swapAmount;
            }

            if (remaining == 0) break;

            if (ethToToken) {
                currentTick -= TICK_SPACING;
            } else {
                currentTick += TICK_SPACING;
            }
        }

        require(amountOut > 0, "Insufficient liquidity");
        return amountOut;
    }

    function getPricebyRatio(int24 tick) public view returns (uint256) {
        uint160 sqrtPrice = tick.getSqrtRatioAtTick();
        uint256 price = sqrtPrice;
        price *= price;
        price /= 2 ** 96;
        price *= 1e18;
        price /= 2 ** 96;
        return price;
    }

    receive() external payable {}
}