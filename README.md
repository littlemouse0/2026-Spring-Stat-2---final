# Final Individual Project: Screen Time and Sleep in the 2007 YRBS

## Student Information
Name:林謙宏  
Student ID: 112370144

## Project Repository
https://github.com/[your-username]/[your-repository-name]

## Presentation Video


## Research Question
Among U.S. high school students in the 2007 Youth Risk Behavior Survey (YRBS), is recreational computer / video game use associated with average sleep duration on school nights?

## Dataset
- File: `data/raw/YRBS_2007.csv`
- Source: CDC Youth Risk Behavior Surveillance System, 2007 National YRBS.
- Cleaned file: `data/processed/yrbs_2007_screen_sleep_cleaned.csv`

## Variables
| Role | Dataset variable | Recoded variable | Description |
|---|---|---|---|
| Outcome | `Sleep` | `sleep_hours_approx` | Average sleep on school nights, recoded from categories to approximate hours: 4, 5, 6, 7, 8, 9, 10. |
| Main predictor | `ComputerUse` | `computer_hours_approx` | Non-school computer/video game use on an average school day, recoded to approximate hours: 0, 0.5, 1, 2, 3, 4, 5. |
| Control | `WhatIsYourSex` | `sex` | Female / Male. |
| Control | `InWhatGradeAreYou` | `grade` | 9th, 10th, 11th, 12th grade. |

## Data Preparation
1. Selected only variables needed for this project.
2. Removed rows with missing values in sleep, computer use, sex, or grade.
3. Removed `Ungraded or other grade` because it was a very small group and not part of standard 9th-12th grade comparison.
4. Recoded categorical survey answers into readable labels and approximate numeric hours.

Final cleaned sample size: **12,042 students**.

## Statistical Methods
This project uses two approved methods:

1. **One-way ANOVA**  
   Tests whether mean sleep hours differ across computer-use groups.

2. **OLS Regression**  
   Estimates the association between approximate computer-use hours and approximate sleep hours, controlling for sex and grade. HC3 robust standard errors are used.

## Key Results
- Mean sleep for students with no recreational screen time: **6.84 hours**.
- Mean sleep for students with 5+ hours of recreational screen time: **6.47 hours**.
- Difference: **-22.3 minutes** for the 5+ hour group compared with the 0-hour group.
- ANOVA result: **F(6, 12035) = 17.41, p = 3.61e-20, eta² = 0.009**.
- Regression result: each additional approximate hour of screen time is associated with **-5.6 minutes** of sleep, controlling for sex and grade, **p < .001**.
- Model R²: **0.039**.

## Interpretation
The ANOVA indicates that average sleep differs across screen-time groups. The regression also shows a statistically significant negative association between recreational screen time and sleep duration. However, the effect size is small. This means screen time is related to sleep, but it explains only a small part of the differences in sleep duration among students.

## Conclusion
Students with more recreational computer/video game use tended to report slightly shorter school-night sleep. The most practical comparison is that students in the 5+ hour group slept about **22 fewer minutes** than students in the 0-hour group. Because this is observational survey data, the result should be interpreted as an association, not proof that screen time causes shorter sleep.

## Repository Structure
```text
.
├── README.md
├── requirements.txt
├── data
│   ├── raw
│   │   └── YRBS_2007.csv
│   └── processed
│       └── yrbs_2007_screen_sleep_cleaned.csv
├── notebooks
│   └── YRBS_Final_Project_Screen_Time_Sleep.ipynb
├── src
│   └── run_analysis.py
└── output
    ├── figures
    ├── infographic
    └── tables
```

## Important Limitation
This is a simplified unweighted class-project analysis. Official YRBS estimates should account for survey weights, strata, and PSU design variables.
