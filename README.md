# Sommit Trade-offs Dashboard

Sommit Dashboard is a companion web-based UI for exploring the dataset released in: Calone, R., Fiore, A., Pellis, G., Mongiano, G., & Bregaglio, S. (2023). Dataset of agronomic case-scenarios and workflow to compute the Σommit index (0.1). Zenodo. https://doi.org/10.5281/zenodo.10014452

More details and data analysis can be found on the main paper "Calone, R., Fiore, A., Pellis, G., Mongiano, G., & Bregaglio, S. A fuzzy logic evaluation of synergies and trade-offs between agricultural production and climate change mitigation" (currently under review).

## Comparative visualisation of multidimensional GEMG distances between cases

This dashboard present a 3D scatterplot visualization showcasing what we can simply call as the GEMG distances, synthesising four different aspects of agronomic case-scenarios: Genotype (G), Environment (E), Management (M), and Greenhouse Gas (GHG) fluxes.

## How to interact with the dashboard

In the top section you can choose

## How to interpret the visualization

- Points: Each point corresponds to a unique agronomic case-scenario defined by crop, environment, management, and resulting GHG fluxes.
- Distance between points: A greater distance between points indicates higher variability or difference in the considered variables.
- Colour coding: Points are colour-coded based on their rating provided by the Σommit index, allowing for quick comparative analysis.

This visualisation is designed as visual comparison tool of the considered cases based on the calculated GEMG distances. For details on how the hyperplane was constructed and distances calculated see the methods section below. Viewers can quickly discern the degree of similarity between cases by observing their relative position on the scatterplot. This visualisation benefits non-experts, providing a visual aid to understand the variability in Genotype, Environment, Management, and GHG fluxes without delving into complex details.

It enables viewers to intuitively understand and evaluate the differences in GEMG distances between the various cases studied. The colour-coded points facilitate a quick and easy comparative analysis, allowing viewers, even with no expert knowledge, to infer the relative differences in the considered variables at a glance. Hovering a point with the mouse reveals more detailed data on the point in the right side panel. 

Focusing on the relative distances between the points allows to understand the differences in the combined variables. Use the colour coding as a quick reference to compare the ratings provided by the Σommit index.
Remember that this visualisation is a high-level representation, and detailed analysis may require a deeper look into the individual variables and cases.
