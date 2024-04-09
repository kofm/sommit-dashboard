#!/usr/bin/env Rscript

processing_needed <- function() {
    if (!file.exists("/data/mfa-ind-coord.csv")) {
        return(TRUE)
    }
    return(FALSE)
}

rescale_vector <- function(vec, min_val, max_val) {
    if (!is.numeric(vec)) {
        stop("vec must be a numeric vector")
    }

    range_vec <- range(vec, na.rm = TRUE)

    rescaled_vec <-
        min_val + ((vec - range_vec[1]) / (range_vec[2] - range_vec[1])) *
            (max_val - min_val)

    rescaled_vec[is.nan(rescaled_vec)] <- 0

    return(rescaled_vec)
}

scale_to_unit_variance <- function(vec) {
    sd_vec <- sd(vec)
    if (sd_vec == 0) {
        stop("Standard deviation cannot be zero.")
    }
    return(vec / sd_vec)
}

process_data <- function() {

    # Load the dataset from the RDS file published on Zenodo.
    # https://zenodo.org/doi/10.5281/zenodo.10014451
    url <- "https://zenodo.org/records/10014452/files/sommit_df.RDS?download=1"
    con <- url(url, "rb")
    sommit_df_zenodo <- readRDS(con)
    close(con)

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
            "ΣI_NT0",
            "ΣI_NT1_mean",
            "ΣI_NT2_mean",
            "ΣI_NT3_mean"
        )

    tocs_vars <-
        c("ΔSOC(CO2_emissions)", "N2O_emissions_(CO2_eq.)",
            "N-NO3_leaching", "Crop_yield")

    # Restrict the dataset only to the chosen variables.
    sommit_df <- sommit_df_zenodo[included_vars]

    # Perform the MFA.
    sommit_indexes <- c("ΣI_NT0", "ΣI_NT1_mean", "ΣI_NT2_mean", "ΣI_NT3_mean")
    mfa_cols <-
        names(sommit_df)[!(names(sommit_df) %in% sommit_indexes)]
    mfa_data <- sommit_df[mfa_cols]
    # Scale TOCs to unit variance.
    mfa_data[tocs_vars] <- lapply(mfa_data[tocs_vars], scale_to_unit_variance)
    mfa <-
        FactoMineR::MFA(
            mfa_data,
            group = c(4, 5, 8),
            type = c("s", "n", "n"),
            graph = FALSE
        )

    # Write the dataset to disk in comma-separated value format.
    # TODO: scale in range 0-1 for dashboard
    sommit_df[c("ΔSOC(CO2_emissions)", "N2O_emissions_(CO2_eq.)",
        "N-NO3_leaching")] <-
        lapply(sommit_df[c("ΔSOC(CO2_emissions)", "N2O_emissions_(CO2_eq.)",
        "N-NO3_leaching")], rescale_vector, 0, 1)

    sommit_df$"Crop_yield" <-
        ave(
            sommit_df$"Crop_yield",
            sommit_df$"Crop",
            FUN = function(x) rescale_vector(x, 0, 1)
        )

    write.csv(sommit_df, "sommit-data.csv", row.names = FALSE)


    # Write the agronomic case-scenarios MFA coordinates to disk.
    write.csv(mfa$ind$coord, "mfa-ind-coord.csv", row.names = FALSE)
}


input_file <- "/data/sommit_data.rds"
hash_file <- "/data/input_files_hash.txt"

if (processing_needed()) {
    process_data()
} else {
    cat("Already processed. Skipping processing.\n")
}
