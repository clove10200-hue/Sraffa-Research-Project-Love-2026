# Sraffa-Research-Project-Love-2026

Sraffa Model Calculator

## Setup

Follow the instructions on the [uv website](https://docs.astral.sh/uv/getting-started/installation/) to install uv.

Then, run the following command to install the project dependencies:

```bash
uv sync
```

## Usage

Run scripts in the `src` directory using uv:

```bash
uv run src/solve_prices.py
```

# Runescape PvM Economy Model Readme

## Intent

Take in a data structure of a file containing the Sraffan matrix M and q for this PvM economy and output relative price and profit rate data for that economy. The model should be fast and not particularly sensitive to measurement or rounding errors. Sraffan matrices can be further modeled as an eigenvalue problem - the rate of profit is contained within its coefficient matrix's dominant eigenvalue, and its corresponding eigenvector contains the relative prices for that economy, corresponding to each commodity. For this model's purposes, due to the following properties of a sraffan matrix:

1. Nonsymmetric
2. Containing entirely non-negative real values as entries
3. Large and sparse, particularly as the matrix gets very, very large

The algorithm determined to be most useful was power iteration. The main drawbacks of power iteration were determined to be irrelevant, as only the dominant eigenvalue of the matrix is of interest and the fact the model only returns an approximation rather than the exact value is of little concern due to the qualitiative nature of the model's utility - it is meant to provide useful information for informing game developers about the consequences of design decisions on game economies, not provide precise values for a mathematical proof.

## Structure

The dataset is currently a text file that contains each equation for an 'industry' in a Sraffan economy as lines in the text file, arranged such that the sequential numbers correspond to the coefficients of the equation and the final entry of each line is the solution coefficient of that equation.

The dataset used by the extant model are test dataset derived from a heuristic argument regarding how the Runescape PvM economy functions(namely potions and food being spent as commodities sold on Runescape's market to 'produce' boss drops that are themselves sold on the market for profit). The specific data required for a Sraffan matrix - the specific amounts of commodities spent for each individual

## Basic Goods

Sraffan basic goods are a commodity that is used in the production of every other commodity in the economy, either directly or indirectly. The nonstandard nature of production in Runescape makes such a good difficult to identify for the entire economy - iron is not actually used to produce, say, wood as it would be in the real world. However, by focusing on specific sections of the Runescape economy, a set of basic goods can be identified, in that in the Player versus Monster(PvM) economy a certain set of consumables are almost always used by players in order to do so.

The Sraffan basic goods under consideration in this model will be doses of overload potion and sailfin soup, the gold standards for PvM consumables.

(A note: overload potions are not directly sold on the open player market, which would normally preclude them from being a commodity at all. However, its ingredients are sellable on the open market, and thus overload potions could still be included by using the equivalent equations for the production and sale of the ingredients. For simplicity, this model will consider a simplified, condensed equation for overload potions as though they could be sold directly.)

Example: 100,000 doses overload potion, 20,000 sailfin soup, ..... , 0 Saradomin Godsword -> 300,000 doses overload potion

## Non-basic Goods

Non-basic goods are a commodity that is not used in the production of every other commodity in the economy, either directly or indirectly. Such a good is 'segmented off' from the rest of the economy and changes in the industry that produces such a good only affects the relative prices of the commodities it is linked to in production.

In reality, this is a useful property, because it can sometimes be difficult to tell whether or not a good is basic or non-basic, and to what extent it is integrated into the economy if it is non-basic. It can be useful for developers to become aware of how much the wider economy will or will not change by a change in, say, drop rate for a boss drop.

The left-hand side of such an equation will start with the assumed amount of each basic good needed for one boss kill(eg 1 overload, 2 sailfins) and then each term will be multiplied by the inverse of the boss drop rate(i.e. if rate is 1/50 then it becomes 50 overload, 100 sailfins -> 1 boss drop). Then the entire equation will be multiplied by the amount of the drop sold from the market data(i.e. if 100 were sold from the previous example then it becomes 5,000 overload, 10,000 sailfins -> 100 boss drop). In the extant model, test datasets will be calculated in a way that emulates this process, by selecting a random number to represent the 'average' number of potions and food items needed to kill a boss, setting its solution coefficient to zero, and then multiplying the entire equation by some integer to represent the total number of boss drops collected in a certain production period.

## Possibilities for extentions in the future

in reality, armor degrades as it is used in high-level Runescape content. This means that armor is itself 'consumed' when it is used
to produce other boss drops. Jagex could track this economic data directly(by, say, tracking how many points of damage each piece of armor takes after each boss kill and aggregating that data for a period of time) but it is difficult to approximate with publicly available market data, as it is unknown to what extent boss drops are bought to replace degraded armor, least of all how much of each individual armor is used in the production of each individual drop. A future model may simply act as though we were Jagex and had access to that data and create an entirely fictional dataset to prove a proof of concept.
