# data analysis scripts BA
Data analysis scripts used for the Bachelor Thesis "A Particle Filter Approach to Bioelectric Catheter Localization"

![img.png](img.png)


## preprocessing pipeline
EM signal:
- offset correction and projection by script project_em_groundtruth_on_centerline.py
- calculation of cumulative groundtruth displacement by script project_em_groundtruth_on_centerline.py
- mapping of EM data on bioelctric timestamps by function interpolate_em_on_bioelectric() by script extract_displacement_and_bioelectric_data.py

Bioelectric signal:
- recording impedance and displacement data based on bioelectric sensor setup as presented by **[1]**
- Gaussian filtering and z-standardization by interpolate_em_on_bioelectric() by script extract_displacement_and_bioelectric_data.py


Reference generation:
- generation of references for cross validation approach by script prepare_cross_validation_maps.py
- generation of reference by FEM-simulation by script prepare_simulated_reference.py


## post-hoc analysis of in-vitro recorded catheter runs
- post hoc trajectory estimation by function posthoc_run_3D_vessel_navigator() of script post_hoc_particle_filter_analysis.py
- post hoc trajectory estimation for cross-validation approach by function cross_validation() of script post_hoc_particle_filter_analysis.py
- performance evaluation by function evaluate_performance_cross_validation() of script post_hoc_particle_filter_analysis.py


## data analysis and statistics
- normal post hoc catheter runs: [input RMSE of all samples] -> prepare_for_statistics.py -> restructured as .csv file, then statistical_evaluation.py
- cross validation post hoc catheter runs: [input RMSE of all samples] -> prepare_for_cross_validation_statistics.py -> restructured as .csv file, then statistical_evaluation.py
- Determination of accuracy of branch position estimates of the post-hoc filter runs by script particle_pruning_statistics.py
- Plotting of performance result figure by script plot_performance_results.py
- Plotting post_hoc catheter runs vs. groundtruth, and alpha change over update steps by script plot_result_figures.py


## Conductivity test series in agar
- Determination of the cell constant of the bioelectric catheter by script cell_constant_determinator.py
- Calculating the conductivity of the probes based on conductance and cell constant by script conductivity_calculator.py

## License
Copyright (c) 2023 Christian Johannes Friess, CC BY-SA 4.0

## references

**[1]** Maier, Heiko, Heribert Schunkert, and Nassir Navab (2023). “Extending bioelectric
navigation for displacement and direction detection.” In: International
journal of computer assisted radiology and surgery. DOI: 10.1007/s11548-
023-02927-w.

