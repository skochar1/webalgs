
# Network Algorithms for Web and Crowds

This repository contains a collection of network algorithms designed for analyzing social networks, predicting links, and simulating cascade models. These algorithms have been developed to address various aspects of network analysis and modeling, including the glass ceiling effect by gender on social media platforms, link prediction, and cascade simulations in infection and economic models.

## Table of Contents
- [Introduction](#introduction)
- [Algorithms](#algorithms)
  - [Glass Ceiling Analysis](#glass-ceiling-analysis)
    - [By Betweenness Centrality](#by-betweenness-centrality)
    - [By K-Centrality](#by-k-centrality)
    - [By Degrees](#by-degrees)
  - [Link Prediction](#link-prediction)
  - [Cascade Simulations](#cascade-simulations)
    - [Out-Degree Seeds](#out-degree-seeds)
    - [Centrality Seeds](#centrality-seeds)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

This repository provides tools for network analysis and modeling, focusing on social media platforms. The algorithms included can be used to analyze the presence of a glass ceiling effect by gender or other metrics, predict links within a network, and simulate cascade processes relevant to infection spread or economic impacts.

## Algorithms

### Glass Ceiling Analysis

The analysis algorithms provided in this section are designed to explore the glass ceiling effect within social networks. These analyses can be adapted to other metrics beyond gender as well.

#### By Betweenness Centrality
**File:** `analysis_by_bet_centrality.py`

This script analyzes the network based on betweenness centrality, which measures the extent to which a node lies on the shortest paths between other nodes. This can help identify key influencers and potential barriers in the network.

#### By K-Centrality
**File:** `analysis_by_k_centrality.py`

This script uses k-centrality, which focuses on the centrality of nodes based on their connectivity. This method helps in understanding the hierarchical structure and influence distribution in the network.

#### By Degrees
**File:** `analysis_by_degrees.py`

This script analyzes the network by the degree of nodes, which counts the number of connections each node has. It provides insights into the most connected individuals and potential hubs within the network.

### Link Prediction

**File:** `link_prediction.py`

This script implements the reconciliation algorithm for link prediction. The reconciliation algorithm is used to predict future connections within a network based on existing structure and patterns. It helps in understanding the potential growth and evolution of the network.

### Cascade Simulations

The cascade simulation algorithms simulate the spread of information, infections, or economic impacts through a network.

#### Out-Degree Seeds
**File:** `outdeg_seeds.py`

This script simulates cascades using out-degree seeds, where the nodes with the highest number of outgoing connections are chosen as the starting points for the cascade. This method helps in modeling scenarios where highly connected individuals initiate the spread.

#### Centrality Seeds
**File:** `centrality_seeds.py`

This script simulates cascades using centrality seeds, where nodes with the highest centrality measures are chosen as the starting points. This approach is useful for understanding the impact of influential nodes on the spread within the network.

## Usage

To use these algorithms, clone the repository and run the desired script using Python. Ensure you have the necessary dependencies installed.

\`\`\`bash
git clone https://github.com/yourusername/network-algorithms.git
cd network-algorithms
python analysis_by_bet_centrality.py
\`\`\`

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code follows the existing style and includes appropriate documentation.
