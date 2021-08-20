# Data Structure
Each experiment has a plaintext __.csv__ file that stores the time series data for each sensor within the respective structure. The *Time* column, in seconds, in each experiment file is offset based on when ignition occurred. In other words, negative values represent background data and positive values represent time post-ignition. The *Timestamp* column represents the local clock time during which the experiment was conducted. This column is used to sync the corresponding **_Events.csv** file to the primary data file for each experiment. The **_Events** file contains the relevant actions performed during the experiments (e.g., ignition, ventilation, burner off).

## Single-Story Experiments
The total heat release rate for the single-story structure was 250 kW. The event timing for each experiment can be found in the corresponding **_Events.csv** file.

| Exp # | Description | Date     |
|-------|-------------|----------|
| 1     |             | 10-18-16 |
| 1R2   | Replicate of Exp 1 | 10-18-16 |
| 1R3   | Replicate of Exp 1 | 10-18-16 |
| 2     |             | 10-19-16 |
| 3     |             | 10-19-16 |


## Two-Story Experiments
The total heat release rate for the two-story structure was 500 kW. The event timing for each experiment can be found in the corresponding **_Events.csv** file.

| Exp # | Description | Date     |
|-------|-------------|----------|
| 4     |             | 11-09-16 |
| 4R2   | Replicate of Exp 4 | 11-09-16 |
| 4R3   | Replicate of Exp 4 | 11-09-16 |
| 4R4   | Replicate of Exp 4 | 11-10-16 |
| 5     |             | 11-10-16 |
| 5R2   | Replicate of Exp 5 | 11-10-16 |
| 6     |             | 11-10-16 |
| 6R2   | Replicate of Exp 6 | 11-10-16 |

### Notes
Instrumentation was installed at vents that were not explicitly used as part of these experiments but were used as part of a larger project. More information can be found here: [Impact of Fixed Ventilation on Fire Damage Patterns](https://fireinvestigation.fsri.org/). As a result, there are data included at vents that remained closed through the duration of some experiments.