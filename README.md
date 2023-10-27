
# Table of Contents

1.  [Σommit Trade-offs analysis dashboard](#orgefe5322)
    1.  [Introduction](#orgea28313)
    2.  [Screenshots](#org131d59b)
    3.  [Installation](#orgace1b2a)
        1.  [Pre-requisites](#org00793c9)
        2.  [Windows](#org0d5e3eb)
        3.  [Unix-like systems (MacOS, Linux, etc.)](#org11a2a39)
    4.  [How to use the dashboard](#org58a22c6)
        1.  [Comparative visualisation of multidimensional EMT distances between cases](#orgd80073d)
        2.  [How to interact with the dashboard](#orgc057420)
        3.  [Filters](#orgeeb09d8)
        4.  [Interacting with the plot](#orga68335a)
        5.  [How to interpret the visualization](#org25e0fce)
    5.  [Methods](#org211867d)
        1.  [Variables used](#org20358da)
        2.  [Multiple Factor Analysis](#orgac5a1d1)
    6.  [Licensing](#org6991267)


<a id="orgefe5322"></a>

# Σommit Trade-offs analysis dashboard


<a id="orgea28313"></a>

## Introduction

The Σommit Trade-offs analysis dashboard is a web-based user interface (UI) for exploring the dataset released in: Calone, R., Fiore, A., Pellis, G., Mongiano, G., & Bregaglio, S. (2023). Dataset of agronomic case-scenarios and workflow to compute the Σommit index (0.1). Zenodo. <https://doi.org/10.5281/zenodo.10014452>

The dataset was generated taking into account over two milions agronomic case-scenarios relative to the Italian agricultural land and following IPCC Guidelines for National Greenhouse Gas Inventories - Tier 1 ([2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories Volume 4 Agriculture, Forestry and Other Land Use](https://www.ipcc-nggip.iges.or.jp/public/2019rf/vol4.html)) to calculate four trade-off components (i.e. soil organic carbon change, nitrous oxide emissions, nitrate nitrogen leaching, and crop yield) resulting from the interaction of varying management practices under different environmental conditions. A fuzzy logic based methodology was then used to derive the Σommit Index, which can be helpful in performing a cost-benefit analysis considering with respect to the trade-off components and based on a set of pre-defined arbitrary rules. In the implementation of the methodology that produced the dataset that can be explored with the present dashboard, four different sets of rules have been applied, corresponding to four different narratives, namely: balanced weighting scheme, young farmer, agrochemical company, EU Community Agricultural Policy agency.

More details on the rules and data analysis will be found on the main paper "Calone, R., Fiore, A., Pellis, G., Mongiano, G., & Bregaglio, S. A fuzzy logic evaluation of synergies and trade-offs between agricultural production and climate change mitigation" (currently submitted to *Journal of Cleaner Production*).


<a id="org131d59b"></a>

## Screenshots

![img](./sommit_dashboard.png)


<a id="orgace1b2a"></a>

## Installation


<a id="org00793c9"></a>

### Pre-requisites

You will need **Docker** and **Docker Compose** installed. Please refer to official install instructions for your system on the [Docker website](https://docs.docker.com/engine/install/). You'll optionally need Git installed if you want to download the dashboard through git; you can also download this repository via the GitHub interface


<a id="org0d5e3eb"></a>

### Windows

1.  [Download this repository](https://github.com/kofm/sommit-dashboard/archive/refs/heads/main.zip). Alternatively you can clone the repository via PowerShell using the command `git clone https://github.com/kofm/sommit-dashboard`; if that's the case, skip to step 3.
2.  Extract the ZIP file in a directory of your liking.
3.  Inside the downloaded directory you will find a PowerShell script named `StartΣommitDashboard.ps1`. Execute it by double clicking it.
4.  Wait for the installation to complete (it may take a few minutes). Then the dashboard can be reached using you favourite browser (Firefox, Edge, Chrome, ecc.) at the following URL <http://localhost:5001>


<a id="org11a2a39"></a>

### Unix-like systems (MacOS, Linux, etc.)

On Unix-like systems, open your favourite terminal then issue the following commands (assuming that you've git installed):

    git clone https://github.com/kofm/sommit-dashboard
    cd sommit-dashboard
    docker-compose up -d

That's it! Wait for the docker container to be built, then you can reach the container at the following URL <http://localhost:5001>


<a id="org58a22c6"></a>

## How to use the dashboard


<a id="orgd80073d"></a>

### Comparative visualisation of multidimensional EMT distances between cases

This dashboard present a 3D scatterplot visualization showcasing what we can simply call CEMG distances, synthesising four different aspects of agronomic case-scenarios: Environment (E), Management (M), and Trade-off components (T)


<a id="orgc057420"></a>

### How to interact with the dashboard

That's becasue some combinations do not exist.


<a id="orgeeb09d8"></a>

### Filters

1.  Narrative

2.  Environment


<a id="orga68335a"></a>

### Interacting with the plot

1.  Plot controls


<a id="org25e0fce"></a>

### How to interpret the visualization

-   Points: Each point corresponds to a unique agronomic case-scenario defined by crop, environment, management, and GHG fluxes, and the Σommit index.
-   Distance between points: A greater distance between points indicates higher variability or difference in the considered variables.
-   Colour coding: Points are colour-coded based on their rating provided by the Σommit index, allowing for quick comparative analysis.

This visualisation is designed as visual comparison tool of the considered cases based on the calculated EMT distances. For details on how the hyperplane was constructed and distances calculated see the methods section below. Viewers can quickly discern the degree of similarity between cases by observing their relative position on the scatterplot. This visualisation benefits non-experts, providing a visual aid to understand the variability in Environment, Management, and Trade-off components without delving into complex details.

It enables viewers to intuitively understand and evaluate the differences in EMT distances between the various cases studied. The colour-coded points facilitate a quick and easy comparative analysis allowing viewers to infer the relative differences in the Σommit Index. Hovering a point with the mouse reveals more detailed data about the point in the right side panel.

Focusing on the relative distances between the points allows to understand the differences in the combined variables. Use the colour coding as a quick reference to compare the ratings provided by the Î£ommit index. Remember that this visualisation is a high-level representation, and detailed analysis may require a deeper look into the individual variables and cases.


<a id="org211867d"></a>

## Methods


<a id="org20358da"></a>

### Variables used


<a id="orgac5a1d1"></a>

### Multiple Factor Analysis

-   What is a MFA?
-   Grouping of variables

    mfa <- MFA(
      sommit_data,
      group = c(4, 1, 5, 8),
      type = c("s", "s", "n", "n"),
      name.group = c("toc", "si", "env", "mgmt"),
      graph = FALSE
    )


<a id="org6991267"></a>

## Licensing

The software in this repository is licensed under the Apache License 2.0. You can find the terms in the `/app/LICENSE` file.

The data provided in this repository is licensed under the Creative Commons Attribution-ShareAlike (CC-BY-SA). The terms for this license can be found in the `/data/LICENSE` file.

