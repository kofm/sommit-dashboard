library(FactoMineR)
library(dplyr)
library(readr)
library(arrow)
library(scales)

# Load the dataset from the RDS file published on Zenodo.
# https://zenodo.org/doi/10.5281/zenodo.10014451
sommit_df_zenodo <- readr::read_rds("data/sommit_df.rds")

# The subset of variables considered in the dashboard.
included_vars <-
    c(
        "ΔSOC(CO2_emissions)",
        "N2O_emissions_(CO2_eq.)",
        "N-NO3_leaching",
        "Crop_yield",
        "Temperature_regime",
        "Moisture_regime",
        "Precipitations",
        "Soil_class",
        "Soil_texture",
        "Crop",
        "Crop_residues",
        "Organic_N_type",
        "Mineral_N_type",
        "Irrigation",
        "N_input",
        "OM_input_(0)",
        "Soil_tillage_(0)",
        ## "Soil_tillage_(0-T)",
        ## "OM_input_(0-T)",
        ## "Mineral_N_fraction",
        ## "Organic_N_fraction",
        ## "Mineral_N_tot",
        ## "Organic_N_tot",
        ## "Animal_manure_tot",
        ## "Green_manure_tot",
        ## "Urea_%",
        ## "Nitrate_%",
        ## "Urea_tot",
        ## "Nitrate_tot",
        ## "ΔSOC",
        ## "N-NO3_leaching_U",
        ## "N2O_emissions",
        "ΣI_NT0",
        "ΣI_NT1_mean",
        "ΣI_NT2_mean",
        "ΣI_NT3_mean"
    )

# Restrict the dataset only to the chosen variables.
sommit_df <-
    sommit_df_zenodo %>%
    dplyr::select(!!!included_vars) %>%
    # Rescale ΔSOC(CO2_emissions) in a range -1 to 1.
    dplyr::mutate(
        dplyr::across("ΔSOC(CO2_emissions)", ~ scales::rescale(.x, to = c(-1, 1))),
    )

# Perform the MFA.
mfa <-
    sommit_df %>%
    # Sommit index is not included in the MFA.
    dplyr::select(-ΣI_NT0, -ΣI_NT1_mean, -ΣI_NT2_mean, -ΣI_NT3_mean) %>%
    FactoMineR::MFA(
        group = c(4, 5, 8),
        type = c("s", "n", "n"),
        name.group = c("toc", "env", "mgmt"),
        graph = FALSE
    )

# Write the dataset to disk in comma-separated value format.
arrow::write_parquet(sommit_df, "data/sommit-data.parquet")

# Write the agronomic case-scenarios MFA coordinates to disk.
arrow::write_parquet(mfa_ind_coord, "data/mfa-ind-coord.parquet")
